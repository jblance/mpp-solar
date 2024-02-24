""" protocols / abstractprotocol.py """
import abc
import logging
import re

import construct as cs

from powermon.commands.command import Command
from powermon.commands.command_definition import CommandDefinition
from powermon.commands.result import ResultType
from powermon.commands.trigger import Trigger
from powermon.dto.command_definition_dto import CommandDefinitionDTO
from powermon.dto.protocolDTO import ProtocolDTO
from powermon.errors import (CommandDefinitionIncorrect,
                             CommandDefinitionMissing, InvalidResponse,
                             PowermonProtocolError)
from powermon.outputs import multiple_from_config
from powermon.ports.porttype import PortType
from powermon.protocols.helpers import crc_pi30 as crc

log = logging.getLogger("AbstractProtocol")


class AbstractProtocol(metaclass=abc.ABCMeta):
    """
    base definition for all protocols
    protocol has:
    - protocol id
    - dict of command definitions
    and functions to:
    - add / remove / count / get command definitions
    - check validity / crc / trim / split response
    """

    def __init__(self) -> None:
        self.command_definitions: dict[str, CommandDefinition] = {}
        self.supported_ports = [PortType.TEST,]
        self.id_command = None

    @property
    def protocol_id(self) -> bytes:
        """ return the protocol id """
        return self._protocol_id

    @protocol_id.setter
    def protocol_id(self, value):
        self._protocol_id = value

    def add_supported_ports(self, port_types: list):
        """ Add to the supported port types list """
        self.supported_ports.extend(port_types)

    def clear_supported_ports(self):
        """ Remove all supported port types except the TEST port type """
        self.supported_ports = [PortType.TEST,]

    def add_command_definitions(self, command_definitions_config: dict, result_type: ResultType = None):
        """ Add command definitions from the configuration """
        for command_definition_key in command_definitions_config.keys():
            try:
                log.debug("Attempting to add command_definition_key: %s", command_definition_key)
                _config = command_definitions_config[command_definition_key]
                if result_type is not None:
                    # Adding command definition with supplied type, so override config
                    log.debug("result_type override to %s", result_type)
                    _config["result_type"] = result_type
                command_definition = CommandDefinition.from_config(_config)
                self.command_definitions[command_definition_key] = command_definition
            except ValueError as value_error:
                log.info("couldnt add command definition for code: %s", command_definition_key)
                log.info("error was: %s", value_error)

    def remove_command_definitions(self, commands_to_remove: list = None):
        """ Remove specified command definitions """
        if commands_to_remove is None:
            return
        for command_to_remove in commands_to_remove:
            self.command_definitions.pop(command_to_remove, None)

    def get_command_definition(self, command: str) -> CommandDefinition:
        """ Get the command definition for a given command string """
        # Handle the commands that don't have a regex
        if command in self.command_definitions and self.command_definitions[command].regex is None:
            log.debug("Found command %s in protocol %s", command, self._protocol_id)
            command_definition = self.command_definitions[command]
            log.debug(command_definition)
            return command_definition

        # Try the regex commands
        for command_code, command_definition in self.command_definitions.items():
            if command_definition.regex is not None:
                log.debug("Regex commands _command: %s", command_code)
                _re = re.compile(command_definition.regex)
                match = _re.match(command)
                if match:
                    log.debug("Matched: %s to: %s value: %s", command, command_definition.code, match.group(1))
                    log.debug(command_definition)
                    return command_definition
        log.info("No command_defn found for %s", command)
        raise CommandDefinitionMissing(f"No command definition found for command: {command}")

    def check_definitions_count(self, expected=None):
        """ check and report number of command definitions, error if 0 """
        definitions_count = len(self.command_definitions)
        if definitions_count == 0:
            raise PowermonProtocolError(f"Attempted to load protocol '{self.protocol_id}' which has no valid commands")
        if expected is None:
            log.info("Using protocol:%s with %i commands (%s)", self.protocol_id, definitions_count, ', '.join(self.command_definitions.keys()))
            return
        if expected == definitions_count:
            log.info("Using protocol:%s found %i commands as expected (%s)", self.protocol_id, definitions_count, ', '.join(self.command_definitions.keys()))
            return
        else:
            raise PowermonProtocolError(f"Loaded protocol '{self.protocol_id}' but found {definitions_count} commands, expected {expected}")

    def get_command_definition_dtos(self) -> dict[str, CommandDefinitionDTO]:
        """ convert all associated command objects to data transfer objects """
        command_dtos: dict[str, CommandDefinitionDTO] = {}
        for command_tuple in self.command_definitions.items():
            command_dtos[command_tuple[0]] = command_tuple[1].to_dto()
        return command_dtos

    def list_commands(self) -> dict[str, CommandDefinition]:
        """ list available commands for the protocol """
        if self.protocol_id is None:
            log.error("Attempted to list commands with no protocol defined")
            raise ValueError("Attempted to list commands with no protocol defined")
        return self.command_definitions

    def get_full_command(self, command: str) -> bytes:
        """ generate the full command including crc and \n as needed """
        log.info("Using protocol: %s with %i commands", self.protocol_id, len(self.command_definitions))
        byte_cmd = bytes(command, "utf-8")
        # calculate the CRC
        crc_high, crc_low = crc(byte_cmd)
        # combine byte_cmd, CRC , return
        full_command = byte_cmd + bytes([crc_high, crc_low, 13])
        log.debug("full command: %s", full_command)
        return full_command

    def check_valid(self, response: str, command_definition: CommandDefinition = None) -> bool:
        """ check response is valid """
        log.debug("check valid for %s, definition: %s", response, command_definition)
        if response is None:
            raise InvalidResponse("Response is None")
        if len(response) <= 3:
            raise InvalidResponse("Response is too short")
        return True

    def check_crc(self, response: str, command_definition: CommandDefinition = None) -> bool:
        """ crc check, needs override in protocol """
        log.debug("no check crc for %s, definition: %s", response, command_definition)
        return True

    def trim_response(self, response: str, command_definition: CommandDefinition = None) -> str:
        """ Remove extra characters from response """
        log.debug("trim %s, definition: %s", response, command_definition)
        return response[1:-3]

    def split_response(self, response: str, command_definition: CommandDefinition = None) -> list:
        """ split response into individual items, return as ordered list or list of tuples """
        result_type = getattr(command_definition, "result_type", None)
        log.debug("splitting %s, result_type %s", response, result_type)
        match result_type:
            case None:
                responses = []
            case ResultType.ACK | ResultType.SINGLE | ResultType.MULTIVALUED:
                responses = response
            case ResultType.COMMA_DELIMITED:
                responses = response.split(b",")
            case ResultType.SLICED:
                responses = []
                for position in range(command_definition.reading_definition_count()):
                    rd = command_definition.get_reading_definition(position=position)
                    responses.append(response[rd.slice_array[0]:rd.slice_array[1]])
            case ResultType.VED_INDEXED:
                # build a list of (index,value) tuples
                responses = []
                for item in response.split(b'\r\n'):
                    try:
                        key, value = item.split(b'\t')
                    except ValueError:
                        continue
                    if isinstance(key, bytes):
                        key = key.decode()
                    responses.append((key.strip(), value.strip()))
            case ResultType.CONSTRUCT:
                # build a list of (index, value) tuples, after parsing with a construct
                responses = []
                # check for construct
                if command_definition.construct is None:
                    raise CommandDefinitionIncorrect("No construct found in command_definition")
                if command_definition.construct_min_response is None:
                    raise CommandDefinitionIncorrect("No construct_min_response found in command_definition")
                if len(response) < command_definition.construct_min_response:
                    raise InvalidResponse(f"response:{response}, len:{len(response)} too short for parsing (expecting {command_definition.construct_min_response:})")
                # parse with construct
                result = command_definition.construct.parse(response)
                # print(result)
                for x in result:
                    match type(result[x]):
                        # case cs.ListContainer:
                        #     print(f"{x}:listcontainer")
                        case cs.Container:
                            # print(f"{x}:")
                            for y in result[x]:
                                if y != "_io":
                                    key = y
                                    value = result[x][y]
                                    responses.append((key, value))
                        case _:
                            if x != "_io":
                                key = x
                                value = result[x]
                                responses.append((key, value))
            case _:
                responses = response.split()
        log.debug("responses: '%s'", responses)
        return responses

    def to_dto(self) -> ProtocolDTO:
        """ convert protocol object to data transfer object """
        dto = ProtocolDTO(protocol_id=self.protocol_id, commands=self.get_command_definition_dtos())
        return dto

    def get_id_command(self) -> Command:
        """ return the command that generates a unique id for this type of device """
        if self.id_command is None:
            raise PowermonProtocolError(f"self.id_command must be defined in protocol {self.protocol_id}")
        cd = self.get_command_definition(self.id_command)
        outputs = multiple_from_config({"type": "screen", "format": "raw"})
        trigger = Trigger.from_config(None)
        command = Command(code=self.id_command, commandtype=cd.command_type, outputs=outputs, trigger=trigger)
        command.command_definition = cd
        command.full_command = self.get_full_command(self.id_command)
        log.debug(command)
        return command

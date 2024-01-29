""" protocols / abstractprotocol.py """
import abc
import logging
import re

from mppsolar.protocols.protocol_helpers import crcPI as crc
from powermon.commands.command_definition import CommandDefinition
from powermon.commands.result import ResultType
from powermon.dto.command_definition_dto import CommandDefinitionDTO
from powermon.dto.protocolDTO import ProtocolDTO
from powermon.errors import CommandDefinitionMissing, InvalidResponse, PowermonProtocolError

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
        self.STATUS_COMMANDS = None
        self.SETTINGS_COMMANDS = None
        self.DEFAULT_COMMAND = None
        self.ID_COMMANDS = None

    @property
    def protocol_id(self) -> bytes:
        """ return the protocol id """
        return self._protocol_id

    @protocol_id.setter
    def protocol_id(self, value):
        self._protocol_id = value

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
            return self.command_definitions[command]

        # Try the regex commands
        for command_code, command_definition in self.command_definitions.items():
            if command_definition.regex is not None:
                log.debug("Regex commands _command: %s", command_code)
                _re = re.compile(command_definition.regex)
                match = _re.match(command)
                if match:
                    log.debug("Matched: %s to: %s value: %s", command, command_definition.code, match.group(1))
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

    def split_response(self, response: str, command_definition: CommandDefinition = None) -> list | dict:
        """ split response into individual items, return as ordered list or keyed dict """
        result_type = getattr(command_definition, "result_type", None)
        log.debug("splitting %s, result_type %s", response, result_type)
        match result_type:
            case None:
                responses = []
            case ResultType.ACK | ResultType.SINGLE | ResultType.MULTIVALUED:
                responses = response
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
            case _:
                responses = response.split()
        log.debug("responses: '%s'", responses)
        return responses

    def to_dto(self) -> ProtocolDTO:
        """ convert protocol object to data transfer object """
        dto = ProtocolDTO(protocol_id=self.protocol_id, commands=self.get_command_definition_dtos())
        return dto

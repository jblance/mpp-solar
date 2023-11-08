""" protocols / abstractprotocol.py """
import abc
import logging
import re

from mppsolar.protocols.protocol_helpers import crcPI as crc
# from powermon.commands.command import Command
from powermon.commands.command_definition import CommandDefinition
from powermon.commands.reading_definition import ReadingDefinition
# from powermon.commands.result import Result, ResultType
from powermon.dto.command_definition_dto import CommandDefinitionDTO
from powermon.dto.protocolDTO import ProtocolDTO
from powermon.errors import PowermonProtocolError, PowermonWIP

log = logging.getLogger("AbstractProtocol")


class AbstractProtocol(metaclass=abc.ABCMeta):
    """ base definition for all protocols """

    def __init__(self) -> None:
        self._command = None
        self._command_dict = None
        self.command_definitions: dict[str, CommandDefinition] = {}
        self.STATUS_COMMANDS = None
        self.SETTINGS_COMMANDS = None
        self.DEFAULT_COMMAND = None
        self.ID_COMMANDS = None
        self._protocol_id = None

    def check_definitions_count(self):
        """ check and report number of command definitions, error if 0 """
        definitions_count = len(self.command_definitions)
        if definitions_count == 0:
            raise PowermonProtocolError(f"Attempted to load protocol '{self._protocol_id}' which has no valid commands")
        log.info("Using protocol:%s with %i commands", self._protocol_id, definitions_count)
        # log.info(f'Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands')

    def to_dto(self) -> ProtocolDTO:
        """ convert protocol object to data transfer object """
        dto = ProtocolDTO(protocol_id=self._protocol_id, commands=self.get_command_definition_dtos())
        return dto

    def get_command_definition_dtos(self) -> dict[str, CommandDefinitionDTO]:
        """ convert all associated command objects to data transfer objects """
        command_dtos: dict[str, CommandDefinitionDTO] = {}
        for command_tuple in self.command_definitions.items():
            command_dtos[command_tuple[0]] = command_tuple[1].to_dto()
        return command_dtos

    def add_command_definitions(self, command_definitions_config: dict):
        """ Add command definitions from the configuration """
        for command_definition_key in command_definitions_config.keys():
            try:
                log.debug("Attempting to add command_definition_key: %s", command_definition_key)
                command_definition = CommandDefinition.from_config(command_definitions_config[command_definition_key])
                self.command_definitions[command_definition_key] = command_definition
            except ValueError as value_error:
                log.info("couldnt add command definition for code: %s", command_definition_key)
                log.info("error was: %s", value_error)

    def list_commands(self) -> dict[str, CommandDefinition]:
        """ list available commands for the protocol """
        if self._protocol_id is None:
            log.error("Attempted to list commands with no protocol defined")
            raise ValueError("Attempted to list commands with no protocol defined")
        return self.command_definitions

    def get_protocol_id(self) -> bytes:
        """ return the protocol id """
        return self._protocol_id

    def get_full_command(self, command) -> bytes:
        """ generate the full command including crc and \n as needed """
        log.info("Using protocol: %s with %i commands", self._protocol_id, len(self.command_definitions))
        byte_cmd = bytes(command, "utf-8")
        # calculate the CRC
        crc_high, crc_low = crc(byte_cmd)
        # combine byte_cmd, CRC , return
        full_command = byte_cmd + bytes([crc_high, crc_low, 13])
        log.debug("full command: %s", full_command)
        return full_command

    def get_response_definition(self, command_definition: CommandDefinition, index=None, key=None) -> ReadingDefinition:
        """ get the definition of a specific response component """
        # QUESTION: is this not a readingdefinition? ie get_reading_definition??
        definitions_count = command_definition.get_response_definition_count()
        if index is not None:
            if index < definitions_count:
                return command_definition.reading_definitions[index]
            else:
                # return [index, f"Unknown value in response {index}", "bytes.decode", ""]
                raise IndexError(f"Index {index} out of range for command {command_definition.code}")
        elif key is not None:
            log.error("key todo abprotocol line 80")  # TODO: add key type get response defn
            raise PowermonWIP("get_response_defn needs key logic implemented")
        else:
            raise PowermonWIP("get_response_defn needs index or key")

    def get_command_with_command_string(self, command) -> CommandDefinition:
        """
        Get the command definition for a given command string
        """

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
                    # QUESTION: Is this the only spot to set a parameter for a command?
                    command_definition.set_parameter_value(match.group(1))
                    return command_definition
        log.info("No command_defn found for %s", command)
        return None

    def check_crc(self, response: str):
        """ crc check, needs override in protocol """
        log.debug("check crc for %s", response)
        return

    def check_response_and_trim(self, response: str) -> str:
        """
        Simplest validity check, CRC checks should be added to individual protocols
        """
        log.debug("response: %s", response)
        if response is None:
            raise ValueError("Response is None")
        if len(response) <= 3:
            raise ValueError("Response is too short")
        self.check_crc(response)
        response = response[1:-3]
        return response

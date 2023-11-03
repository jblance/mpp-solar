import abc
import calendar  # noqa: F401
import logging
import re

# from typing import Tuple

# from mppsolar.protocols.protocol_helpers import uptime  # noqa: F401
# from mppsolar.protocols.protocol_helpers import (  # noqa: F401
#     BigHex2Float,
#     BigHex2Short,
#     Hex2Ascii,
#     Hex2Int,
#     Hex2Str,
#     LittleHex2Float,
#     LittleHex2Int,
#     LittleHex2Short,
#     LittleHex2UInt,
# )
from mppsolar.protocols.protocol_helpers import crcPI as crc
from powermon.dto.protocolDTO import ProtocolDTO
from powermon.commands.result import ResultType
from powermon.commands.result import Result
from powermon.commands.reading_definition import ReadingDefinition
from powermon.commands.command import Command
from powermon.commands.command_definition import CommandDefinition
from powermon.dto.command_definition_dto import CommandDefinitionDTO

log = logging.getLogger("AbstractProtocol")


class AbstractProtocol(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self._command = None
        self._command_dict = None
        self.command_definitions: dict[str, CommandDefinition] = {}
        self.STATUS_COMMANDS = None
        self.SETTINGS_COMMANDS = None
        self.DEFAULT_COMMAND = None
        self.ID_COMMANDS = None
        self._protocol_id = None

    def toDTO(self) -> ProtocolDTO:
        dto = ProtocolDTO(protocol_id=self._protocol_id, commands=self.get_command_definition_dtos())
        return dto

    def add_command_definitions(self, command_definitions_config: dict, command_definition_type):
        """Add command definitions from the configuration"""
        for course_definition_key in command_definitions_config.keys():
            course_definition = CommandDefinition.from_config(command_definitions_config[course_definition_key], command_definition_type)
            self.command_definitions[course_definition_key] = course_definition

    def list_commands(self) -> dict[str, CommandDefinition]:
        # print(f"{'Parameter':<30}\t{'Value':<15} Unit")
        if self._protocol_id is None:
            log.error("Attempted to list commands with no protocol defined")
            return {"ERROR": ["Attempted to list commands with no protocol defined", ""]}
        # result = {}
        # result["_command"] = "command help"
        # result["_command_description"] = f"List available commands for protocol {str(self._protocol_id, 'utf-8')}"
        # for command in sorted(self.COMMANDS):
        #    if "help" in self.COMMANDS[command]:
        #        info = self.COMMANDS[command]["description"] + self.COMMANDS[command]["help"]
        #    else:
        #        info = self.COMMANDS[command]["description"]
        #    result[command] = [info, ""]
        return self.command_definitions

    def get_command_definition_dtos(self) -> dict[str, CommandDefinitionDTO]:
        command_dtos: dict[str, CommandDefinitionDTO] = {}
        for command_tuple in self.command_definitions.items():
            command_dtos[command_tuple[0]] = command_tuple[1].to_dto()
        return command_dtos

    def get_protocol_id(self) -> bytes:
        return self._protocol_id

    def get_full_command(self, command) -> bytes:
        log.info(f"Using protocol {self._protocol_id} with {len(self.command_definitions)} commands")
        byte_cmd = bytes(command, "utf-8")
        # calculate the CRC
        crc_high, crc_low = crc(byte_cmd)
        # combine byte_cmd, CRC , return
        full_command = byte_cmd + bytes([crc_high, crc_low, 13])
        log.debug(f"full command: {full_command}")
        return full_command

    def get_response_definition(self, command_definition: CommandDefinition, index=None, key=None) -> ReadingDefinition:
        definitions_count = command_definition.get_response_definition_count()
        if index is not None:
            if index < definitions_count:
                return command_definition.reading_definitions[index]
            else:
                # return [index, f"Unknown value in response {index}", "bytes.decode", ""]
                raise IndexError(f"Index {index} out of range for command {command_definition.code}")
        elif key is not None:
            log.error("key todo abprotocol line 80")  # TODO: add key type get response defn
            raise Exception("get_response_defn needs key logic implemented")
        else:
            raise Exception("get_response_defn needs index or key")

    def get_command_with_command_string(self, command) -> CommandDefinition:
        """
        Get the command definition for a given command string
        """
        
        #Handle the commands that don't have a regex
        if command in self.command_definitions and self.command_definitions[command].regex is None:
            log.debug("Found command %s in protocol %s", command, self._protocol_id)
            return self.command_definitions[command]
        
        #Try the regex commands
        for command_code, command_definition in self.command_definitions.items():
            if command_definition.regex is not None:
                log.debug("Regex commands _command: %s", command_code)
                _re = re.compile(command_definition.regex)
                match = _re.match(command)
                if match:
                    log.debug("Matched: %s to: %s value: %s", command, command_definition.code, match.group(1))
                    #Is this the only spot to set a parameter for a command?
                    command_definition.set_parameter_value(match.group(1))
                    return command_definition
        log.info("No command_defn found for %s", command)
        return None



    def check_response_and_trim(self, response: str) -> str:
        """
        Simplest validity check, CRC checks should be added to individual protocols
        """
        if response is None:
            raise ValueError("Response is None")
        else:
            response = response[1:-3]
        return response

    

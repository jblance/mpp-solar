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
from powermon.commands.response_definition import ResponseDefinition
from powermon.commands.command import Command
from powermon.commands.command_definition import CommandDefinition
from powermon.dto.command_definition_dto import CommandDefinitionDTO

log = logging.getLogger("AbstractProtocol")


class AbstractProtocol(metaclass=abc.ABCMeta):
    def __init__(self, *args, **kwargs) -> None:
        self._command = None
        self._command_dict = None
        self.command_definitions : dict[str, CommandDefinition] = {}
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
        #result = {}
        #result["_command"] = "command help"
        #result["_command_description"] = f"List available commands for protocol {str(self._protocol_id, 'utf-8')}"
        #for command in sorted(self.COMMANDS):
        #    if "help" in self.COMMANDS[command]:
        #        info = self.COMMANDS[command]["description"] + self.COMMANDS[command]["help"]
        #    else:
        #        info = self.COMMANDS[command]["description"]
        #    result[command] = [info, ""]
        return self.command_definitions
    
    def get_command_definition_dtos(self) -> dict[str, CommandDefinitionDTO]:
        command_dtos: dict[str, CommandDefinitionDTO] = {}
        for command_tuple in self.command_definitions.items():
            command_dtos[command_tuple[0]] = command_tuple[1].to_DTO()
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

    def get_response_definition(self, command_definition: CommandDefinition, index=None, key=None) -> ResponseDefinition:
        definitions_count = command_definition.get_response_definition_count()
        if index is not None:
            if index < definitions_count:
                return command_definition.response_definitions[index]
            else:
                #return [index, f"Unknown value in response {index}", "bytes.decode", ""]
                raise IndexError(f"Index {index} out of range for command {command_definition.code}")
        elif key is not None:
            log.error("key todo abprotocol line 80")  # TODO: add key type get response defn
            raise Exception("get_response_defn needs key logic implemented")
        else:
            raise Exception("get_response_defn needs index or key")

    def get_command_definition(self, command) -> CommandDefinition:
        log.debug(f"Processing command '{command}'")
        if command in self.command_definitions and self.command_definitions[command].regex is None:
            log.debug(f"Found command {command} in protocol {self._protocol_id}")
            return self.command_definitions[command]
        for _command_code in self.command_definitions.keys():
            if self.command_definitions[_command_code].regex is not None:
                log.debug(f"Regex commands _command: {_command_code}")
                _re = re.compile(self.command_definitions[_command_code].regex)
                match = _re.match(command)
                if match:
                    log.debug(f"Matched: {command} to: {self.command_definitions[_command_code].code} value: {match.group(1)}")
                    self._command_value = match.group(1)
                    return self.command_definitions[_command_code]
        log.info(f"No command_defn found for {command}")
        return None

    def get_responses(self, response) -> list:
        """
        Default implementation of split and trim
        """
        # Trim leading '(' + trailing CRC and \r of response, then split
        return response[1:-3].split(None)

    def check_response_valid(self, result: Result) -> Result:
        """
        Simplest validity check, CRC checks should be added to individual protocols
        """
        if result.raw_response_blob is None:
            result.is_valid = False
            result.error = True
            result.error_messages.append("failed validity check: response was empty")
        else:
            result.is_valid = True
        return result


    def decode(self, result: Result, command: Command):
        #TODO: this should return something instead of modifying result, then it's easy to test
        #TODO: should be moved into a Result class
        """
        Take the a result object and decode the raw response
        into a ??? dict of name: value, unit entries
        """

        log.info(f"result.raw_response passed to decode: {result.raw_response_blob}")

        # Check response is valid
        self.check_response_valid(result)
        if result.error:
            return
        
        # Cant decode without a definition of the command
        if command.command_definition is None:
            log.debug(f"No definition for command {command.code}")
            result.error = True
            result.error_messages.append(f"failed to decode responses: no definition for {command.code}")
            return
        
        if command.command_definition.response_type is ResultType.MULTIVALUED:
            response = result.raw_response_blob[1:-3] #this should be moved to the protocol, it should check the CRC then strip them
            responses = command.validate_and_translate_raw_value(response, index=0)
            result.add_responses(responses)
        else:
            # Split the response into individual responses
            for i, raw_response in enumerate(self.get_responses(result.raw_response_blob)):
                responses = command.validate_and_translate_raw_value(raw_response, index=i)
                result.add_responses(responses)
        log.debug(f"trimmed and split responses: {result.responses}")
        
        #TODO: this is ugly, info types need to be reworked to not have code in the protocol definition
        #IF there are more response definitions than responses, check if they are INFO and fill them in
        number_of_responses = len(result.get_responses())
        if len(command.get_response_definitions()) > number_of_responses:
            for index in range(number_of_responses, len(command.get_response_definitions())):
                response_definition = command.get_response_definitions()[index]
                if response_definition.is_info():
                    result.add_responses(response_definition.response_from_raw_values(command.code))
                index += 1
        return


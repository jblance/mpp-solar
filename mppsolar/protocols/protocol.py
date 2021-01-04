import abc
import logging
import re
from typing import Tuple

from .protocol_helpers import crcPI as crc

log = logging.getLogger("MPP-Solar")


class AbstractProtocol(metaclass=abc.ABCMeta):
    def __init__(self, *args, **kwargs) -> None:
        self._command = None
        self._command_dict = None
        self.COMMANDS = {}
        self.STATUS_COMMANDS = None
        self.SETTINGS_COMMANDS = None
        self.DEFAULT_COMMAND = None
        self._protocol_id = None

    def get_protocol_id(self) -> bytes:
        return self._protocol_id

    def get_full_command(self, command) -> bytes:
        log.info(
            f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands"
        )
        # These need to be set to allow other functions to work
        self._command = command
        self._command_defn = self.get_command_defn(command)
        # End of required variables setting

        byte_cmd = bytes(self._command, "utf-8")
        # calculate the CRC
        crc_high, crc_low = crc(byte_cmd)
        # combine byte_cmd, CRC , return
        full_command = byte_cmd + bytes([crc_high, crc_low, 13])
        log.debug(f"full command: {full_command}")
        return full_command

    def get_command_defn(self, command) -> dict:
        log.debug(f"get_command_defn for: {command}")
        if self._command is None:
            return None
        if command in self.COMMANDS:
            # print(command)
            log.debug(f"Found command {self._command} in protocol {self._protocol_id}")
            return self.COMMANDS[command]
        for _command in self.COMMANDS:
            if "regex" in self.COMMANDS[_command] and self.COMMANDS[_command]["regex"]:
                log.debug(f"Regex commands _command: {_command}")
                _re = re.compile(self.COMMANDS[_command]["regex"])
                match = _re.match(command)
                if match:
                    log.debug(
                        f"Matched: {command} to: {self.COMMANDS[_command]['name']} value: {match.group(1)}"
                    )
                    self._command_value = match.group(1)
                    return self.COMMANDS[_command]
        log.info(f"No command_defn found for {command}")
        return None

    def get_responses(self, response) -> list:
        """
        Default implementation of split and trim
        """
        responses = response.split(b" ")
        # Trim leading '(' of first response
        responses[0] = responses[0][1:]
        # Remove CRC and \r of last response
        responses[-1] = responses[-1][:-3]
        return responses

    def check_response_valid(self, response) -> Tuple[bool, dict]:
        """
        Simplest validity check, CRC checks should be added to individual protocols
        """
        if response is None:
            return False, {"ERROR": ["No response", ""]}
        return True, {}

    def decode(self, response, show_raw) -> dict:
        log.info(f"response passed to decode: {response}")

        valid, msgs = self.check_response_valid(response)
        if not valid:
            log.info(msgs["ERROR"][0])
            return msgs

        # Raw response requested
        if show_raw:
            log.debug(f'Protocol "{self._protocol_id}" raw response requested')
            # TODO: deal with \x09 type crc response items better
            _response = b""
            for item in response:
                _response += chr(item).encode()
            raw_response = _response.decode("utf-8")
            msgs["raw_response"] = [raw_response, ""]
            return msgs

        # Check for a stored command definition
        if not self._command_defn:
            # No definiution, so just return the data
            len_command_defn = 0
            log.debug(
                f"No definition for command {self._command}, raw response returned"
            )
            msgs["ERROR"] = [
                f"No definition for command {self._command} in protocol {self._protocol_id}",
                "",
            ]
        else:
            len_command_defn = len(self._command_defn["response"])
        # Decode response based on stored command definition
        # if not self.is_response_valid(response):
        #    log.info('Invalid response')
        #    msgs['ERROR'] = ['Invalid response', '']
        #    msgs['response'] = [response, '']
        #    return msgs

        responses = self.get_responses(response)

        log.debug(f"trimmed and split responses: {responses}")

        for i, result in enumerate(responses):
            # decode result
            result = result.decode("utf-8")
            # Check if we are past the 'known' responses
            if i >= len_command_defn:
                resp_format = ["string", f"Unknown value in response {i}", ""]
            else:
                resp_format = self._command_defn["response"][i]

            key = "{}".format(resp_format[1]).lower().replace(" ", "_")
            # log.debug(f'result {result}, key {key}, resp_format {resp_format}')
            # Process results
            if resp_format[0] == "float":
                if "--" in result:
                    result = 0
                msgs[key] = [float(result), resp_format[2]]
            elif resp_format[0] == "int":
                if "--" in result:
                    result = 0
                msgs[key] = [int(result), resp_format[2]]
            elif resp_format[0] == "string":
                msgs[key] = [result, resp_format[2]]
            elif resp_format[0] == "10int":
                if "--" in result:
                    result = 0
                msgs[key] = [float(result) / 10, resp_format[2]]
            # eg. ['option', 'Output source priority', ['Utility first', 'Solar first', 'SBU first']],
            elif resp_format[0] == "option":
                msgs[key] = [resp_format[2][int(result)], ""]
            # eg. ['keyed', 'Machine type', {'00': 'Grid tie', '01': 'Off Grid', '10': 'Hybrid'}],
            elif resp_format[0] == "keyed":
                msgs[key] = [resp_format[2][result], ""]
            # eg. ['flags', 'Device status', [ 'is_load_on', 'is_charging_on' ...
            elif resp_format[0] == "flags":
                for j, flag in enumerate(result):
                    msgs[resp_format[2][j]] = [int(flag), "True - 1/False - 0"]
            # eg. ['stat_flags', 'Warning status', ['Reserved', 'Inver...
            elif resp_format[0] == "stat_flags":
                output = ""
                for j, flag in enumerate(result):
                    if flag == "1":
                        output = "{}\n\t- {}".format(output, resp_format[2][j])
                msgs[key] = [output, ""]
            # eg. ['enflags', 'Device Status', {'a': {'name': 'Buzzer', 'state': 'disabled'},
            elif resp_format[0] == "enflags":
                # output = {}
                status = "unknown"
                for item in result:
                    if item == "E":
                        status = "enabled"
                    elif item == "D":
                        status = "disabled"
                    else:
                        # output[resp_format[2][item]['name']] = status
                        _key = (
                            "{}".format(resp_format[2][item]["name"])
                            .lower()
                            .replace(" ", "_")
                        )
                        msgs[_key] = [status, ""]
                # msgs[key] = [output, '']
            elif self._command_defn["type"] == "SETTER":
                _key = "{}".format(self._command_defn["name"]).lower().replace(" ", "_")
                msgs[_key] = [result, ""]
            else:
                msgs[i] = [result, ""]
        return msgs

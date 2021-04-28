import abc
import logging
import re
from typing import Tuple

from ..helpers import get_resp_defn
from .protocol_helpers import Big2ByteHex2Int  # noqa: F401
from .protocol_helpers import Little2ByteHex2Int  # noqa: F401
from .protocol_helpers import Hex2Int  # noqa: F401
from .protocol_helpers import Hex2Str  # noqa: F401
from .protocol_helpers import crcPI as crc

log = logging.getLogger("AbstractProtocol")


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
            f"get_full_command: Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands"
        )

        byte_cmd = bytes(command, "utf-8")
        # calculate the CRC
        crc_high, crc_low = crc(byte_cmd)
        # combine byte_cmd, CRC , return
        full_command = byte_cmd + bytes([crc_high, crc_low, 13])
        log.debug(f"get_full_command: full command: {full_command}")
        return full_command

    def get_command_defn(self, command) -> dict:
        log.debug(f"get_command_defn: Processing command '{command}'")
        if command in self.COMMANDS and "regex" not in self.COMMANDS[command]:
            log.debug(f"get_command_defn: Found command {command} in protocol {self._protocol_id}")
            return self.COMMANDS[command]
        for _command in self.COMMANDS:
            if "regex" in self.COMMANDS[_command] and self.COMMANDS[_command]["regex"]:
                log.debug(f"get_command_defn: Regex commands _command: {_command}")
                _re = re.compile(self.COMMANDS[_command]["regex"])
                match = _re.match(command)
                if match:
                    log.debug(
                        f"get_command_defn: Matched: {command} to: {self.COMMANDS[_command]['name']} value: {match.group(1)}"
                    )
                    self._command_value = match.group(1)
                    return self.COMMANDS[_command]
        log.info(f"get_command_defn: No command_defn found for {command}")
        return None

    def get_responses(self, response) -> list:
        """
        Default implementation of split and trim
        """
        # Trim leading '(' + trailing CRC and \r of response, then split
        if type(response) is str:
            return response[1:-3].split(" ")
        return response[1:-3].split(b" ")

    def check_response_valid(self, response) -> Tuple[bool, dict]:
        """
        Simplest validity check, CRC checks should be added to individual protocols
        """
        if response is None:
            return False, {"ERROR": ["No response", ""]}
        return True, {}

    def process_response(
        self, data_name=None, data_type=None, data_units=None, raw_value=None, frame_number=0
    ):
        template = None
        # Check for a format modifying template
        if ":" in data_type:
            data_type, template = data_type.split(":")
            log.info(f"Got template {template} for {data_name} {raw_value}")
        log.debug(
            f"Processing data_type: {data_type} for data_name: {data_name}, raw_value {raw_value}"
        )
        if data_type == "lookup":
            log.warn("lookup not implemented...")
            return data_name, None, data_units
        if data_type == "exclude" or data_type == "discard":
            # Just ignore these ones
            log.debug(f"Discarding {data_name}:{raw_value}")
            return None, raw_value, data_units
        if data_type == "option":
            response_id = int(raw_value[0])
            responses = data_units
            r = responses[response_id]
            return data_name, r, ""
        if data_type == "keyed":
            log.debug("decode: keyed defn")
            # [
            #     "keyed",
            #     1,
            #     "Command response flag",
            #     {
            #         "00": "OK",
            #         "01": "Unknown ID",
            #         "02": "Not supported",
            #         "04": "Parameter Error",
            #     },
            # ],
            key = ""
            for x in raw_value:
                key += f"{x:02x}"
            r = data_units[key]
            return data_name, r, ""
        format_string = f"{data_type}(raw_value)"
        log.debug(f"Processing format string {format_string}")
        try:
            r = eval(format_string)
        except TypeError as e:
            log.warn(f"Failed to eval format {format_string}, error: {e}")
            return data_name, format_string, data_units
        if template is not None:
            r = eval(template)
        if "{" in data_name:
            f = frame_number  # noqa: F841
            data_name = eval(data_name)
        return data_name, r, data_units

    def decode(self, response, command) -> dict:
        """
        Take the raw response and turn it into a dict of name: value, unit entries
        """

        log.info(f"decode: response passed to decode: {response}")

        valid, msgs = self.check_response_valid(response)
        if not valid:
            log.info(msgs["ERROR"][0])
            return msgs

        # Add Raw response
        _response = b""
        for item in response:
            if type(item) is int:
                _response += chr(item).encode()
            else:
                _response += item.encode()
        raw_response = _response.decode("utf-8")
        msgs["raw_response"] = [raw_response, ""]

        # Add metadata
        msgs["_command"] = command
        # Check for a stored command definition
        command_defn = self.get_command_defn(command)
        if command_defn is not None:
            msgs["_command_description"] = command_defn["description"]
            len_command_defn = len(command_defn["response"])
        else:
            # No definiution, so just return the data
            len_command_defn = 0
            log.debug(
                f"decode: No definition for command {command}, (splitted) raw response returned"
            )
            msgs["WARNING"] = [
                f"No definition for command {command} in protocol {self._protocol_id}",
                "",
            ]
            msgs["response"] = [raw_response, ""]
            return msgs

        # Split the response into individual responses
        responses = self.get_responses(response)
        log.debug(f"decode: trimmed and split responses: {responses}")

        # Determine the type of response
        if "response_type" in command_defn:
            response_type = command_defn["response_type"]
        else:
            response_type = "DEFAULT"
        log.info(f"decode: Processing response of type {response_type}")

        # Decode response based on stored command definition and type
        # process default response type
        # TODO: fix this - move into new approach
        # DEFAULT - responses are determined by the order they are returned
        if response_type == "DEFAULT":
            log.info("decode: Processing DEFAULT type responses")
            for i, result in enumerate(responses):
                # decode result
                if type(result) is bytes:
                    result = result.decode("utf-8")

                # Check if we are past the 'known' responses
                if i >= len_command_defn:
                    resp_format = ["string", f"Unknown value in response {i}", ""]
                else:
                    resp_format = command_defn["response"][i]

                # key = "{}".format(resp_format[1]).lower().replace(" ", "_")
                key = resp_format[1]
                # log.debug(f'result {result}, key {key}, resp_format {resp_format}')
                # Process results
                if result == "NAK":
                    msgs[f"WARNING{i}"] = [
                        f"Command {command} was rejected",
                        "",
                    ]
                elif resp_format[0] == "float":
                    try:
                        result = float(result)
                    except ValueError:
                        log.debug(f"Error resolving {result} as float")
                    msgs[key] = [result, resp_format[2]]
                elif resp_format[0] == "int":
                    try:
                        result = int(result)
                    except ValueError:
                        log.debug(f"Error resolving {result} as int")
                    msgs[key] = [result, resp_format[2]]
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
                        msgs[resp_format[2][j]] = [int(flag), "bool"]
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
                            # _key = "{}".format(resp_format[2][item]["name"]).lower().replace(" ", "_")
                            if resp_format[2].get(item, None):
                                _key = resp_format[2][item]["name"]
                            else:
                                _key = "unknown_{}".format(item)
                            msgs[_key] = [status, ""]
                    # msgs[key] = [output, '']
                elif resp_format[0] == "multi":
                    for x, item in enumerate(result):
                        item_value = int(item)
                        item_resp_format = resp_format[1][x]
                        item_type = item_resp_format[0]
                        # print(x, item_value, item_resp_format, item_type)
                        if item_type == "option":
                            item_name = item_resp_format[1]
                            resolved_value = item_resp_format[2][item_value]
                            msgs[item_name] = [resolved_value, ""]
                        elif item_type == "string":
                            item_name = item_resp_format[1]
                            msgs[item_name] = [item_value, ""]
                        else:
                            print(f"item type {item_type} not defined")
                elif command_defn["type"] == "SETTER":
                    # _key = "{}".format(command_defn["name"]).lower().replace(" ", "_")
                    _key = command_defn["name"]
                    msgs[_key] = [result, ""]
                else:
                    log.info(f"Processing unknown response format {result}")
                    msgs[i] = [result, ""]
            return msgs

        # Check for multiple frame type responses
        if response_type == "MULTIFRAME-POSITIONAL":
            log.debug("decode: Processing MULTIFRAME-POSITIONAL type responses")
            # MULTIFRAME-POSITIONAL - multiple frames of responses are not separated and are determined by the position in the response
            # each frame has the same definition
            frame_count = len(responses)
            log.debug(f"got {frame_count} frames")
            # the responses are the frames
            frames = responses
        else:
            frames = [responses]
            frame_count = 1

        for frame_number, frame in enumerate(frames):
            for i, response in enumerate(frame):
                if response_type == "KEYED":
                    log.debug("decode: Processing KEYED type responses")
                    # example defn ["H1", "Depth of the deepest discharge", "Ah", "mFloat"],
                    # example response data [b'H1', b'-32914']
                    if len(response) <= 1:
                        # Not enough data in response, so ignore
                        continue
                    lookup_key = response[0]
                    raw_value = response[1]
                    response_defn = get_resp_defn(lookup_key, command_defn["response"])
                    if response_defn is None:
                        # No definition for this key, so ignore???
                        log.warn(f"No definition for {response}")
                        continue
                    data_name = response_defn[1]
                    data_units = response_defn[2]
                    data_type = response_defn[3]
                elif response_type in ["POSITIONAL", "MULTIFRAME-POSITIONAL"]:
                    log.debug("decode: Processing POSITIONAL type responses")
                    # POSITIONAL - responses are not separated and are determined by the position in the response
                    # example defn :
                    #   ["discard", 1, "start flag", ""],
                    #   ["Big2ByteHex2Int", 2, "Battery Bank Voltage", "V"],
                    # example response data:
                    #   [b'\xa5', b'\x01', b'\x90', b'\x08', b'\x01\t', b'\x00\x00', b'u\xcf', b'\x03\x99', b'']
                    raw_value = response
                    # Check if we are past the 'known' responses
                    if i >= len_command_defn:
                        response_defn = ["str", f"Unknown value in response {i}", ""]
                    else:
                        response_defn = command_defn["response"][i]
                    if response_defn is None:
                        # No definition for this key, so ignore???
                        log.warn(f"No definition for {response}")
                        response_defn = ["str", f"Undefined value in response {i}", ""]
                    data_name = response_defn[2]
                    data_units = response_defn[3]
                    data_type = response_defn[0]
                # print(data_type, data_name, raw_value)

                # Process response
                data_name, value, data_units = self.process_response(
                    data_name=data_name,
                    raw_value=raw_value,
                    data_units=data_units,
                    data_type=data_type,
                    frame_number=frame_number,
                )
                # print(data_type, data_name, raw_value, value)
                if data_name is not None:
                    msgs[data_name] = [value, data_units]

        return msgs

import abc
import calendar  # noqa: F401
import logging
import re
from typing import Tuple

from ..helpers import get_resp_defn
from .protocol_helpers import BigHex2Short, BigHex2Float  # noqa: F401
from .protocol_helpers import LittleHex2Float, LittleHex2Short  # noqa: F401
from .protocol_helpers import LittleHex2UInt, LittleHex2Int  # noqa: F401
from .protocol_helpers import Hex2Ascii, Hex2Int, Hex2Str  # noqa: F401
from .protocol_helpers import uptime  # noqa: F401
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

    def list_commands(self):
        # print(f"{'Parameter':<30}\t{'Value':<15} Unit")
        if self._protocol_id is None:
            log.error("Attempted to list commands with no protocol defined")
            return {
                "ERROR": ["Attempted to list commands with no protocol defined", ""]
            }
        result = {}
        result["_command"] = "command help"
        result[
            "_command_description"
        ] = f"List available commands for protocol {str(self._protocol_id, 'utf-8')}"
        for command in self.COMMANDS:
            if "help" in self.COMMANDS[command]:
                info = (
                    self.COMMANDS[command]["description"]
                    + self.COMMANDS[command]["help"]
                )
            else:
                info = self.COMMANDS[command]["description"]
            result[command] = [info, ""]
        return result

    def get_protocol_id(self) -> bytes:
        return self._protocol_id

    def get_full_command(self, command) -> bytes:
        log.info(
            f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands"
        )
        byte_cmd = bytes(command, "utf-8")
        # calculate the CRC
        crc_high, crc_low = crc(byte_cmd)
        # combine byte_cmd, CRC , return
        full_command = byte_cmd + bytes([crc_high, crc_low, 13])
        log.debug(f"full command: {full_command}")
        return full_command

    def get_command_defn(self, command) -> dict:
        log.debug(f"Processing command '{command}'")
        if command in self.COMMANDS and "regex" not in self.COMMANDS[command]:
            log.debug(f"Found command {command} in protocol {self._protocol_id}")
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
        self,
        data_name=None,
        data_type=None,
        data_units=None,
        raw_value=None,
        frame_number=0,
    ):
        template = None
        # Check for a format modifying template
        if ":" in data_type:
            data_type, template = data_type.split(":", 1)
            log.debug(f"Got template {template} for {data_name} {raw_value}")
        log.debug(
            f"Processing data_type: {data_type} for data_name: {data_name}, raw_value {raw_value}"
        )
        if data_type == "loop":
            log.warning("loop not implemented...")
            return data_name, None, data_units
        if data_type == "exclude" or data_type == "discard" or raw_value == "extra":
            # Just ignore these ones
            log.debug(f"Discarding {data_name}:{raw_value}")
            return None, raw_value, data_units
        if data_type == "option":
            try:
                key = int(raw_value)
                r = data_units[key]
            except ValueError:
                r = f"Unable to process to int: {raw_value}"
                return None, r, ""
            except IndexError:
                r = f"Invalid option: {key}"
            return data_name, r, ""
        if data_type == "hex_option":
            key = int(raw_value[0])
            if key < len(data_units):
                r = data_units[key]
            else:
                r = f"Invalid hex_option: {key}"
            return data_name, r, ""
        if data_type == "keyed":
            log.debug("keyed defn")
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
            if key in data_units:
                r = data_units[key]
            else:
                r = f"Invalid key: {key}"
            return data_name, r, ""
        if data_type == "str_keyed":
            log.debug("str_keyed defn")
            # [
            #     "str_keyed",
            #     "Device Mode",
            #     {
            #         "B": "Inverter (Battery) Mode",
            #         "C": "PV charging Mode",
            #         "D": "Shutdown Mode",
            #         "F": "Fault Mode",
            #         "G": "Grid Mode",
            #         "L": "Line Mode",
            #         "P": "Power on Mode",
            #         "S": "Standby Mode",
            #         "Y": "Bypass Mode",
            #     },
            # ]
            key = raw_value.decode()
            if key in data_units:
                r = data_units[key]
            else:
                r = f"Invalid key: {key}"
            return data_name, r, ""
        format_string = f"{data_type}(raw_value)"
        log.debug(f"Processing format string {format_string}")
        try:
            r = eval(format_string)
        except ValueError as e:
            log.info(f"Failed to eval format {format_string} (returning 0), error: {e}")
            return data_name, 0, data_units
        except TypeError as e:
            log.warning(f"Failed to eval format {format_string}, error: {e}")
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

        log.info(f"response passed to decode: {response}")

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
            # No definition, so just return the data
            len_command_defn = 0
            log.debug(
                f"No definition for command {command}, (splitted) raw response returned"
            )
            msgs["WARNING"] = [
                f"No definition for command {command} in protocol {self._protocol_id}",
                "",
            ]
            msgs["response"] = [raw_response, ""]
            return msgs

        # Determine the type of response
        if "response_type" in command_defn:
            response_type = command_defn["response_type"]
        else:
            response_type = "DEFAULT"
        log.info(f"Processing response of type {response_type}")

        # Split the response into individual responses
        responses = self.get_responses(response)
        log.debug(f"trimmed and split responses: {responses}")

        # Decode response based on stored command definition and type
        # process default response type
        # TODO: fix this - move into new approach
        # DEFAULT - responses are determined by the order they are returned
        if response_type == "DEFAULT":
            log.info("Processing DEFAULT type responses")
            # print("Processing DEFAULT type responses")
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
                        # if flag != "" and flag != b'':
                        msgs[resp_format[2][j]] = [int(flag), "bool"]
                # eg. ['stat_flags', 'Warning status', ['Reserved', 'Inver...
                elif resp_format[0] == "stat_flags":
                    output = ""
                    for j, flag in enumerate(result):
                        # only display 'enabled' flags
                        # if flag == "1" or flag == b"1":
                        #    output = "{}\n\t- {}".format(output, resp_format[2][j])
                        # display all flags
                        key = resp_format[2][j]
                        output = flag
                        if key:  # only add msg if key is something
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
            log.debug("Processing MULTIFRAME-POSITIONAL type responses")
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
                    log.debug("Processing KEYED type responses")
                    # example defn ["V", "Main or channel 1 (battery) voltage", "V", "float:r/1000"]
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
                    # key = response_defn[0] #0
                    data_type = response_defn[3]  # 1
                    data_name = response_defn[1]  # 2
                    data_units = response_defn[2]  # 3

                elif response_type == "SEQUENTIAL":
                    log.debug("Processing SEQUENTIAL type responses")
                    # check for extra definitions...
                    extra_responses_needed = len(command_defn["response"]) - len(frame)
                    if extra_responses_needed > 0:
                        for _ in range(extra_responses_needed):
                            frame.append("extra")
                    # example ["int", "Energy produced", "Wh"]

                    # Check if we are past the 'known' responses
                    if i >= len_command_defn:
                        response_defn = ["str", f"Unknown value in response {i}", ""]
                    else:
                        response_defn = command_defn["response"][i]
                    log.debug(f"Got defn {response_defn}")
                    raw_value = response
                    # spacer = response_defn[0] #0
                    data_type = response_defn[0]  # 1
                    data_name = response_defn[1]  # 2
                    data_units = response_defn[2]  # 3

                    # print(f"{data_type=}, {data_name=}, {raw_value=}")
                elif response_type in ["POSITIONAL", "MULTIFRAME-POSITIONAL"]:
                    log.debug("Processing POSITIONAL type responses")
                    # check for extra definitions...
                    extra_responses_needed = len(command_defn["response"]) - len(frame)
                    if extra_responses_needed > 0:
                        for _ in range(extra_responses_needed):
                            frame.append("extra")
                    # POSITIONAL - responses are not separated and are determined by the position in the response
                    # example defn :
                    #   ["discard", 1, "start flag", ""],
                    #   ["BigHex2Short", 2, "Battery Bank Voltage", "V"],
                    # example response data:
                    #   [b'\xa5', b'\x01', b'\x90', b'\x08', b'\x01\t', b'\x00\x00', b'u\xcf', b'\x03\x99', b'']
                    raw_value = response
                    # Check if we are past the 'known' responses
                    if i >= len_command_defn:
                        response_defn = ["str", 1, f"Unknown value in response {i}", ""]
                    else:
                        response_defn = command_defn["response"][i]
                    if response_defn is None:
                        # No definition for this key, so ignore???
                        log.warn(f"No definition for {response}")
                        response_defn = [
                            "str",
                            1,
                            f"Undefined value in response {i}",
                            "",
                        ]
                    log.debug(f"Got defn {response_defn}")
                    # length = response_defn[1] #0
                    data_type = response_defn[0]  # 1
                    data_name = response_defn[2]  # 2
                    data_units = response_defn[3]  # 3

                # Check for lookup
                if data_type.startswith("lookup"):
                    log.debug("processing lookup...")
                    log.info(
                        f"Processing data_type: '{data_type}' for data_name: '{data_name}', raw_value '{raw_value}'"
                    )
                    m = msgs
                    template = data_type.split(":", 1)[1]
                    log.debug(f"Got template {template} for {data_name} {raw_value}")
                    lookup = eval(template)
                    log.debug(f"looking up values for: {lookup}")
                    value, data_units = m[lookup]
                elif data_type.startswith("info"):
                    log.debug("processing info...")
                    # print(
                    #    f"Processing {data_type=} for {data_name=}, {data_units=} {response=} {command=} {self._command_value=}"
                    # )
                    template = data_type.split(":", 1)[1]
                    # Provide cv as shortcut to self._command_value for info fields
                    cv = self._command_value  # noqa: F841
                    value = eval(template)
                else:
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
            # print(f"{i=} {response=} {len(command_defn['response'])}")

        return msgs

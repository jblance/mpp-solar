import logging
from typing import Tuple

from .abstractprotocol import AbstractProtocol
from .protocol_helpers import crc8 as dalyChecksum

# from .pi30 import COMMANDS

log = logging.getLogger("daly")

# (AAA BBB CCC DDD EEE
# (000 001 002 003 004

COMMANDS = {
    "SOC": {
        "name": "SOC",
        "description": "State of Charge",
        "help": " -- display the battery state of charge",
        "type": "DALY",
        "command_code": "90",
        "response_type": "POSITIONAL",
        "response": [
            ["discard", 1, "start flag", ""],
            ["discard", 1, "module address", ""],
            ["discard", 1, "command id", ""],
            ["discard", 1, "data length", ""],
            ["BigHex2Short:r/10", 2, "Battery Bank Voltage", "V"],
            ["BigHex2Short:r/10", 2, "acquistion", "V"],
            ["BigHex2Short:(r-30000)/10", 2, "Current", "A"],
            ["BigHex2Short:r/10", 2, "SOC", "%"],
            ["discard", 1, "checksum", ""],
        ],
        "test_responses": [
            b"\xa5\x01\x90\x08\x02\x10\x00\x00uo\x03\xbc\xf3",
            b"\xa5\x01\x90\x08\x02\x14\x00\x00uE\x03x\x89",
            b"\xa5\x01\x90\x08\x01\t\x00\x00u\xcf\x03\n\x99",
        ],
    },
    "cellMinMaxVoltages": {
        "name": "cellMinMaxVoltages",
        "description": "Cell Minimum and Maximum Voltages",
        "help": " -- display the cell number and voltage of the cells with the min and max voltages",
        "type": "DALY",
        "command_code": "91",
        "response_type": "POSITIONAL",
        "response": [
            ["discard", 1, "start flag", ""],
            ["discard", 1, "module address", ""],
            ["discard", 1, "command id", ""],
            ["discard", 1, "data length", ""],
            ["BigHex2Short:r/1000", 2, "Maximum Cell Voltage", "V"],
            ["Hex2Int", 1, "Maximum Cell Number", ""],
            ["BigHex2Short:r/1000", 2, "Minimum Cell Voltage", "V"],
            ["Hex2Int", 1, "Minimum Cell Number", ""],
            ["discard", 2, "SOC", "%"],
            ["discard", 1, "checksum", ""],
        ],
        "test_responses": [
            b"\xa5\x01\x91\x08\r\x00\x0f\x0c\xfe\x01\x03x\xe1",
        ],
    },
    "cellMinMaxTemps": {
        "name": "cellMinMaxTemps",
        "description": "Cell Minimum and Maximum Temperatures",
        "help": " -- display the cell number and temperature of the cells with the min and max temperatures",
        "type": "DALY",
        "command_code": "92",
        "response_type": "POSITIONAL",
        "response": [
            ["discard", 1, "start flag", ""],
            ["discard", 1, "module address", ""],
            ["discard", 1, "command id", ""],
            ["discard", 1, "data length", ""],
            ["Hex2Int:r-40", 1, "Maximum Cell Temperature", "°C"],
            ["Hex2Int", 1, "Maximum Cell Number", ""],
            ["Hex2Int:r-40", 1, "Minimum Cell Temperature", "°C"],
            ["Hex2Int", 1, "Minimum Cell Number", ""],
            ["discard", 2, "not used", ""],
            ["discard", 2, "SOC", "%"],
            ["discard", 1, "checksum", ""],
        ],
        "test_responses": [b"\xa5\x01\x92\x087\x017\x01\xfe\x01\x03x*"],
    },
    "mosStatus": {
        "name": "mosStatus",
        "description": "mosStatus",
        "help": " -- display the mosStatus",
        "type": "DALY",
        "command_code": "93",
        "response_type": "POSITIONAL",
        "response": [
            ["discard", 1, "start flag", ""],
            ["discard", 1, "module address", ""],
            ["discard", 1, "command id", ""],
            ["discard", 1, "data length", ""],
            ["hex_option", 1, "Charge Status", ["stationary", "charged", "discharged"]],
            ["Hex2Str", 1, "Charging MOS Tube Status", ""],
            ["Hex2Str", 1, "Discharging MOS Tube Status", ""],
            ["Hex2Int", 1, "BMS Life", "cycles"],
            ["BigHex2Float:r/1000", 4, "Residual Capacity", "AH"],
            ["discard", 1, "checksum", ""],
        ],
        "test_responses": [
            b"\xa5\x01\x93\x08\x02\x01\x01x\x00\x03\xcb@\xcb",
            b"\xa5\x01\x93\x08\x00\x01\x01\x9a\x00\x02\xa2\xd8Y",
        ],
    },
    "status": {
        "name": "status",
        "description": "Status Information",
        "help": " -- display the status information",
        "type": "DALY",
        "command_code": "94",
        "response_type": "POSITIONAL",
        "response": [
            ["discard", 1, "start flag", ""],
            ["discard", 1, "module address", ""],
            ["discard", 1, "command id", ""],
            ["discard", 1, "data length", ""],
            ["Hex2Int", 1, "Number of Cells", ""],
            ["Hex2Int", 1, "Number of Temperature Sensors", ""],
            ["hex_option", 1, "Charger Status", ["disconnected", "connected"]],
            ["hex_option", 1, "Load Status", ["disconnected", "connected"]],
            ["Hex2Str", 1, "Flags (TODO)", ""],
            ["BigHex2Short", 2, "Charge/Discharge Cycles", "cycles"],
            ["Hex2Str", 1, "Reserved", ""],
            ["discard", 1, "checksum", ""],
        ],
        "test_responses": [
            b"\xa5\x01\x94\x08\x10\x01\x00\x00\x00\x00\x03@\x96",
        ],
    },
    "cellVoltages": {
        "name": "cellVoltages",
        "description": "Cell Voltages Information",
        "help": " -- display the cell voltages",
        "type": "DALY",
        "command_code": "95",
        "response_type": "MULTIFRAME-POSITIONAL",
        "response_length": 13,
        "response": [
            ["discard", 1, "start flag", ""],
            ["discard", 1, "module address", ""],
            ["discard", 1, "command id", ""],
            ["discard", 1, "data length", ""],
            ["discard", 1, "f'Frame Number {f:02d}'", ""],
            ["BigHex2Short:r/1000", 2, "f'Cell {3*f+1:02d} Voltage'", "V"],
            ["BigHex2Short:r/1000", 2, "f'Cell {3*f+2:02d} Voltage'", "V"],
            ["BigHex2Short:r/1000", 2, "f'Cell {3*f+3:02d} Voltage'", "V"],
            ["discard", 1, "Reserved", ""],
            ["discard", 1, "checksum", ""],
        ],
        "test_responses": [
            b"\xa5\x01\x95\x08\x01\x0c\xfd\x0c\xfe\x0c\xfe@\xa1\xa5\x01\x95\x08\x02\x0c\xfe\x0c\xfe\x0c\xfe@\xa3\xa5\x01\x95\x08\x03\x0c\xfe\x0c\xfe\x0c\xfe@\xa4\xa5\x01\x95\x08\x04\x0c\xfe\x0c\xfc\x0c\xfe@\xa3\xa5\x01\x95\x08\x05\x0c\xfe\x0c\xff\x0c\xfe@\xa7\xa5\x01\x95\x08\x06\x0c\xfc\x00\x00\x00\x00@\x91\xa5\x01\x95\x08\x07\x00\x00\x00\x00\x00\x00@\x8a\xa5\x01\x95\x08\x08\x00\x00\x00\x00\x00\x00@\x8b\xa5\x01\x95\x08\t\x00\x00\x00\x00\x00\x00@\x8c\xa5\x01\x95\x08\n\x00\x00\x00\x00\x00\x00@\x8d\xa5\x01\x95\x08\x0b\x00\x00\x00\x00\x00\x00@\x8e\xa5\x01\x95\x08\x0c\x00\x00\x00\x00\x00\x00@\x8f\xa5\x01\x95\x08\r\x00\x00\x00\x00\x00\x00@\x90\xa5\x01\x95\x08\x0e\x00\x00\x00\x00\x00\x00@\x91\xa5\x01\x95\x08\x0f\x00\x00\x00\x00\x00\x00@\x92\xa5\x01\x95\x08\x10\x00\x00\x00\x00\x00\x00@\x93",
            b"\xa5\x01\x95\x08\x01\x0c\xa3\x0c\xa7\x0c\xa6\xf9Q\xa5\x01\x95\x08\x02\x0c\xa8\x0c\xa5\x0c\xa4\xf9S\xa5\x01\x95\x08\x03\x0c\xa5\x0c\xa6\x00\x00\xf9\xa2\xa5\x01\x95\x08\x04\x00\x00\x00\x00\x00\x00\xf9@\xa5\x01\x95\x08\x05\x00\x00\x00\x00\x00\x00\xf9A\xa5\x01\x95\x08\x06\x00\x00\x00\x00\x00\x00\xf9B\xa5\x01\x95\x08\x07\x00\x00\x00\x00\x00\x00\xf9C\xa5\x01\x95\x08\x08\x00\x00\x00\x00\x00\x00\xf9D\xa5\x01\x95\x08\t\x00\x00\x00\x00\x00\x00\xf9E\xa5\x01\x95\x08\n\x00\x00\x00\x00\x00\x00\xf9F\xa5\x01\x95\x08\x0b",
        ],
    },
    "cellTemperatures": {
        "name": "cellTemperatures",
        "description": "Cell Temperature Information",
        "help": " -- display the cell temperatures",
        "type": "DALY",
        "command_code": "96",
        "response_type": "MULTIFRAME-POSITIONAL",
        "response_length": 13,
        "response": [
            ["discard", 1, "start flag", ""],
            ["discard", 1, "module address", ""],
            ["discard", 1, "command id", ""],
            ["discard", 1, "data length", ""],
            ["discard", 1, "f'Frame Number {f:02d}'", ""],
            ["Hex2Int:r-40", 1, "f'Cell {7*f+1:02d} Temperature'", "°C"],
            ["Hex2Int:r-40", 1, "f'Cell {7*f+2:02d} Temperature'", "°C"],
            ["Hex2Int:r-40", 1, "f'Cell {7*f+3:02d} Temperature'", "°C"],
            ["Hex2Int:r-40", 1, "f'Cell {7*f+4:02d} Temperature'", "°C"],
            ["Hex2Int:r-40", 1, "f'Cell {7*f+5:02d} Temperature'", "°C"],
            ["Hex2Int:r-40", 1, "f'Cell {7*f+6:02d} Temperature'", "°C"],
            ["Hex2Int:r-40", 1, "f'Cell {7*f+7:02d} Temperature'", "°C"],
            ["discard", 1, "checksum", ""],
        ],
        "test_responses": [
            b"\xa5\x01\x96\x08\x017\x00\x00\x00\x00\x00\x00|\xa5\x01\x96\x08\x02\x00\x00\x00\x00\x00\x00\x00F",
        ],
    },
}
startFlag = bytes.fromhex("A5")


class daly(AbstractProtocol):
    """
    DALY - Daly BMS protocol handler
    """

    def __str__(self):
        return "Daly BMS protocol handler"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"DALY"
        self.module_address = bytes.fromhex("80")
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = [
            "SOC",
        ]
        self.SETTINGS_COMMANDS = [
            "",
        ]
        self.DEFAULT_COMMAND = "SOC"

    def get_full_command(self, command) -> bytes:
        """
        Override the default get_full_command as its different
        """
        log.info(
            f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands"
        )
        # These need to be set to allow other functions to work`
        self._command = command
        self._command_defn = self.get_command_defn(command)
        # End of required variables setting
        if self._command_defn is None:
            return None

        # DALY
        # startFlag = bytes.fromhex("A5")
        commandID = bytes.fromhex(self._command_defn["command_code"])
        dataLength = bytes.fromhex("08")
        data = bytes.fromhex("00" * 8)
        cmd = startFlag + self.module_address + commandID + dataLength + data

        checksum = f"{dalyChecksum(cmd):02X}"
        cmd = cmd + bytes.fromhex(checksum) + b"\n"
        log.debug(f"full command: {cmd}")
        return cmd

    def is_multiframe(self, response) -> bool:
        # startFlag = bytes.fromhex("A5")
        if (
            "response_length" in self._command_defn
            and len(response) > self._command_defn["response_length"]
        ):
            return True
        return False

    def check_response_valid(self, response) -> Tuple[bool, dict]:
        """
        DALY protocol - checksum is sum of bytes
        """
        log.debug(f"checking validity of {response}")
        if not response:
            return False, {"validity check": ["Error: Response was empty", ""]}

        # Check to see if the response is a multi frame response
        if self.is_multiframe(response):
            log.info("is multiframe response - assuming ok for now")
            # TODO: fix check_response_valid for multiframe results
            return True, {}

        _r = response
        # print(f"bytes response {_r}")
        data = _r[:-1]
        checksum = _r[-1:][0]
        if dalyChecksum(data) == checksum:
            log.debug(
                f"DALY Checksum matches response '{response}' checksum:{checksum}"
            )
            return True, {}
        else:
            # print("VED Hex Checksum does not match")
            return False, {
                "validity check": [
                    f"Error: DALY checksum did not match for response {response}",
                    "",
                ]
            }

    def get_responses(self, response):
        """
        Override the default get_responses as its different
        """
        responses = []
        # remove \n
        # response = response.replace(b"\n", b"")

        if (
            self._command_defn is not None
            and self._command_defn["response_type"] == "MULTIFRAME-POSITIONAL"
        ):
            # Have multiple frames of positional data
            # Split into frames
            frame_size = self._command_defn["response_length"]
            frames = [
                response[i : i + frame_size]
                for i in range(0, len(response), frame_size)
            ]
            log.info(f"Multi frame response with {len(frames)} frames")
            # Loop through each frame and process as per definition
            for frame in frames:
                if len(frame) == 0:
                    continue
                items = []
                for defn in self._command_defn["response"]:
                    size = defn[1]
                    item = frame[:size]
                    items.append(item)
                    frame = frame[size:]
                responses.append(items)
            # print(responses)
            return responses

        if (
            self._command_defn is not None
            and self._command_defn["response_type"] == "POSITIONAL"
        ):
            # Have a POSITIONAL type response, so need to break it up...
            # example defn :
            # "response": [
            #   ["discard", 1, "start flag", ""],
            #   ["discard", 1, "module address", ""],
            #   ["discard", 1, "command id", ""],
            #   ["discard", 1, "data length", ""],
            # ]
            # example response data b"\xa5\x01\x90\x08\x02\x10\x00\x00uo\x03\xbc\xf3",
            for defn in self._command_defn["response"]:
                size = defn[1]
                item = response[:size]
                responses.append(item)
                response = response[size:]
            return responses
        else:
            return bytearray(response)

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
            ["Big2ByteHex2Int:r/10", 2, "Battery Bank Voltage", "V"],
            ["Big2ByteHex2Int:r/10", 2, "acquistion", "V"],
            ["Big2ByteHex2Int:(r-30000)/10", 2, "Current", "A"],
            ["Big2ByteHex2Int:r/10", 2, "SOC", "%"],
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
            ["Big2ByteHex2Int:r/1000", 2, "Maximum Cell Voltage", "V"],
            ["Hex2Int", 1, "Maximum Cell Number", ""],
            ["Big2ByteHex2Int:r/1000", 2, "Minimum Cell Voltage", "V"],
            ["Hex2Int", 1, "Minimum Cell Number", ""],
            ["Big2ByteHex2Int:r/10", 2, "SOC", "%"],
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
            ["Big2ByteHex2Int:r/10", 2, "SOC", "%"],
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
            ["option", 1, "Charge Status", ["stationary", "charged", "discharged"]],
            ["Hex2Str", 1, "Charging MOS Tube Status", ""],
            ["Hex2Str", 1, "Discharging MOS Tube Status", ""],
            ["Hex2Int", 1, "BMS Life", "cycles"],
            ["Hex2Str", 4, "Residual Capacity (TODO)", "(HEX) mAH"],
            ["discard", 1, "checksum", ""],
        ],
        "test_responses": [b"\xa5\x01\x93\x08\x02\x01\x01x\x00\x03\xcb@\xcb"],
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
            ["Hex2Str", 1, "Battery String", ""],
            ["Hex2Str", 1, "Temperature", ""],
            ["option", 1, "Charger Status", ["disconnected", "connected"]],
            ["option", 1, "Load Status", ["disconnected", "connected"]],
            ["Hex2Str", 1, "Flags (TODO)", ""],
            ["Big2ByteHex2Int", 2, "Charge/Discharge Cycles", "cycles"],
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
            ["Big2ByteHex2Int:r/1000", 2, "f'Cell {3*f+1:02d} Voltage'", "V"],
            ["Big2ByteHex2Int:r/1000", 2, "f'Cell {3*f+2:02d} Voltage'", "V"],
            ["Big2ByteHex2Int:r/1000", 2, "f'Cell {3*f+3:02d} Voltage'", "V"],
            ["discard", 1, "Reserved", ""],
            ["discard", 1, "checksum", ""],
        ],
        "test_responses": [
            b"\xa5\x01\x95\x08\x01\x0c\xfd\x0c\xfe\x0c\xfe@\xa1\xa5\x01\x95\x08\x02\x0c\xfe\x0c\xfe\x0c\xfe@\xa3\xa5\x01\x95\x08\x03\x0c\xfe\x0c\xfe\x0c\xfe@\xa4\xa5\x01\x95\x08\x04\x0c\xfe\x0c\xfc\x0c\xfe@\xa3\xa5\x01\x95\x08\x05\x0c\xfe\x0c\xff\x0c\xfe@\xa7\xa5\x01\x95\x08\x06\x0c\xfc\x00\x00\x00\x00@\x91\xa5\x01\x95\x08\x07\x00\x00\x00\x00\x00\x00@\x8a\xa5\x01\x95\x08\x08\x00\x00\x00\x00\x00\x00@\x8b\xa5\x01\x95\x08\t\x00\x00\x00\x00\x00\x00@\x8c\xa5\x01\x95\x08\n\x00\x00\x00\x00\x00\x00@\x8d\xa5\x01\x95\x08\x0b\x00\x00\x00\x00\x00\x00@\x8e\xa5\x01\x95\x08\x0c\x00\x00\x00\x00\x00\x00@\x8f\xa5\x01\x95\x08\r\x00\x00\x00\x00\x00\x00@\x90\xa5\x01\x95\x08\x0e\x00\x00\x00\x00\x00\x00@\x91\xa5\x01\x95\x08\x0f\x00\x00\x00\x00\x00\x00@\x92\xa5\x01\x95\x08\x10\x00\x00\x00\x00\x00\x00@\x93",
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

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"DALY"
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
        Override the default get_full_command as its different for DALY
        """
        log.info(
            f"get_full_command: Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands"
        )
        # These need to be set to allow other functions to work`
        self._command = command
        self._command_defn = self.get_command_defn(command)
        # End of required variables setting
        if self._command_defn is None:
            return None

        # DALY
        # startFlag = bytes.fromhex("A5")
        moduleAddress = bytes.fromhex("80")
        commandID = bytes.fromhex(self._command_defn["command_code"])
        dataLength = bytes.fromhex("08")
        data = bytes.fromhex("00" * 8)
        cmd = startFlag + moduleAddress + commandID + dataLength + data

        checksum = f"{dalyChecksum(cmd):02X}"
        cmd = cmd + bytes.fromhex(checksum) + b"\n"
        log.debug(f"get_full_command: full command: {cmd}")
        return cmd

    def is_multiframe(self, response) -> bool:
        # startFlag = bytes.fromhex("A5")
        if response.count(startFlag) > 1:
            return True
        return False

    def check_response_valid(self, response) -> Tuple[bool, dict]:
        """
        DALY protocol - checksum is sum of bytes
        """
        if not response:
            return False, {"ERROR": ["No response", ""]}

        log.debug(f"checking validity of {response}")

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
            log.debug(f"DALY Checksum matches response '{response}' checksum:{checksum}")
            return True, {}
        else:
            # print("VED Hex Checksum does not match")
            return False, {"ERROR": [f"DALY checksum did not match for response {response}", ""]}

    def get_responses(self, response):
        """
        Override the default get_responses as its different
        """
        responses = []
        # remove \n
        response = response.replace(b"\n", b"")

        if (
            self._command_defn is not None
            and self._command_defn["response_type"] == "MULTIFRAME-POSITIONAL"
        ):
            # Have multiple frames of positional data
            # Either 1a:Split into frames?,
            # 1b: Then split frames into responses?
            # 2: Or combine frames into jumbo frame?
            _response = response.replace(startFlag, b"#%s" % startFlag)
            # Ignore the first # as dont want to split there anyway (creates an empty frame)
            frames = _response[1:].split(b"#")
            log.info(f"Multi frame response with {len(frames)} frames")
            #
            # TODO: so now what????
            for frame in frames:
                items = []
                for defn in self._command_defn["response"]:
                    size = defn[1]
                    item = frame[:size]
                    items.append(item)
                    frame = frame[size:]
                responses.append(items)
            return responses

        if self._command_defn is not None and self._command_defn["response_type"] == "POSITIONAL":
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

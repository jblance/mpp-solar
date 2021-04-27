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
            ["2dInt", 2, "pressure", "V"],
            ["2dInt", 2, "acquistion", "V"],
            ["2dInt-30k", 2, "current", "A"],
            ["2dInt", 2, "SOC", "%"],
            ["discard", 1, "checksum", ""],
        ],
        "test_responses": [
            # bytes.fromhex("A58090080000000000000000bd\n"),
            # b'\xa5\x01\x90\x08\x02\x10\x00\x00uo\x03\xbc\xf3',
            b"\xa5\x01\x90\x08\x02\x14\x00\x00uE\x03x\x89",
        ],
    },
    "cellMinMax": {
        "name": "cellMinMax",
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
            ["2mInt", 2, "Maximum Cell Voltage", "V"],
            ["int", 1, "Maximum Cell Number", ""],
            ["2mInt", 2, "Minimum Cell Voltage", "V"],
            ["int", 1, "Minimum Cell Number", ""],
            ["2dInt", 2, "SOC", "%"],
            ["discard", 1, "checksum", ""],
        ],
        "test_responses": [
            b"\xa5\x01\x91\x08\r\x00\x0f\x0c\xfe\x01\x03x\xe1",
        ],
    },
    "cellTemperatures": {
        "name": "cellTemperatures",
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
            ["int-40", 1, "Maximum Cell Temperature", "°C"],
            ["int", 1, "Maximum Cell Number", ""],
            ["int-40", 1, "Minimum Cell Temperature", "°C"],
            ["int", 1, "Minimum Cell Number", ""],
            ["hex", 2, "not used", ""],
            ["2dInt", 2, "SOC", "%"],
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
            ["hex", 1, "Charging MOS Tube Status", ""],
            ["hex", 1, "Discharging MOS Tube Status", ""],
            ["int", 1, "BMS Life", "cycles"],
            ["hex", 4, "Residual Capacity (TODO)", "(HEX) mAH"],
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
            ["hex", 1, "Battery String", ""],
            ["hex", 1, "Temperature", ""],
            ["option", 1, "Charger Status", ["disconnected", "connected"]],
            ["option", 1, "Load Status", ["disconnected", "connected"]],
            ["hex", 1, " Flags (TODO)", ""],
            ["2int", 2, "Charge/Discharge Cycles", "cycles"],
            ["hex", 1, "Reserved", ""],
            ["discard", 1, "checksum", ""],
        ],
        "test_responses": [
            b"\xa5\x01\x94\x08\x10\x01\x00\x00\x00\x00\x03@\x96",
        ],
    },
}


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
        startFlag = bytes.fromhex("A5")
        moduleAddress = bytes.fromhex("80")
        commandID = bytes.fromhex(self._command_defn["command_code"])
        # commandID = bytes.fromhex("90")
        dataLength = bytes.fromhex("08")
        data = bytes.fromhex("00" * 8)
        cmd = startFlag + moduleAddress + commandID + dataLength + data

        checksum = f"{dalyChecksum(cmd):02X}"
        cmd = cmd + bytes.fromhex(checksum) + b"\n"
        log.debug(f"get_full_command: full command: {cmd}")
        return cmd

    def check_response_valid(self, response) -> Tuple[bool, dict]:
        """
        DALY protocol - checksum is sum of bytes
        """
        if not response:
            return False, {"ERROR": ["No response", ""]}
        # HEX protocol response
        log.debug(f"checking validity of {response}")

        # _r = response.split(b":")[1][:-1].decode()
        # print(f"trimmed response {_r}")
        # _r = f"0{_r}"
        # print(f"padded response {_r}")
        # _r = bytes.fromhex(response)
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
                "ERROR": [f"DALY checksum did not match for response {response}", ""]
            }

    def get_responses(self, response):
        """
        Override the default get_responses as its different for PI00
        """
        # remove \n
        response = response.replace(b"\n", b"")
        responses = []
        for r in response:
            responses.append(r)
        return bytearray(responses)

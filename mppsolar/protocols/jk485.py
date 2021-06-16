import logging

from .jkabstractprotocol import jkAbstractProtocol
from .protocol_helpers import crc8


log = logging.getLogger("jk485")


# Request balancer data
# 55 AA 01 FF 00 00 FF
# frame header  0x55 0xaa
# slave address 0x01
# command code  0xff
# frame data    0x0000
# checksum      0xff

COMMANDS = {
    "getBalancerData": {
        "name": "getBalancerData",
        "command_code": "FF",
        "description": "Get Balancer Data",
        "help": " -- Get Balancer Data",
        "type": "QUERY",
        "checksum_required": "True",
        "response_type": "POSITIONAL",
        "response": [
            ["Hex2Str", 2, "Header", ""],
            ["Hex2Str", 1, "Slave Address", ""],
            ["Hex2Str", 1, "Command Code", ""],
            ["BigHex2Short:r/100", 2, "Total Battery Voltage", "V"],
            ["BigHex2Short:r/1000", 2, "Average Cell Voltage", "V"],
            ["Hex2Int", 1, "Number of Cells", ""],
            ["Hex2Int", 1, "Highest Cell", ""],
            ["Hex2Int", 1, "Lowest Cell", ""],
            ["Hex2Str", 1, "Charging / Discharging", ""],
            ["Hex2Str", 1, "Alarm - todo", ""],
            ["BigHex2Short:r/1000", 2, "Voltage Difference", "V"],
            ["BigHex2Short:r/1000", 2, "Balance Current", "A"],
            ["BigHex2Short:r/1000", 2, "Balance Trigger Voltage", "V"],
            ["BigHex2Short:r/1000", 2, "Max Balance Current", "A"],
            ["Hex2Str", 1, "Balance On / Off", ""],
            ["Hex2Int", 1, "Set Number of Cells", ""],
            ["BigHex2Short:r/1000", 2, "Voltage Cell01", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell02", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell03", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell04", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell05", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell06", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell07", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell08", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell09", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell10", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell11", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell12", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell13", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell14", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell15", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell16", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell17", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell18", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell19", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell20", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell21", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell22", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell23", "V"],
            ["BigHex2Short:r/1000", 2, "Voltage Cell24", "V"],
            ["BigHex2Short", 2, "Temperature", "°C"],
            ["Hex2Str", 1, "Checksum", ""],
        ],
        "test_responses": [
            bytes.fromhex(
                "EB 90 01 FF 1E D3 0F 69 14 13 02 00 00 00 07 00 00 00 05 03 E8 01 14 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 00 16 6F"
            ),
        ],
    },
}


class jk485(jkAbstractProtocol):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"JK485"
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = [
            "getBalancerData",
        ]
        self.SETTINGS_COMMANDS = [
            "",
        ]
        self.DEFAULT_COMMAND = "getBalancerData"

    def get_full_command(self, command) -> bytes:
        """
        Override the default get_full_command as its different for JK485
        """
        log.info(f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands")
        # These need to be set to allow other functions to work`
        self._command = command
        self._command_defn = self.get_command_defn(command)
        # End of required variables setting
        if self._command_defn is None:
            # Maybe return a default here?
            return None
        if "command_code" in self._command_defn:
            # full command is 7 bytes long
            cmd = bytearray(7)
            # 55 AA 01 FF 00 00 FF
            # frame header  0x55 0xaa
            cmd[0:2] = bytes.fromhex("55aa")
            log.debug(f"cmd with header: {cmd}")
            # slave address 0x01
            cmd[2] = 0x01
            log.debug(f"cmd with header + slave address: {cmd}")
            # command code  0xff
            cmd[3] = int(self._command_defn["command_code"], 16)
            # frame data    0x0000
            cmd[4:6] = bytes.fromhex("0000")
            log.debug(f"cmd with command code and frame data: {cmd}")
            # checksum      0xff
            cmd[-1] = crc8(cmd)
            log.debug(f"cmd with crc: {cmd}")
            return cmd

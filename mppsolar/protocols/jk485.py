import logging

from .jkabstractprotocol import jkAbstractProtocol
from .protocol_helpers import crc8


log = logging.getLogger("MPP-Solar")


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
        "response": [
            ["hex", 2, "Header", ""],
            ["hex", 1, "Slave Address", ""],
            ["hex", 1, "Command Code", ""],
            ["16Int100", 1, "Total Battery Voltage", "V"],
            ["16Int1000", 1, "Average Cell Voltage", "V"],
            ["int", 1, "Number of Cells", ""],
            ["int", 1, "Highest Cell", ""],
            ["int", 1, "Lowest Cell", ""],
            ["hex", 1, "Charging / Discharging", ""],
            ["hex", 1, "Alarm - todo", ""],
            ["16Int1000", 1, "Voltage Difference", "V"],
            ["16Int1000", 1, "Balance Current", "A"],
            ["16Int1000", 1, "Balance Trigger Voltage", "V"],
            ["16Int1000", 1, "Max Balance Current", "A"],
            ["hex", 1, "Balance On / Off", ""],
            ["int", 1, "Set Number of Cells", ""],
            ["loop", 24, "Voltage Cell", "V", "16Int1000"],
            ["16Int", 1, "Temperature", "°C"],
            ["hex", 1, "Checksum", ""],
            ["rem"],
        ],
        "test_responses": [
            bytes.fromhex(
                "EB 90 01 FF 1E D3 0F 69 14 13 02 00 00 00 07 00 00 00 05 03 E8 01 14 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 00 16 6F"
            ),
        ],
        "regex": "",
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

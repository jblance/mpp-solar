import logging

from .protocol import AbstractProtocol
from .protocol_helpers import decode4ByteHex, crc8


log = logging.getLogger("MPP-Solar")

# >>> print(f'{151:#04x}')
# 0x97
# >>> print(f'{1:#04x}')
# 0x01
# >>> print(f'{1:#02x}')
# 0x1
# >>> print(f'{1:#04x}')
# 0x01
# >>> bytes.fromhex('aa5590eb')
# b'\xaaU\x90\xeb'
# getInfo = b'\xaa\x55\x90\xeb\x97\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11'
# getCellInfo = b'\xaa\x55\x90\xeb\x96\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10'

COMMANDS = {
    "getInfo": {
        "name": "getInfo",
        "command_code": "97",
        "description": "BLE Device Information inquiry",
        "help": " -- queries the ble device information",
        "type": "QUERY",
        "response": [
            ["offset", "" "Protocol Version", ""],
        ],
        "test_responses": [
            b"",
        ],
        "regex": "",
    },
}


class jk04(AbstractProtocol):
    """
    JK04 - Handler for JKBMS 4 byte data communication
         - e.g. ASASASAS = ??V
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"JK04"
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = [
            "",
        ]
        self.SETTINGS_COMMANDS = [
            "getInfo",
        ]
        self.DEFAULT_COMMAND = "getInfo"

    def get_full_command(self, command) -> bytes:
        """
        Override the default get_full_command as its different for JK04
        # getInfo = b'\xaa\x55\x90\xeb\x97\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11'
        """
        log.info(
            f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands"
        )
        # These need to be set to allow other functions to work`
        self._command = command
        self._command_defn = self.get_command_defn(command)
        # End of required variables setting
        if self._command_defn is None:
            # Maybe returna default here?
            return None
        if "command_code" in self._command_defn:
            # full command is 20 bytes long
            cmd = bytearray(20)
            # starts with \xaa\x55\x90\xeb
            cmd[0:4] = bytes.fromhex("aa5590eb")
            log.debug(f"cmd with SOR: {cmd}")
            # then has command code
            cmd[4] = int(self._command_defn["command_code"], 16)
            log.debug(f"cmd with command code: {cmd}")
            cmd[-1] = crc8(cmd)
            log.debug(f"cmd with crc: {cmd}")
            return cmd
        return None

    def get_responses(self, response):
        """
        Override the default get_responses as its different for JK04
        """
        responses = response.split(b" ")
        # Trim leading '(' of first response
        responses[0] = responses[0][1:]
        # Remove CRC and \r of last response
        responses[-1] = responses[-1][:-3]
        return responses

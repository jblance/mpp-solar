import logging

from .abstractprotocol import AbstractProtocol
from .protocol_helpers import crcPI as crc

# from .pi30 import COMMANDS

log = logging.getLogger("pi17")

COMMANDS = {
    "PI": {
        "name": "PI",
        "prefix": "^P003",
        "description": "Device Protocol Version inquiry",
        "help": " -- queries the device protocol version",
        "type": "QUERY",
        "response": [["string", "Protocol Version", ""]],
        "test_responses": [
            b"",
        ],
    },
}


class pi17(AbstractProtocol):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI17"
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = []
        self.SETTINGS_COMMANDS = [
            "PI",
        ]
        self.DEFAULT_COMMAND = "PI"

    def get_full_command(self, command) -> bytes:
        """
        Override the default get_full_command as its different
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

        _cmd = bytes(self._command, "utf-8")
        _type = self._command_defn["type"]

        # No CRC in PI17 commands?
        data_length = len(_cmd) + 1
        if _type == "QUERY":
            _prefix = f"^P{data_length:03}"
        else:
            _prefix = f"^S{data_length:03}"
        _pre_cmd = bytes(_prefix, "utf-8") + _cmd
        log.debug(f"get_full_command: _pre_cmd: {_pre_cmd}")
        # calculate the CRC
        crc_high, crc_low = crc(_pre_cmd)
        # combine byte_cmd, CRC , return
        # PI18 full command "^P005GS\x..\x..\r"
        # _crc = bytes([crc_high, crc_low, 13])
        full_command = _pre_cmd + bytes([13])  # + _crc
        log.debug(f"get_full_command: full command: {full_command}")
        return full_command

    def get_responses(self, response):
        """
        Override the default get_responses as its different
        """
        responses = response.split(b",")
        if responses[0] == b"^0\x1b\xe3\r":
            # is a reject response
            return ["NAK"]

        # Drop ^Dxxx from first response
        responses[0] = responses[0][5:]
        # Remove CRC of last response
        responses[-1] = responses[-1][:-3]
        return responses

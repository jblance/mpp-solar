import logging

from .protocol import AbstractProtocol

# from .pi30 import COMMANDS

log = logging.getLogger("MPP-Solar")

# (AAA BBB CCC DDD EEE
# (000 001 002 003 004

COMMANDS = {
    "QPI": {
        "name": "QPI",
        "description": "Device Protocol Version inquiry",
        "help": " -- queries the device protocol version",
        "type": "QUERY",
        "response": [["string", "Protocol Version", ""]],
        "test_responses": [
            b"(PI00\r",
        ],
        "regex": "",
    },
}


class pi00(AbstractProtocol):
    """
    PI00 - test protocol handler
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI00"
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = [
            "",
        ]
        self.SETTINGS_COMMANDS = [
            "QPI",
        ]
        self.DEFAULT_COMMAND = "QPI"

    def get_full_command(self, command) -> bytes:
        """
        Override the default get_full_command as its different for PI00
        """
        log.info(
            f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands"
        )
        # These need to be set to allow other functions to work`
        self._command = command
        self._command_defn = self.get_command_defn(command)
        # End of required variables setting
        cmd = bytes(self._command, "utf-8")
        # combine byte_cmd, return
        full_command = cmd + bytes([13])
        log.debug(f"full command: {full_command}")
        return full_command

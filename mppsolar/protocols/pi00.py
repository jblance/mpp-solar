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
            b"(PI00\x42\x42\r",
        ],
        "regex": "",
    },
    "QPIRI": {
        "name": "QPIRI",
        "description": "Device rating inquiry",
        "help": " -- queries the Inverter ratings",
        "type": "QUERY",
        "response": [
            ["float", "Grid Input Voltage Rating", "V"],
            ["float", "Grid Input Frequency Rating", "Hz"],
            ["float", "Grid Input Current Rating", "A"],
            ["float", "AC Output Voltage Rating", "V"],
            ["float", "AC Output Current Rating", "A"],
            ["float", "Per MPPT Current Rating", "A"],
            ["float", "Battery Voltage Rating", "V"],
            ["int", "MPPT Track Number", ""],
            [
                "keyed",
                "Machine Type",
                {"00": "Grid tie", "01": "Off Grid", "10": "Hybrid"},
            ],
            ["option", "Topology", ["transformerless", "transformer"]],
        ],
        "test_responses": [
            b"(230.0 50.0 013.0 230.0 013.0 18.0 048.0 1 10 0\x86\x42\r",
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

    def get_responses(self, response):
        """
        Override the default get_responses as its different for PI00
        """
        responses = response.split(b" ")
        # Trim leading '(' of first response
        responses[0] = responses[0][1:]
        # Remove CRC and \r of last response
        responses[-1] = responses[-1][:-3]
        return responses

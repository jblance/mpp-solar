import logging

from .protocol import AbstractProtocol
from .protocol_helpers import crcPI as crc

# from .pi30 import COMMANDS

log = logging.getLogger("MPP-Solar")

COMMANDS = {
    "ET": {
        "name": "ET",
        "prefix": "^P005",
        "description": "Total Generated Energy query",
        "help": " -- Query total generated energy",
        "type": "QUERY",
        "response": [["int", "Total generated energy", "KWh"]],
        "test_responses": [
            b"",
        ],
        "regex": "",
    },
    "GS": {
        "name": "GS",
        "prefix": "^P005",
        "description": "General status query",
        "help": " -- Query general status information",
        "type": "QUERY",
        "response": [
            ["10int", "Grid voltage", "V"],
            ["10int", "Grid frequency", "Hz"],
            ["10int", "AC output voltage", "V"],
            ["10int", "AC output frequency", "Hz"],
            ["int", "AC output apparent power", "VA"],
            ["int", "AC output active power", "W"],
            ["int", "Output load percent", "%"],
            ["10int", "Battery voltage", "V"],
            ["10int", "Battery voltage from SCC", "V"],
            ["10int", "Battery voltage from SCC2", "V"],
            ["int", "Battery discharge current", "A"],
            ["int", "Battery charging current", "A"],
            ["int", "Battery capacity", "%"],
            ["int", "Inverter heat sink temperature", "°C"],
            ["int", "MPPT1 charger temperature", "°C"],
            ["int", "MPPT2 charger temperature", "°C"],
            ["int", "PV1 Input power", "W"],
            ["int", "PV2 Input power", "W"],
            ["10int", "PV1 Input voltage", "V"],
            ["10int", "PV2 Input voltage", "V"],
            [
                "option",
                "Setting value configuration state",
                ["Nothing changed", "Something changed"],
            ],
            [
                "option",
                "MPPT1 charger status",
                ["abnormal", "normal but not charged", "charging"],
            ],
            [
                "option",
                "MPPT2 charger status",
                ["abnormal", "normal but not charged", "charging"],
            ],
            ["option", "Load connection", ["disconnect", "connect"]],
            ["option", "Battery power direction", ["donothing", "charge", "discharge"]],
            ["option", "DC/AC power direction", ["donothing", "AC-DC", "DC-AC"]],
            ["option", "Line power direction", ["donothing", "input", "output"]],
            ["int", "Local parallel ID", ""],
        ],
        "test_responses": [
            b"D1062232,499,2232,499,0971,0710,019,008,000,000,000,000,000,044,000,000,0520,0000,1941,0000,0,2,0,1,0,2,1,0\x09\x7b\r",
        ],
        "regex": "",
    },
    "MOD": {
        "name": "MOD",
        "prefix": "^P006",
        "description": "Working mode query",
        "help": " -- Query the working mode",
        "type": "QUERY",
        "response": [
            [
                "option",
                "Working mode",
                [
                    "Power on mode",
                    "Standby mode",
                    "Bypass mode",
                    "Battery mode",
                    "Fault mode",
                    "Hybrid mode(Line mode, Grid mode)",
                ],
            ]
        ],
        "test_responses": [
            b"",
        ],
        "regex": "",
    },
    "PI": {
        "name": "PI",
        "prefix": "^P005",
        "description": "Device Protocol Version inquiry",
        "help": " -- queries the device protocol version",
        "type": "QUERY",
        "response": [["string", "Protocol Version", ""]],
        "test_responses": [
            b"",
        ],
        "regex": "",
    },
}


class pi18(AbstractProtocol):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI18"
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = ["MOD", "GS", "ET"]
        self.SETTINGS_COMMANDS = [
            "PI",
        ]
        self.DEFAULT_COMMAND = "PI"

    def get_full_command(self, command) -> bytes:
        """
        Override the default get_full_command as its different for PI18
        """
        log.info(f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands")
        # These need to be set to allow other functions to work`
        self._command = command
        self._command_defn = self.get_command_defn(command)
        # End of required variables setting
        if self._command_defn is None:
            return None

        _cmd = bytes(self._command, "utf-8")
        _type = self._command_defn["type"]

        # calculate the CRC
        crc_high, crc_low = crc(_cmd)
        # combine byte_cmd, CRC , return
        # PI18 full command "^P005GS\x..\x..\r"
        command_crc = _cmd + bytes([crc_high, crc_low, 13])
        if _type == "QUERY":
            _prefix = f"^P{len(command_crc):03}"
            full_command = bytes(_prefix, "utf-8") + command_crc
        log.debug(f"full command: {full_command}")
        return full_command

    def get_responses(self, response):
        """
        Override the default get_responses as its different for PI18
        """
        responses = response.split(b",")
        # Drop ^Dxxx from first response
        responses[0] = responses[0][4:]
        # Remove CRC of last response
        responses[-1] = responses[-1][:-3]
        return responses

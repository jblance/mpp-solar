import logging

from .pi30m045 import pi30m045

log = logging.getLogger("pi30m054")

QUERY_COMMANDS = {
    "QBMS": {
        "name": "QBMS",
        "description": "Read lithium battery information",
        "help": " -- queries the value of various metrics from the battery",
        "type": "QUERY",
        "crctype": "chk",
        "response_type": "INDEXED",
        "response": [
            [0, "Battery connect status", "str_keyed", {"0": "Connected", "1": "Disconnected"}],
            [1, "Battery capacity from BMS", "int", "%"],
            [2, "Battery force charging", "str_keyed", {"0": "No", "1": "Yes"}],
            [3, "Battery stop discharge flag", "str_keyed", {"0": "Enable discharge", "1": "Disable discharge"}],
            [4, "Battery stop charge flag", "str_keyed", {"0": "Enable charge", "1": "Disable charge"}],
            [5, "Battery bulk charging voltage from BMS", "int:r/10", "V"],
            [6, "Battery float charging voltage from BMS", "int:r/10", "V"],
            [7, "Battery cut off voltage from BMS", "int:r/10", "V"],
            [8, "Battery max charging current", "int", "A"],
            [9, "Battery max discharge current", "int", "A"]],
        "test_responses": [
            b"(0 086 0 0 0 532 532 450 0120 0240\x7fU\r",
        ],
    },
}

class pi30m054(pi30m045):
    def __str__(self):
        return "PI30 protocol handler for MKS2 and similar inverters"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._protocol_id = b"PI30M054"
        self.COMMANDS.update(QUERY_COMMANDS)
        log.info(f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands")

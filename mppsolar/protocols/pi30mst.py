import logging

from .pi30max import pi30max

log = logging.getLogger("pi30mst")

QUERY_COMMANDS = {
    "QPIGS2": {
        "name": "QPIGS2",
        "description": "General Status Parameters inquiry 2 for 3 PV",
        "type": "QUERY",
        "response": [
            ["float", "PV2 Input Current", "A"],
            ["float", "PV2 Input Voltage", "V"],
            ["float", "Battery voltage from SCC 2", "V"],
            ["int", "PV2 Charging Power", "W"],
            ["string", "Device status", ""],
            ["float", "AC charging current", "A"],
            ["int", "AC charging power", "W"],
            ["float", "PV3 Input Current", "A"],
            ["float", "PV3 Input Voltage", "V"],
            ["float", "Battery voltage from SCC 3", "V"],
            ["int", "PV3 Charging Power", "W"],
            ["int", "PV total charging power", "W"],
        ],
        "test_responses": [
            b"(03.1 327.3 01026 \xc9\x8b\r",
        ],
    },
}

# SETTER_COMMANDS = {}
# COMMANDS = QUERY_COMMANDS
# COMMANDS.update(SETTER_COMMANDS)


class pi30mst(pi30max):
    def __str__(self):
        return "PI30 protocol handler for PIP4048MST with 3 PV and similar inverters"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI30MST"
        self.COMMANDS.update(QUERY_COMMANDS)
        # self.STATUS_COMMANDS = ["QPIGS", "QPIGS2"]
        # self.SETTINGS_COMMANDS = ["QPIRI", "QFLAG"]
        # self.DEFAULT_COMMAND = "QPI"
        # log.info(f'Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands')

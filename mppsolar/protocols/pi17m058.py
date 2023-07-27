import logging

from .pi17 import pi17


log = logging.getLogger("pi17m058")

QUERY_COMMANDS = {
    "BATS": {
        "name": "BATS",
        "description": "Query battery setting",
        "help": " -- queries battery setting",
        "type": "QUERY",
        "response_type": "INDEXED",
        "response": [
            [1, "Battery maximum charge current", "int:r/10", "A"],
            [2, "Battery constant charge voltage", "int:r/10", "V"],
            [3, "Battery floating charge voltage", "int:r/10", "V"],
            [4, "Battery stop charger current level in floating charging", "int:r/10", "A"],
            [
                5,
                "Keep charged time of battery catch stopped charging current level",
                "int",
                "Minutes",
            ],
            [
                6,
                "Battery voltage of recover to charge when battery stop charger in floating charging",
                "int:r/10",
                "V",
            ],
            [7, "Battery under voltage", "int:r/10", "V"],
            [8, "Battery under voltage release", "int:r/10", "V"],
            [9, "Battery weak voltage in hybrid mode", "int:r/10", "V"],
            [10, "Battery weak voltage release in hybrid mode", "int:r/10", "V"],
            [11, "Battery Type", "option", ["Ordinary", "Li-Fe"]],
            [12, "Reserved1", "discard", ""],
            [13, "Reserved2", "discard", ""],
            [
                14,
                "AC charger keep battery voltage function enable/diable",
                "option",
                ["Disabled", "Enabled"],
            ],
            [15, "AC charger keep battery voltage", "int:r/10", "V"],
            [16, "Battery temperature sensor compensation", "int:r/10", "mV"],
            [17, "Max. AC charging current", "int:r/10", "A"],
            [18, "Battery discharge max current in hybrid mode", "int", "A"],
            [19, "Battery under SOC", "int", "%"],
            [20, "Battery under back SOC", "int", "%"],
            [21, "Battery weak SOC in hybrid mode", "int", "%"],
            [22, "Battery weak back SOC in hybrid mode", "int", "%"],
            [23, "Unknown", "int", ""],
        ],
        "test_responses": [b"^D0941750,0560,0540,0000,060,0530,0420,0480,0480,0540,0,,,0,0480,000,0100,0175,010,020,020,080,0mr\r"],
    },
}
SETTER_COMMANDS = {}
COMMANDS_TO_REMOVE = []


#


class pi17m058(pi17):
    def __str__(self):
        return "PI17 protocol handler modified for model 058"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI17m058"
        # Add pi17m058 specific commands to pi17 commands
        self.COMMANDS.update(QUERY_COMMANDS)
        # Add pi17m058 specific setter commands
        self.COMMANDS.update(SETTER_COMMANDS)
        # remove and unwanted pi30 commands
        for item in COMMANDS_TO_REMOVE:
            if item in self.COMMANDS:
                self.COMMANDS.pop(item)

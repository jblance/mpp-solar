""" mppsolar / protocols / pi17infini.py """
import logging

from .pi17 import pi17


log = logging.getLogger("pi17infini")

QUERY_COMMANDS = {}
SETTER_COMMANDS = {
    "ACCT": {
        "name": "ACCT",
        "description": "Set AC charge time range",
        "help": " -- examples: ACCT2200,2259,2300,2359 (Sets primary time range from 22:00 to 22:59 and secondary time range from 23:00 to 23:59. End minute is inclusive)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "ACCT((2[0-3]|[01]?[0-9])([0-5]?[0-9]),(2[0-3]|[01]?[0-9])([0-5]?[0-9]),(2[0-3]|[01]?[0-9])([0-5]?[0-9]),(2[0-3]|[01]?[0-9])([0-5]?[0-9]))$",
    },
    "PEA": {
        "name": "PEA",
        "description": "Enable 'mute buzzer beep",
        "help": " -- enable the 'mute buzzer beep'",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "PDA": {
        "name": "PDA",
        "description": "Disable 'mute buzzer beep",
        "help": " -- disable the 'mute buzzer beep'",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
}
COMMANDS_TO_REMOVE = ["PA", "PB"]


class pi17infini(pi17):
    """ pi17 protocol for Infini-Solar inverters (2022 specs) """
    def __str__(self):
        return "PI17INFINI protocol handler"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI17INFINI"
        # Add pi17infini specific commands to pi17 commands
        self.COMMANDS.update(QUERY_COMMANDS)
        # Add pi17infini specific setter commands
        self.COMMANDS.update(SETTER_COMMANDS)
        # remove and unwanted pi30 commands
        for item in COMMANDS_TO_REMOVE:
            self.COMMANDS.pop(item, None)

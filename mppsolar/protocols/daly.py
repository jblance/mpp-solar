import logging
from typing import Tuple

from .abstractprotocol import AbstractProtocol
from .protocol_helpers import crc8 as dalyChecksum

# from .pi30 import COMMANDS

log = logging.getLogger("daly")

# (AAA BBB CCC DDD EEE
# (000 001 002 003 004

COMMANDS = {
    "SOC": {
        "name": "SOC",
        "description": "State of Charge",
        "help": " -- display the battery state of charge",
        "type": "DALY",
        "command_code": "90",  # or should be the more accurate 1000
        "response_type": "POSITIONAL",
        "response": [
            ["hex", 1, "start flag", ""],
            ["hex", 1, "module address", ""],
            ["hex", 1, "command id", ""],
            ["hex", 1, "data length", ""],
            ["hex", 2, "pressure", "0.1V"],
            ["hex", 2, "acquistion", "0.1V"],
            ["hex", 2, "current 30000 offset", "0.1A"],
            ["hex", 2, "SOC", "0.1%"],
            ["hex", 1, "checksum", ""],
        ],
        "test_responses": [
            bytes.fromhex("A58090080000000000000000bd\n"),
        ],
        "regex": "",
    },
}


class daly(AbstractProtocol):
    """
    DALY - Daly BMS protocol handler
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"DALY"
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = [
            "SOC",
        ]
        self.SETTINGS_COMMANDS = [
            "",
        ]
        self.DEFAULT_COMMAND = "SOC"

    def get_full_command(self, command) -> bytes:
        """
        Override the default get_full_command as its different for DALY
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

        # DALY
        startFlag = bytes.fromhex("A5")
        moduleAddress = bytes.fromhex("80")
        commandID = bytes.fromhex(self._command_defn["command_code"])
        # commandID = bytes.fromhex("90")
        dataLength = bytes.fromhex("08")
        data = bytes.fromhex("00" * 8)
        cmd = startFlag + moduleAddress + commandID + dataLength + data

        checksum = f"{dalyChecksum(cmd):02X}"
        cmd = cmd + bytes.fromhex(checksum) + b"\n"
        log.debug(f"get_full_command: full command: {cmd}")
        return cmd

    def check_response_valid(self, response) -> Tuple[bool, dict]:
        """
        DALY protocol - checksum is sum of bytes
        """
        if not response:
            return False, {"ERROR": ["No response", ""]}
        # HEX protocol response
        log.debug(f"checking validity of {response}")

        # _r = response.split(b":")[1][:-1].decode()
        # print(f"trimmed response {_r}")
        # _r = f"0{_r}"
        # print(f"padded response {_r}")
        # _r = bytes.fromhex(response)
        _r = response
        # print(f"bytes response {_r}")
        data = _r[:-1]
        checksum = _r[-1:][0]
        if dalyChecksum(data) == checksum:
            log.debug(f"DALY Checksum matches response '{response}' checksum:{checksum}")
            return True, {}
        else:
            # print("VED Hex Checksum does not match")
            return False, {"ERROR": [f"DALY checksum did not match for response {response}", ""]}

    def get_responses(self, response):
        """
        Override the default get_responses as its different for PI00
        """
        # remove \n
        response = response.replace(b"\n", b"")
        responses = []
        for r in response:
            responses.append(r)
        return responses

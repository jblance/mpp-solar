import logging
import struct

from .abstractprotocol import AbstractProtocol
from .protocol_helpers import crc8


log = logging.getLogger("jkAbstractProtocol")

SOR = bytes.fromhex("55aaeb90")

COMMANDS = {
    "getInfo": {
        "name": "getInfo",
        "command_code": "97",
        "record_type": "3",
        "description": "BLE Device Information inquiry",
        "help": " -- queries the ble device information",
        "type": "QUERY",
        "response_type": "POSITIONAL",
        "response": [
            ["Hex2Str", 4, "Header", ""],
            ["Hex2Str", 1, "Record Type", ""],
            ["Hex2Int", 1, "Record Counter", ""],
            ["Hex2Ascii", 16, "Device Model", ""],
            ["Hex2Ascii", 8, "Hardware Version", ""],
            ["Hex2Ascii", 8, "Software Version", ""],
            ["uptime", 4, "Up Time", ""],
            ["Hex2Int", 4, "Power-on Times", ""],
            ["Hex2Ascii", 16, "Device Name", ""],
            ["Hex2Ascii", 16, "Device Passcode", ""],
            ["Hex2Ascii", 8, "Manufacturing Date", ""],
            ["Hex2Ascii", 11, "Serial Number", ""],
            ["Hex2Ascii", 5, "Passcode", ""],
            ["Hex2Ascii", 16, "User Data", ""],
            ["Hex2Ascii", 16, "Setup Passcode", ""],
            ["discard", 672, "unknown", ""],
        ],
        "test_responses": [
            bytes.fromhex(
                "55aaeb9003f14a4b2d42324132345300000000000000332e300000000000332e322e330000000876450004000000506f7765722057616c6c203100000000313233340000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c2"
            ),
            bytes.fromhex(
                "55aaeb9003b54a4b2d42443641323053313050000000342e300000000000342e312e37000000541d1600040000004e6f7468696e67204a4b31000000000031323334000000000000000000000000323030373038000032303036323834303735000000000000496e707574205573657264617461000031323334353600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c4"
            ),
        ],
    },
}


class jkAbstractProtocol(AbstractProtocol):
    """
    JKAbstractProtocol - Abstract Handler for JKBMS communication
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"JK"
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = [
            "",
        ]
        self.SETTINGS_COMMANDS = [
            "getInfo",
        ]
        self.DEFAULT_COMMAND = "getInfo"
        self.ID_COMMANDS = None

    def get_full_command(self, command) -> bytes:
        """
        Override the default get_full_command as its different for JK
        """
        # getInfo = b'\xaa\x55\x90\xeb\x97\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11'
        log.info(f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands")
        # These need to be set to allow other functions to work`
        self._command = command
        self._command_defn = self.get_command_defn(command)
        # log.debug(f"self._command = {self._command}, self._command_defn = {self._command_defn}")
        log.debug(f"self._command = {self._command}")
        # End of required variables setting
        if self._command_defn is None:
            # Maybe return a default here?
            log.debug("No command_defn found")
            return None
        if "command_code" in self._command_defn:
            # full command is 20 bytes long
            cmd = bytearray(20)
            # starts with \xaa\x55\x90\xeb
            cmd[0:4] = bytes.fromhex("aa5590eb")
            log.debug(f"cmd with SOR: {cmd}")
            # then has command code
            cmd[4] = int(self._command_defn["command_code"], 16)
            if self._command_defn["type"] == "SETTER":
                cmd[5] = 0x04
                value = struct.pack("<h", int(float(self._command_value) * 1000))
                cmd[6] = value[0]
                cmd[7] = value[1]
            log.debug(f"cmd with command code: {cmd}")
            cmd[-1] = crc8(cmd)
            log.debug(f"cmd with crc: {cmd}")
            return cmd
        return None

    def get_command_defn(self, command):
        log.debug(f"get_command_defn for: {command}")
        if command is None:
            log.debug("command is None")
            return None
        return super().get_command_defn(command)

    def get_responses(self, response):
        """
        Override the default get_responses as its different for JK
        """
        responses = []
        if self._command_defn is not None and self._command_defn["response_type"] == "POSITIONAL":
            # Have a POSITIONAL type response, so need to break it up...
            # example defn :
            # "response": [
            #   ["discard", 1, "start flag", ""],
            #   ["discard", 1, "module address", ""],
            #   ["discard", 1, "command id", ""],
            #   ["discard", 1, "data length", ""],
            # ]
            # example response data b"\xa5\x01\x90\x08\x02\x10\x00\x00uo\x03\xbc\xf3",
            for defn in self._command_defn["response"]:
                log.debug(f"Got defn: {defn}")
                if defn[0].startswith("lookup"):
                    responses.append("lookup")
                    continue
                size = defn[1]
                item = response[:size]
                responses.append(item)
                response = response[size:]
            if len(response) > 0:
                responses.append(response)
            return responses
        else:
            return bytearray(response)

    def is_record_start(self, record):
        if record.startswith(SOR):
            log.debug("SOR found in record")
            return True
        return False

    def wipe_to_start(self, record):
        sor_loc = record.find(SOR)
        if sor_loc == -1:
            log.debug("SOR not found in record")
            return bytearray()
        return record[sor_loc:]

    def is_record_correct_type(self, record, type):
        if len(record) < len(SOR):
            return False
        if record[len(SOR)] == int(type):
            log.debug(f"Record is type {type}")
            return True
        return False

    def is_record_complete(self, record):
        """"""
        # check record starts with 'SOR'
        if not self.is_record_start(record):
            log.debug("No SOR found in record looking for completeness")
            return False
        # check that length one of the valid lengths (300, 320)
        if len(record) == 300 or len(record) == 320:
            # check the crc/checksum is correct for the record data
            crc = record[299]
            calcCrc = crc8(record[:-1])
            # print (crc, calcCrc)
            if crc == calcCrc:
                log.debug("Record CRC is valid")
                return True
        return False

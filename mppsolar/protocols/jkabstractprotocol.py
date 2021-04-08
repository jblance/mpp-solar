import logging
import math

from .abstractprotocol import AbstractProtocol
from .protocol_helpers import decode4ByteHex1000, decode4ByteHex, decode2ByteHex, crc8


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
        "response": [
            ["hex", 4, "Header", ""],
            ["hex", 1, "Record Type", ""],
            ["int", 1, "Record Counter", ""],
            ["ascii", 10, "Device Model", ""],
            ["ascii", 10, "Hardware Version", ""],
            ["ascii", 10, "Software Version", ""],
            ["discard", 10, "", ""],
            ["ascii", 16, "Device Name", ""],
            ["ascii", 10, "Device Passcode", ""],
            ["ascii", 14, "Unknown1", ""],
            ["ascii", 14, "Unknown2", ""],
            ["ascii", 16, "User Data", ""],
            ["ascii", 16, "Settings Passcode?", ""],
        ],
        "test_responses": [
            bytes.fromhex(
                "55aaeb9003f14a4b2d42324132345300000000000000332e300000000000332e322e330000000876450004000000506f7765722057616c6c203100000000313233340000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c2"
            ),
            bytes.fromhex(
                "55aaeb9003b54a4b2d42443641323053313050000000342e300000000000342e312e37000000541d1600040000004e6f7468696e67204a4b31000000000031323334000000000000000000000000323030373038000032303036323834303735000000000000496e707574205573657264617461000031323334353600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c4"
            ),
        ],
        "regex": "",
    },
}


class jkAbstractProtocol(AbstractProtocol):
    """
    JKAbstractProtocol - Abstract Handler for JKBMS communication
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"JK02"
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = [
            "",
        ]
        self.SETTINGS_COMMANDS = [
            "getInfo",
        ]
        self.DEFAULT_COMMAND = "getInfo"

    def get_full_command(self, command) -> bytes:
        """
        Override the default get_full_command as its different for JK
        """
        # getInfo = b'\xaa\x55\x90\xeb\x97\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11'
        log.info(
            f"get_full_command: Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands"
        )
        # These need to be set to allow other functions to work`
        self._command = command
        self._command_defn = self.get_command_defn(command)
        log.debug(
            f"get_full_command: self._command = {self._command}, self._command_defn = {self._command_defn}"
        )
        # End of required variables setting
        if self._command_defn is None:
            # Maybe return a default here?
            log.debug("get_full_command: No command_defn found")
            return None
        if "command_code" in self._command_defn:
            # full command is 20 bytes long
            cmd = bytearray(20)
            # starts with \xaa\x55\x90\xeb
            cmd[0:4] = bytes.fromhex("aa5590eb")
            log.debug(f"get_full_command: cmd with SOR: {cmd}")
            # then has command code
            cmd[4] = int(self._command_defn["command_code"], 16)
            log.debug(f"get_full_command: cmd with command code: {cmd}")
            cmd[-1] = crc8(cmd)
            log.debug(f"get_full_command: cmd with crc: {cmd}")
            return cmd
        return None

    def get_command_defn(self, command):
        log.debug(f"get_command_defn: get_command_defn for: {command}")
        if command is None:
            log.debug("get_command_defn: command is None")
            return None
        return super().get_command_defn(command)

    def get_responses(self, response):
        """
        Override the default get_responses as its different for JK
        """
        return bytearray(response)

    def is_record_start(self, record):
        if record.startswith(SOR):
            log.debug("get_responses: SOR found in record")
            return True
        return False

    def is_record_correct_type(self, record, type):
        if len(record) < len(SOR):
            return False
        if record[len(SOR)] == int(type):
            log.debug(f"is_record_correct_type: Record is type {type}")
            return True
        return False

    def is_record_complete(self, record):
        """"""
        # check record starts with 'SOR'
        if not self.is_record_start(record):
            log.debug("is_record_complete: No SOR found in record looking for completeness")
            return False
        # check that length one of the valid lengths (300, 320)
        if len(record) == 300 or len(record) == 320:
            # check the crc/checksum is correct for the record data
            crc = ord(record[-1:])
            calcCrc = crc8(record[:-1])
            # print (crc, calcCrc)
            if crc == calcCrc:
                log.debug("is_record_complete: Record CRC is valid")
                return True
        return False

    def decode(self, response, command) -> dict:
        msgs = {}
        log.info(f"decode: response passed to decode: {response}")
        # No response
        if response is None:
            log.info("decode: No response")
            msgs["ERROR"] = ["No response", ""]
            return msgs

        # Raw response
        _response = b""
        for item in response:
            _response += chr(item).encode()
        raw_response = _response.decode("utf-8")
        msgs["raw_response"] = [raw_response, ""]

        command_defn = self.get_command_defn(command)
        # Add metadata
        msgs["_command"] = command
        if command_defn is not None:
            msgs["_command_description"] = command_defn["description"]

        # Check for a stored command definition
        if not command_defn:
            # No definiution, so just return the data
            len_command_defn = 0
            log.debug(f"decode: No definition for command {command}, raw response returned")
            msgs["ERROR"] = [
                f"No definition for command {command} in protocol {self._protocol_id}",
                "",
            ]
        else:
            len_command_defn = len(command_defn["response"])
            # Decode response based on stored command definition
            responses = self.get_responses(response)
            log.debug(f"decode: Length of responses {len(responses)}")

            for defn in command_defn["response"]:
                log.debug(f"decode: Processing defn {defn}")
                # ["hex", 4, "Header", ""]
                # if defn[2] == "":
                #    log.debug(f"skipping {defn} and no name defined")
                if defn[0] == "lookup":
                    # calculated lookup column
                    # looks for a columnb based on another
                    # ["int+", 1, "Highest Cell", ""],
                    # ["lookup", "Highest Cell", "Voltage Cell", "Highest Cell Voltage" ],
                    log.debug("decode: using lookup defn")
                    lookup_value = msgs[defn[1]][0]
                    key_tofind = f"{defn[2]}{lookup_value:02d}"
                    value = msgs[key_tofind][0]
                    unit = msgs[key_tofind][1]
                    msgs[defn[3]] = [value, unit]
                elif defn[0] == "hex":
                    log.debug("decode: hex defn")
                    value = ""
                    for x in range(defn[1]):
                        value += f"{responses.pop(0):02x}"
                    if defn[2] != "":
                        msgs[defn[2]] = [value, defn[3]]
                elif defn[0] == "ascii":
                    log.debug("decode: ascii defn")
                    value = ""
                    for x in range(defn[1]):
                        b = responses.pop(0)
                        if b == 0:
                            continue
                        value += f"{b:c}"
                    msgs[defn[2]] = [value, defn[3]]
                elif defn[0] == "uptime":
                    log.debug("decode: uptime defn")
                    value = 0
                    for x in range(defn[1]):
                        b = responses.pop(0)
                        value += b * 256 ** x
                        log.debug(f"decode: Uptime int value {value} for pos {x}")
                    daysFloat = value / (60 * 60 * 24)
                    days = math.trunc(daysFloat)
                    hoursFloat = (daysFloat - days) * 24
                    hours = math.trunc(hoursFloat)
                    minutesFloat = (hoursFloat - hours) * 60
                    minutes = math.trunc(minutesFloat)
                    secondsFloat = (minutesFloat - minutes) * 60
                    seconds = round(secondsFloat)
                    uptime = f"{days}D{hours}H{minutes}M{seconds}S"
                    log.info(f"decode: Uptime result {uptime}")
                    msgs[defn[2]] = [uptime, defn[3]]
                elif defn[0] == "discard":
                    log.debug(f"decode: Discarding {defn[1]} values")
                    value = ""
                    for x in range(defn[1]):
                        value += f"{responses.pop(0):02x}"
                    log.debug(f"decode: Discarded {value}")
                    # if defn[2] != "":
                    #    msgs[defn[2]] = [value, defn[3]]
                elif defn[0] == "int":
                    log.debug("decode: int defn")
                    msgs[defn[2]] = [responses.pop(0), defn[3]]
                elif defn[0] == "int+":
                    log.debug("decode: int+ defn")
                    msgs[defn[2]] = [responses.pop(0) + 1, defn[3]]
                elif defn[0] == "16Int":
                    log.debug("decode: 16Int defn")
                    value = responses.pop(0) * 256
                    value += responses.pop(0)
                    # print(f"value {value}")
                    msgs[defn[2]] = [value, defn[3]]
                elif defn[0] == "16Int100":
                    log.debug("decode: 16Int100 defn")
                    value = responses.pop(0) * 256
                    value += responses.pop(0)
                    value = value / 100
                    # print(f"value {value}")
                    msgs[defn[2]] = [value, defn[3]]
                elif defn[0] == "16Int1000":
                    log.debug("decode: 16Int1000 defn")
                    value = responses.pop(0) * 256
                    value += responses.pop(0)
                    value = value / 1000
                    # print(f"value {value}")
                    msgs[defn[2]] = [value, defn[3]]
                elif defn[0] == "2ByteHex":
                    log.debug("decode: 2ByteHex defn")
                    v = responses[:2]
                    responses = responses[2:]
                    value = decode2ByteHex(v)
                    msgs[defn[2]] = [value, defn[3]]
                elif defn[0] == "2ByteHexU":
                    # used for unknow values provides undecoded hex as well
                    log.debug("decode: 2ByteHexU defn")
                    v = responses[:2]
                    responses = responses[2:]
                    value = decode2ByteHex(v)
                    if defn[2] != "":
                        msgs[defn[2]] = [value, f"{v[0]:02x} {v[1]:02x}"]
                elif defn[0] == "2ByteHexC":
                    # temperatures seem to be deocded value * 100
                    log.debug("decode: 2ByteHexC defn")
                    v = responses[:2]
                    responses = responses[2:]
                    value = decode2ByteHex(v) * 100
                    msgs[defn[2]] = [value, defn[3]]
                elif defn[0] == "4ByteHex":
                    log.debug("decode: 4ByteHex defn")
                    v = responses[:4]
                    responses = responses[4:]
                    value = decode4ByteHex(v)
                    msgs[defn[2]] = [value, defn[3]]
                elif defn[0] == "4ByteHex1000":
                    log.debug("decode: 4ByteHex1000 defn")
                    v = responses[:4]
                    responses = responses[4:]
                    value = decode4ByteHex1000(v)
                    msgs[defn[2]] = [value, defn[3]]
                elif defn[0] == "4ByteHexU":
                    log.debug("decode: 4ByteHexU defn")
                    v = responses[:4]
                    responses = responses[4:]
                    value = decode4ByteHex(v)
                    msgs[defn[2]] = [value, f"{v[0]:02x} {v[1]:02x} {v[2]:02x} {v[3]:02x}"]
                elif defn[0] == "loop":
                    log.debug("decode: loop defn")
                    # loop of repeating data, eg cell voltages
                    for x in range(defn[1]):
                        param = f"{defn[2]}{x+1:02d}"
                        if defn[4] == "4ByteHex":
                            v = responses[:4]
                            responses = responses[4:]
                            value = decode4ByteHex(v)
                            msgs[param] = [value, defn[3]]
                        if defn[4] == "2ByteHex":
                            v = responses[:2]
                            responses = responses[2:]
                            value = decode2ByteHex(v)
                            msgs[param] = [value, defn[3]]
                        if defn[4] == "16Int1000":
                            value = responses.pop(0) * 256
                            value += responses.pop(0)
                            value = value / 1000
                            msgs[param] = [value, defn[3]]
                elif defn[0] == "rem":
                    log.debug(f"decode: {len(responses)} bytes remain: {str(responses)}")
                    # msgs["remainder"] = [str(responses), ""]
                    # msgs["len remainder"] = [len(responses), ""]
                    return msgs
                else:
                    log.error("decode: undefined type")
        return msgs

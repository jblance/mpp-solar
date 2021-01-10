import logging
import math

from .protocol import AbstractProtocol
from .protocol_helpers import decode4ByteHex, decode2ByteHex, crc8


log = logging.getLogger("MPP-Solar")

# >>> print(f'{151:#04x}')
# 0x97
# >>> print(f'{1:#04x}')
# 0x01
# >>> print(f'{1:#02x}')
# 0x1
# >>> print(f'{1:#04x}')
# 0x01
# >>> bytes.fromhex('aa5590eb')
# b'\xaaU\x90\xeb'
# getInfo = b'\xaa\x55\x90\xeb\x97\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11'
# getCellInfo = b'\xaa\x55\x90\xeb\x96\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10'
# message after 9003
# aa5590ebc8010100000000000000000000000044
# 55aaeb90
# 02 record type
# b5 counter
SOR = bytes.fromhex("55aaeb90")

COMMANDS = {
    "getInfo": {
        "name": "getInfo",
        "command_code": "97",
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
        log.info(f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands")
        # These need to be set to allow other functions to work`
        self._command = command
        self._command_defn = self.get_command_defn(command)
        # End of required variables setting
        if self._command_defn is None:
            # Maybe return a default here?
            return None
        if "command_code" in self._command_defn:
            # full command is 20 bytes long
            cmd = bytearray(20)
            # starts with \xaa\x55\x90\xeb
            cmd[0:4] = bytes.fromhex("aa5590eb")
            log.debug(f"cmd with SOR: {cmd}")
            # then has command code
            cmd[4] = int(self._command_defn["command_code"], 16)
            log.debug(f"cmd with command code: {cmd}")
            cmd[-1] = crc8(cmd)
            log.debug(f"cmd with crc: {cmd}")
            return cmd
        return None

    def get_responses(self, response):
        """
        Override the default get_responses as its different for JK
        """
        # responses = response.split(b" ")
        # Trim leading '(' of first response
        # responses[0] = responses[0][1:]
        # Remove CRC and \r of last response
        # responses[-1] = responses[-1][:-3]
        return bytearray(response)

    def is_record_start(self, record):
        if record.startswith(SOR):
            log.debug("SOR found in record")
            return True
        return False

    def is_record_complete(self, record):
        """"""
        # check record starts with 'SOR'
        if not self.is_record_start(record):
            log.error("No SOR found in record looking for completeness")
            return False
        # check that length one of the valid lengths (300, 320)
        if len(record) == 300 or len(record) == 320:
            # check the crc/checksum is correct for the record data
            crc = ord(record[-1:])
            calcCrc = crc8(record[:-1])
            # print (crc, calcCrc)
            if crc == calcCrc:
                log.debug("Record CRC is valid")
                return True
        return False

    def decode(self, response, show_raw) -> dict:
        msgs = {}
        log.info(f"response passed to decode: {response}")
        # No response
        if response is None:
            log.info("No response")
            msgs["ERROR"] = ["No response", ""]
            return msgs

        # Raw response requested
        if show_raw:
            log.debug(f'Protocol "{self._protocol_id}" raw response requested')
            # TODO: deal with \x09 type crc response items better
            _response = b""
            for item in response:
                _response += chr(item).encode()
            raw_response = _response.decode("utf-8")
            msgs["raw_response"] = [raw_response, ""]
            return msgs

        # Check for a stored command definition
        if not self._command_defn:
            # No definiution, so just return the data
            len_command_defn = 0
            log.debug(f"No definition for command {self._command}, raw response returned")
            msgs["ERROR"] = [
                f"No definition for command {self._command} in protocol {self._protocol_id}",
                "",
            ]
        else:
            len_command_defn = len(self._command_defn["response"])
            # Decode response based on stored command definition
            responses = self.get_responses(response)
            log.debug(f"Length of responses {len(responses)}")

            for defn in self._command_defn["response"]:
                log.debug(f"Processing defn {defn}")
                # ["hex", 4, "Header", ""]
                if defn[0] == "hex":
                    log.debug("hex defn")
                    value = ""
                    for x in range(defn[1]):
                        value += f"{responses.pop(0):02x}"
                    msgs[defn[2]] = [value, defn[3]]
                elif defn[0] == "ascii":
                    log.debug("ascii defn")
                    value = ""
                    for x in range(defn[1]):
                        b = responses.pop(0)
                        if b == 0:
                            continue
                        value += f"{b:c}"
                    msgs[defn[2]] = [value, defn[3]]
                elif defn[0] == "uptime":
                    log.debug("uptime defn")
                    value = 0
                    for x in range(defn[1]):
                        b = responses.pop(0)
                        value += b * 256 ** x
                        log.debug(f"Uptime int value {value} for pos {x}")
                    daysFloat = value / (60 * 60 * 24)
                    days = math.trunc(daysFloat)
                    hoursFloat = (daysFloat - days) * 24
                    hours = math.trunc(hoursFloat)
                    minutesFloat = (hoursFloat - hours) * 60
                    minutes = math.trunc(minutesFloat)
                    secondsFloat = (minutesFloat - minutes) * 60
                    seconds = round(secondsFloat)
                    uptime = f"{days}D{hours}H{minutes}M{seconds}S"
                    log.info(f"Uptime result {uptime}")
                    msgs[defn[2]] = [uptime, defn[3]]
                elif defn[0] == "discard":
                    log.debug(f"Discarding {defn[1]} values")
                    discard = responses[: defn[1]]
                    log.debug(f"Discarded {discard}")
                    msgs[defn[2]] = [f"{str(discard)}", defn[3]]
                    responses = responses[defn[1] :]
                elif defn[0] == "int":
                    log.debug("int defn")
                    msgs[defn[2]] = [responses.pop(0), defn[3]]
                elif defn[0] == "16Int":
                    log.debug("16Int defn")
                    value = responses.pop(0) * 256
                    value += responses.pop(0)
                    print(f"value {value}")
                    msgs[defn[2]] = [f"{value:0.3f}", defn[3]]
                elif defn[0] == "16Int100":
                    log.debug("16Int100 defn")
                    value = responses.pop(0) * 256
                    value += responses.pop(0)
                    value = value / 100
                    print(f"value {value}")
                    msgs[defn[2]] = [f"{value:0.3f}", defn[3]]
                elif defn[0] == "16Int1000":
                    log.debug("16Int1000 defn")
                    value = responses.pop(0) * 256
                    value += responses.pop(0)
                    value = value / 1000
                    print(f"value {value}")
                    msgs[defn[2]] = [f"{value:0.3f}", defn[3]]
                elif defn[0] == "2ByteHex":
                    log.debug("2ByteHex defn")
                    v = responses[:2]
                    responses = responses[2:]
                    value = decode2ByteHex(v)
                    msgs[defn[2]] = [f"{value:0.4f}", defn[3]]
                elif defn[0] == "2ByteHexU":
                    # used for unknow values provides undecoded hex as well
                    log.debug("2ByteHexU defn")
                    v = responses[:2]
                    responses = responses[2:]
                    value = decode2ByteHex(v)
                    msgs[defn[2]] = [f"{value:0.4f}", f"{v[0]:02x} {v[1]:02x}"]
                elif defn[0] == "2ByteHexC":
                    # temperatures seem to be deocded value * 100
                    log.debug("2ByteHexC defn")
                    v = responses[:2]
                    responses = responses[2:]
                    value = decode2ByteHex(v) * 100
                    msgs[defn[2]] = [f"{value:0.1f}", defn[3]]
                elif defn[0] == "4ByteHex":
                    log.debug("4ByteHex defn")
                    v = responses[:4]
                    responses = responses[4:]
                    value = decode4ByteHex(v)
                    msgs[defn[2]] = [f"{value:0.4f}", defn[3]]
                elif defn[0] == "4ByteHexU":
                    log.debug("4ByteHexU defn")
                    v = responses[:4]
                    responses = responses[4:]
                    value = decode4ByteHex(v)
                    msgs[defn[2]] = [f"{value:0.4f}", f"{v[0]:02x} {v[1]:02x} {v[2]:02x} {v[3]:02x}"]
                elif defn[0] == "loop":
                    log.debug("loop defn")
                    # loop of repeating data, eg cell voltages
                    for x in range(defn[1]):
                        param = f"{defn[2]}{x+1:02d}"
                        if defn[4] == "4ByteHex":
                            v = responses[:4]
                            responses = responses[4:]
                            value = decode4ByteHex(v)
                            msgs[param] = [f"{value:0.4f}", defn[3]]
                        if defn[4] == "2ByteHex":
                            v = responses[:2]
                            responses = responses[2:]
                            value = decode2ByteHex(v)
                            msgs[param] = [f"{value:0.4f}", defn[3]]
                elif defn[0] == "rem":
                    log.debug("remainder")
                    msgs["remainder"] = [str(responses), ""]
                    msgs["len remainder"] = [len(responses), ""]
                    return msgs
                else:
                    log.error("undefined type")
        return msgs

import logging

from .abstractprotocol import AbstractProtocol
from .protocol_helpers import crcJK232 as crc


log = logging.getLogger("jk232")


# Read basic information and status
# DD A5 03 00 FF FD 77
# start bit  0xDD
# status 0xA5 means read, status 0x5A means write.
# command code 0x03
# Data length: 1 byte, indicating the effective length of the data carried in the frame.
# Data content: N bytes, the content carried by the frame data, when the data length is 0, there is no such part.
# Verification: 2 bytes,
# the verification field is "command code + length byte + data segment content",
#    the verification method is thesum of the above fields and then the inverse plus 1, the high bit is in the front and the low bit is in the back.
# Stop bit: 1 byte, indicating the end of a frame of data, fixed as 0x77;


COMMANDS = {
    "getBalancerData": {
        "name": "getBalancerData",
        "command_code": "03",
        "description": "Get Balancer Data",
        "help": " -- Get Balancer Data",
        "type": "QUERY",
        "checksum_required": "True",
        "response_type": "POSITIONAL",
        "response": [
            ["Hex2Str", 1, "Start Byte", ""],
            ["Hex2Str", 1, "Command Code", ""],
            ["Hex2Str", 1, "Status", ""],
            ["Hex2Int", 1, "Data Length", ""],
            ["BigHex2Short:r/100", 2, "Total Battery Voltage", "V"],
            ["BigHex2Short:r/100", 2, "Total Current", "A"],
            ["BigHex2Short:r/100", 2, "Remaining Capacity", "Ah"],
            ["BigHex2Short:r/100", 2, "Nominal Capacity", "Ah"],
            ["BigHex2Short", 2, "Cycles", "cycles"],
            ["Hex2Str", 2, "Production Date", ""],
            ["Hex2Str", 2, "Equilibrium State (TODO)", ""],
            ["Hex2Str", 2, "Equilibrium State 2 (TODO)", ""],
            ["Hex2Str", 2, "Protection State (TODO)", ""],
            ["Hex2Str", 1, "Keep", ""],
            ["Hex2Int", 1, "Remaining Battery", "%"],
            ["Hex2Str", 1, "FET Control Status", ""],
            ["Hex2Int", 1, "Number of Battery Strings", ""],
            ["Hex2Int", 1, "Number of NTC", ""],
            ["BigHex2Short:(r-2731)/10", 2, "NTC 1", "°C"],
            ["BigHex2Short:(r-2731)/10", 2, "NTC 2", "°C"],
            ["Hex2Str", 2, "Checksum", ""],
            ["Hex2Str", 1, "End Byte", ""],
        ],
        "test_responses": [
            bytes.fromhex(
                "DD 03 00 1B 17 00 00 00 02 D0 03 E8 00 00 20 78 00 00 00 00 00 00 10 48 03 0F 02 0B 76 0B 82 FB FF 77"
            ),
        ],
    },
}


class jk232(AbstractProtocol):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"JK232"
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = [
            "getBalancerData",
        ]
        self.SETTINGS_COMMANDS = [
            "",
        ]
        self.DEFAULT_COMMAND = "getBalancerData"

    def get_full_command(self, command) -> bytes:
        """
        Override the default get_full_command as its different
        """
        log.info(f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands")
        # These need to be set to allow other functions to work`
        self._command = command
        self._command_defn = self.get_command_defn(command)
        # End of required variables setting
        if self._command_defn is None:
            # Maybe return a default here?
            return None
        if "command_code" in self._command_defn:

            # Read basic information and status
            # DD A5 03 00 FF FD 77
            # full command is 7 bytes long
            cmd = bytearray(7)

            # start bit  0xDD
            cmd[0] = 0xDD
            log.debug(f"cmd with start bit: {cmd}")

            # status 0xA5 means read, status 0x5A means write.
            if self._command_defn["type"] == "SETTER":
                cmd[1] = 0x5A
            else:
                cmd[1] = 0xA5
            # command code 0x03
            command_code = int(self._command_defn["command_code"], 16)
            # Data length: 1 byte, indicating the effective length of the data carried in the frame.
            # Data content: N bytes, the content carried by the frame data, when the data length is 0, there is no such part.
            data = ""
            # TODO: data stuff here
            data_len = len(data)
            if data_len == 0:
                crc_high, crc_low = crc([command_code, data_len])
                cmd[2] = command_code
                cmd[3] = data_len
                cmd[4] = crc_high
                cmd[5] = crc_low
                cmd[6] = 0x77

            log.debug(f"cmd with crc: {cmd}")
            return cmd

    def get_responses(self, response):
        """
        Override the default get_responses as its different
        """
        responses = []
        # remove \n
        # response = response.replace(b"\n", b"")

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
                size = defn[1]
                item = response[:size]
                responses.append(item)
                response = response[size:]
            if response:
                responses.append(response)
            log.debug(f"get_responses: responses {responses}")
            return responses
        else:
            return bytearray(response)

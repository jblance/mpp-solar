import logging
from .abstractprotocol import AbstractProtocol
from .protocol_helpers import crcJK232 as crc

log = logging.getLogger("jk232")


COMMANDS = {
    "getBalancerData": {
        "name": "getBalancerData",
        "command_code": "00",
        "description": "Get Balancer Data",
        "help": " -- Get Balancer Data",
        "type": "QUERY",
        "checksum_required": "True",
        "response_type": "POSITIONAL",
        "response": [
            ["Hex2Str", 50, "response", ""],      # First 12 and last 9 bytes - headers. Data size depends on cell count(3bytes*n cells for voltage)
        ],
        "test_responses": [
            bytes.fromhex(
                "4e 57 01 1b 00 00 00 00 03 00 01 79 2a 01 0f 91 02 0f 94 03 0f 99 04 0f 92 05 0f 94 06 0f 94 07 0f 94 08 0f 91 09 0f 96 0a 0f 91 0b 0f 92 0c 0f 93 0d"
            ),
        ],
    },
}


class jkserial(AbstractProtocol):
    def __str__(self):
        return "JKBMS TTL serial communication protocol handler"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"JKSERIAL"
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
            # full command is 21 bytes long
            cmd = bytearray(21)
            command_code = int(self._command_defn["command_code"], 16)

            # start bit  0x4E
            cmd[0] = 0x4E                         # start sequence
            cmd[1] = 0x57                         # start sequence
            cmd[2] = 0x00                         # data length lb
            cmd[3] = 0x13                         # data length hb
            cmd[4] = 0x00                         # bms terminal number
            cmd[5] = 0x00                         # bms terminal number
            cmd[6] = 0x00                         # bms terminal number
            cmd[7] = 0x00                         # bms terminal number
            if self._command_defn["type"] == "SETTER":
                cmd[8] = 0x02                     # command word: 0x01 (activation), 0x02 (write), 0x03 (read), 0x05 (password), 0x06 (read all)
            else:
                cmd[8] = 0x03
            cmd[9] = 0x03                         # frame source: 0x00 (bms), 0x01 (bluetooth), 0x02 (gps), 0x03 (computer)
            cmd[10] = 0x00                        # frame type: 0x00 (read data), 0x01 (reply frame), 0x02 (BMS active upload)
            cmd[11] = command_code                # register: 0x00 (read all registers), 0x8E...0xBF (holding registers)
            cmd[12] = 0x00                        # record number
            cmd[13] = 0x00                        # record number
            cmd[14] = 0x00                        # record number
            cmd[15] = 0x00                        # record number
            cmd[16] = 0x68                        # end sequence
            cmd[17] = 0x00                        # crc unused
            cmd[18] = 0x00                        # crc unused
            crc_high, crc_low = crc(cmd[0:17])
            cmd[19] = crc_high
            cmd[20] = crc_low

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
            # example response data  b'NW\x01\x1b\x00\x00\x00\x00\x03\x00\x01y*\x01\x0f\x91\x02\x0f\x94\x03\x0f\x97\x04\x0f\x91\x05\x0f\x94\x06\x0f\x94\x07\x0f\x93\x08\x0f\x92\t\x0f\x96\n\x0f\x91\x0b\x0f\x92\x0c\x0f\x92\r'
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
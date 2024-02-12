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
            ["discard", 11, "Packet header", ""],
            ["discard", 1, "Cells connected", ""],
            ["Hex2Int:r/3", 1, "Cells_connected", ""],
            ["discard", 1, "Voltage_Cell01", ""],
            ["BigHex2Short:r/1000", 2, "Voltage_Cell01", "V"],
            ["discard", 1, "Voltage_Cell02", ""],
            ["BigHex2Short:r/1000", 2, "Voltage_Cell02", "V"],
            ["discard", 1, "Voltage_Cell03", ""],
            ["BigHex2Short:r/1000", 2, "Voltage_Cell03", "V"],
            ["discard", 1, "Voltage_Cell04", ""],
            ["BigHex2Short:r/1000", 2, "Voltage_Cell04", "V"],
            ["discard", 1, "Voltage_Cell05", ""],
            ["BigHex2Short:r/1000", 2, "Voltage_Cell05", "V"],
            ["discard", 1, "Voltage_Cell06", ""],
            ["BigHex2Short:r/1000", 2, "Voltage_Cell06", "V"],
            ["discard", 1, "Voltage_Cell07", ""],
            ["BigHex2Short:r/1000", 2, "Voltage_Cell07", "V"],
            ["discard", 1, "Voltage_Cell08", ""],
            ["BigHex2Short:r/1000", 2, "Voltage_Cell08", "V"],
            ["discard", 1, "Voltage_Cell09", ""],
            ["BigHex2Short:r/1000", 2, "Voltage_Cell09", "V"],
            ["discard", 1, "Voltage_Cell10", ""],
            ["BigHex2Short:r/1000", 2, "Voltage_Cell10", "V"],
            ["discard", 1, "Voltage_Cell11", ""],
            ["BigHex2Short:r/1000", 2, "Voltage_Cell11", "V"],
            ["discard", 1, "Voltage_Cell12", ""],
            ["BigHex2Short:r/1000", 2, "Voltage_Cell12", "V"],
            ["discard", 1, "Voltage_Cell13", ""],
            ["BigHex2Short:r/1000", 2, "Voltage_Cell13", "V"],
            ["discard", 1, "Voltage_Cell14", ""],
            ["BigHex2Short:r/1000", 2, "Voltage_Cell14", "V"],
            ["discard", 1, "Voltage_Cell15", ""],
            ["BigHex2Short:r/1000", 2, "Voltage_Cell15", "V"],
            ["discard", 1, "Voltage_Cell16", ""],
            ["BigHex2Short:r/1000", 2, "Voltage_Cell16", "V"],
            ["discard", 1, "MOS_Temp", ""],
            ["BigHex2Short", 2, "MOS_Temp", "°C"],
            ["discard", 1, "Battery_T1", ""],
            ["BigHex2Short", 2, "Battery_T1", "°C"],
            ["discard", 1, "Battery_T2", ""],
            ["BigHex2Short", 2, "Battery_T2", "°C"],
            ["discard", 1, "Battery_Voltage", ""],
            ["BigHex2Short:r/100", 2, "Battery_Voltage", "V"],
            ["discard", 1, "Battery_Current", ""],
            ["BigHex2Short:(r&0x7FFF)/100*(((r&0x8000)>>15)*2-1)", 2, "Battery_Current", "A"],
            ["discard", 1, "Percent_Remain", ""],
            ["Hex2Int", 1, "Percent_Remain", "%"],
            ["discard", 2, "Number of battery sensors", ""],  # useless so dropped
            ["discard", 1, "Cycle_Count", ""],
            ["BigHex2Short", 2, "Cycle_Count", ""],
            ["discard", 1, "Total_capacity", ""],
            ["BigHex2Float", 4, "Total_capacity", "Ahr"], # Needs other formula
            ["discard", 3, "Total number of battery strings", ""],  # dropping
            ["discard", 1, "Battery Warning Message", ""],
            ["Hex2Str", 2, "Battery Warning Message", ""],
            ["discard", 1, "Battery status information", ""],
            ["Hex2Str", 2, "Battery status information", ""],
            ["discard", 15 * 3, "settings", ""],
            ["discard", 1, "Balancer Active", ""],
            ["Hex2Int", 1, "Balancer Active", ""],
            ["discard", 7 * 3, "more settings", ""],
            ["discard", 4 * 3, "temp settings", ""],
            ["discard", 2, "string count", ""], # dropping
            ["discard", 1, "Capacity Setting", ""],
            ["BigHex2Float", 4, "Capacity Setting", "Ahr"],
            ["discard", 1, "Charge Enabled", ""],
            ["Hex2Int", 1, "Charge Enabled", ""],
            ["discard", 1, "Discharge Enabled", ""],
            ["Hex2Int", 1, "Discharge Enabled", ""],
            ["discard", 20 + 96, "remaining data", ""]
        ],
        "test_responses": [
            bytes.fromhex("4e 57 01 1b 00 00 00 00 03 00 01 79 2a 01 0f 91 02 0f 94 03 0f 99 04 0f 92 05 0f 94 06 0f 94 07 0f 94 08 0f 91 09 0f 96 0a 0f 91 0b 0f 92 0c 0f 93 0d"),
            b'NW\x01\x1b\x00\x00\x00\x00\x03\x00\x01y*\x01\x0f\x90\x02\x0f\x91\x03\x0f\x94\x04\x0f\x8e\x05\x0f\x92\x06\x0f\x91\x07\x0f\x91\x08\x0f\x91\t\x0f\x93\n\x0f\x8e\x0b\x0f\x91\x0c\x0f\x90\r\x0f\x90\x0e\x0f\x8d\x80\x00!\x81\x00\x1c\x82\x00\x1e\x83\x15\xca\x84\x81\xc5\x85d\x86\x02\x87\x00\x19\x89\x00\x00\x16\xda\x8a\x00\x0e\x8b\x00\x00\x8c\x00\x03\x8e\x16\xb2\x8f\x10\xf4\x90\x106\x91\x10\x04\x92\x00\x05\x93\x0c\x1c\x94\x0c\x80\x95\x00\x05\x96\x01,\x97\x00n\x98\x01,\x99\x00U\x9a\x00\x1e\x9b\x0b\xb8\x9c\x002\x9d\x01\x9e\x00Z\x9f\x00F\xa0\x00d\xa1\x00d\xa2\x00\x14\xa3\x00<\xa4\x00<\xa5\x00\x01\xa6\x00\x03\xa7\xff\xec\xa8\xff\xf6\xa9\x0e\xaa\x00\x00\x00\xea\xab\x01\xac\x01\xad\x047\xae\x01\xaf\x01\xb0\x00\n\xb1\x14\xb2123456\x00\x00\x00\x00\xb3\x00\xb4Input Us\xb52306\xb6\x00\x01\x82\xe3\xb711.XW_S11.261__\xb8\x00\xb9\x00\x00\x00\xea\xbaInput UserdaJK_B1A20S15P\xc0\x01\x00\x00\x00\x00h\x00\x00Q\xd6'
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
        log.debug(f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands")
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

import logging

from .jkabstractprotocol import jkAbstractProtocol


log = logging.getLogger("jk02")

NEW_COMMANDS = {
    "getCellData": {
        "name": "getCellData",
        "command_code": "96",
        "record_type": "2",
        "description": "BLE Cell Data inquiry",
        "help": " -- queries the ble device for the cell data",
        "type": "QUERY",
        "response": [
            ["hex", 4, "Header", ""],
            ["hex", 1, "Record_Type", ""],
            ["int", 1, "Record_Counter", ""],
            ["loop", 24, "Voltage_Cell", "V", "2ByteHex"],
            ["discard", 4, "discard1", ""],
            ["2ByteHex", 1, "Average_Cell_Voltage", "V"],
            ["2ByteHex", 1, "Delta_Cell_Voltage", "V"],
            ["2ByteHex", 1, "Current_Balancer", ""],
            ["loop", 24, "Resistance_Cell", "Ohm", "2ByteHex"],
            ["discard", 6, "discard2", ""],
            ["4ByteHex1000", 1, "Battery_Voltage", "V"],
            ["discard", 8, "discard3", ""],
            ["2ByteHexC", 1, "Battery_T1", "°C"],
            ["2ByteHexC", 1, "Battery_T2", "°C"],
            ["2ByteHexC", 1, "MOS_Temp", "°C"],
            ["discard", 4, "discard4", ""],  # discard4
            ["discard", 1, "discard4_1", ""],  # added
            ["int", 1, "Percent_Remain", ""],  # Unknown5
            ["4ByteHex1000", 4, "Capacity_Remain", ""],  # Unknown6+7
            ["4ByteHex1000", 4, "Nominal_Capacity", ""],  # Unknown8+9
            ["discard", 4, "discard5", ""],
            # ["discard", 2, "Unknown10", ""],
            # ["discard", 2, "Unknown11", ""],
            ["4ByteHex1000", 4, "Capacity_Cycle", ""],  # Unknown10+11
            ["discard", 2, "Unknown12", ""],
            ["discard", 2, "Unknown13", ""],
            ["uptime", 3, "Time", ""],
            ["discard", 2, "Unknown15", ""],
            ["discard", 2, "Unknown16", ""],
            ["discard", 2, "Unknown17", ""],
            ["discard", 12, "discard6", ""],
            ["discard", 2, "Unknown18", ""],
            ["discard", 2, "Unknown19", ""],
            ["discard", 2, "Unknown20", ""],
            ["2ByteHex", 1, "Current_Charge", ""],  # Unknown21
            ["2ByteHex", 1, "Current_Discharge", ""],  # Unknown22
            ["discard", 2, "Unknown23", ""],
            ["discard", 2, "Unknown24", ""],
            ["discard", 2, "Unknown25", ""],
            ["discard", 2, "Unknown26", ""],
            ["discard", 2, "Unknown27", ""],
            ["discard", 2, "Unknown28", ""],
            ["discard", 2, "Unknown29", ""],
            ["rem"],
        ],
        "test_responses": [
            bytes.fromhex(
                "55aaeb9002b52e0d280dfa0c2e0d2f0d220d220d130d190d1d0d1d0d170d1f0d160dfb0c1f0d00000000000000000000000000000000ffff00001c0d350004029b00c600a000b300bc00cc00be00b100b4002d013d01b000a100ab00b200ad0000000000000000000000000000000000000000000000bcd1000000000000000000001e0116013c010000000000636b0c0300400d030000000000dc4d010064000000781e16000101480a000000000000000000000000070101000000980400000000260141400000000037feffff00000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000080"
            ),
            bytes.fromhex(
                "55aaeb9002bb2e0d280dfa0c2e0d2f0d220d220d130d190d1d0d1d0d170d1f0d160dfb0c1f0d00000000000000000000000000000000ffff00001b0d350004029b00c600a000b300bc00cc00be00b100b4002d013d01b000a100ab00b200ad0000000000000000000000000000000000000000000000b8d1000000000000000000001e0114013c010000000000636b0c0300400d030000000000dc4d0100640000007a1e16000101480a000000000000000000000000070101000000980400000000260141400000000037feffff00000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000081"
            ),
            bytes.fromhex(
                "55 AA EB 90 02 10 AD 0E 52 0E 53 0E 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 07 00 00 00 70 0E 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 51 2B 00 00 00 00 00 00 00 00 00 00 30 F8 30 F8 53 01 00 00 0C 01 00 00 C2 14 00 00 70 17 00 00 00 00 00 00 8F 01 00 00 00 00 51 07 AF 69 00 00 00 00 CB 06 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 11 04 00 00 00 00 92 4A 3B 40 00 00 00 00 AD 08 00 00 00 00 00 01 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0C"
            ),
            b"U\xaa\xeb\x90\x02\xa7\xd8\x0e\xd8\x0e\xd7\x0e\xd8\x0e\xd8\x0e\xda\x0e\xd7\x0e\xda\x0e\xd7\x0e\xd8\x0e\xd8\x0e\xd8\x0e\xc3\x0e\xda\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff?\x00\x00\xd7\x0e\x19\x00\x0c\x02m\x00n\x00o\x00n\x00o\x00m\x00p\x00l\x00l\x00l\x00l\x00l\x00o\x00l\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc1\xcf\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf5\x00\xda\x00\x05\x01\x00\x00\x02\xf9\x02EN!\x00\x00\xc7\x00\x00\x03\x00\x00\x00\x87\x91\x00\x00W\x00)\x03\x16\x11\x04\x00\x01\x01\xa8\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x01\x00\x00\x00\x11\x04\x00\x00\x00\x00\xee(@@\x7f\x00\x00\x00i\xfd\xff\xff\x00\x00\x00\x01\x00\x01\x00\x00t\xa3(\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00F",
        ],
    },
}


class jk02(jkAbstractProtocol):
    """
    JK02 - Handler for JKBMS 2 byte data communication
         - e.g. ASAS = ??V
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"JK02"
        self.COMMANDS.update(NEW_COMMANDS)
        self.STATUS_COMMANDS = [
            "getCellData",
        ]
        self.SETTINGS_COMMANDS = [
            "getInfo",
        ]
        self.DEFAULT_COMMAND = "getCellData"

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
        "response_type": "POSITIONAL",
        "response": [
            ["Hex2Str", 4, "Header", ""],
            ["Hex2Str", 1, "Record_Type", ""],
            ["Hex2Int", 1, "Record_Counter", ""],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell01", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell02", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell03", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell04", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell05", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell06", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell07", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell08", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell09", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell10", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell11", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell12", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell13", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell14", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell15", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell16", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell17", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell18", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell19", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell20", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell21", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell22", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell23", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell24", "V"],
            ["discard", 4, "discard1", ""],
            ["LittleHex2Short:r/1000", 2, "Average_Cell_Voltage", "V"],
            ["LittleHex2Short:r/1000", 2, "Delta_Cell_Voltage", "V"],
            ["LittleHex2Short:r/1000", 2, "Current_Balancer", ""],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell01", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell02", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell03", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell04", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell05", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell06", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell07", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell08", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell09", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell10", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell11", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell12", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell13", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell14", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell15", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell16", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell17", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell18", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell19", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell20", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell21", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell22", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell23", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell24", "Ohm"],
            ["discard", 6, "discard2", ""],
            ["LittleHex2UInt:r/1000", 4, "Battery_Voltage", "V"],
            ["LittleHex2UInt", 4, "Battery_Power", "W"],
            ["LittleHex2Int:r/1000", 4, "Balance_Current", "A"],  # signed int32
            # ["discard", 8, "discard3", ""],
            ["LittleHex2Short:r/10", 2, "Battery_T1", "°C"],
            ["LittleHex2Short:r/10", 2, "Battery_T2", "°C"],
            ["LittleHex2Short:r/10", 2, "MOS_Temp", "°C"],
            ["discard", 4, "discard4", ""],  # discard4
            ["discard", 1, "discard4_1", ""],  # added
            ["Hex2Int", 1, "Percent_Remain", "%"],
            ["LittleHex2UInt:r/1000", 4, "Capacity_Remain", "Ah"],  # Unknown6+7
            ["LittleHex2UInt:r/1000", 4, "Nominal_Capacity", "Ah"],  # Unknown8+9
            ["LittleHex2UInt", 4, "Cycle_Count", ""],
            # ["discard", 2, "Unknown10", ""],
            # ["discard", 2, "Unknown11", ""],
            ["LittleHex2UInt:r/1000", 4, "Cycle_Capacity", "Ah"],  # Unknown10+11
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
            ["LittleHex2Short:r/1000", 2, "Current_Charge", ""],  # Unknown21
            ["LittleHex2Short:r/1000", 2, "Current_Discharge", ""],  # Unknown22
            ["discard", 2, "Unknown23", ""],
            ["discard", 2, "Unknown24", ""],
            ["discard", 2, "Unknown25", ""],
            ["discard", 2, "Unknown26", ""],
            ["discard", 2, "Unknown27", ""],
            ["discard", 2, "Unknown28", ""],
            ["discard", 2, "Unknown29", ""],
            ["discard", 93, "Unknown30", ""],
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
            bytearray(
                b"U\xaa\xeb\x90\x02\xee\xc3\x0e\xc0\x0e\xd2\x0e\xb6\x0e\xce\x0e\xc6\x0e\xc0\x0e\xbd\x0e\xcb\x0e\xcd\x0e\xc1\x0e\xd2\x0e\xc0\x0e\xc6\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff?\x00\x00\xc6\x0e\x18\x00\x06\x05}\x00u\x00q\x00s\x00q\x00i\x00h\x00k\x00l\x00g\x00e\x00\x80\x00\x85\x00h\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd9\xce\x00\x00\x1a\x83\x05\x00Z\xe5\xff\xff:\x01\xc7\x00\r\x01\x00\x00&\xf9\x02S\xa5\x1b\x02\x00p\x88\x02\x00\x13\x00\x00\x00\xc3\xfe1\x00d\x00\xef\x02.\xb8\x8b\x00\x01\x01\\\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x01\x00\x00\x00*\x04\x00\x00 \x00\xcb'A@\x90\x00\x00\x00\x05\xff\xff\xff\x00\x00\x00\x01\x00\x03\x00\x00b\x8f\xaf\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00L"
            ),
            bytearray(
                b"U\xaa\xeb\x90\x02\x86;\x0eD\x0e:\x0eD\x0e6\x0e>\x0eB\x0e>\x0eB\x0e:\x0e>\x0eD\x0eD\x0e<\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff?\x00\x00?\x0e\x0c\x00\x0c\x04}\x00u\x00q\x00s\x00q\x00i\x00h\x00k\x00l\x00g\x00e\x00\x80\x00\x85\x00h\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00n\xc7\x00\x00.\xa9\x01\x00\x82\xf8\xff\xff\x04\x01\xc9\x00\t\x01\x00\x008\xf8\x02:4x\x01\x00p\x88\x02\x00\x13\x00\x00\x004\xa22\x00d\x00{\x02s-\x8c\x00\x01\x01_\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x01\x00\x00\x00*\x04\x00\x00\t\x00\xcb'A@\xa5\x00\x00\x00\x05\xff\xff\xff\x00\x00\x00\x01\x00\x03\x00\x00\x17$\xb4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00O"
            ),
        ],
    },
    "setCellOVP": {
        "name": "setCellOVP",
        "command_code": "04",
        "record_type": "2",
        "description": "Set cell over voltage protection",
        "help": " -- example setCellOVP3.65",
        "type": "SETTER",
        "response_type": "POSITIONAL",
        "response": [["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [
            bytes.fromhex(
                "55aaeb9002b52e0d280dfa0c2e0d2f0d220d220d130d190d1d0d1d0d170d1f0d160dfb0c1f0d00000000000000000000000000000000ffff00001c0d350004029b00c600a000b300bc00cc00be00b100b4002d013d01b000a100ab00b200ad0000000000000000000000000000000000000000000000bcd1000000000000000000001e0116013c010000000000636b0c0300400d030000000000dc4d010064000000781e16000101480a000000000000000000000000070101000000980400000000260141400000000037feffff00000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000080"
            ),
        ],
        "regex": "setCellOVP(\\d\\.\\d*)$",
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

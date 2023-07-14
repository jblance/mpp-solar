import logging

from .jkabstractprotocol import jkAbstractProtocol


log = logging.getLogger("jkv11")

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
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell25", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell26", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell27", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell28", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell29", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell30", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell31", "V"],
            ["LittleHex2Short:r/1000", 2, "Voltage_Cell32", "V"],
            ["discard", 4, "discard1", ""],
            ["LittleHex2Short:r/1000", 2, "Average_Cell_Voltage", "V"],
            ["LittleHex2Short:r/1000", 2, "Delta_Cell_Voltage", "V"],
            ["LittleHex2Short:r/1000", 2, "Current_Balancer", "A"],
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
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell25", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell26", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell27", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell28", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell29", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell30", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell31", "Ohm"],
            ["LittleHex2Short:r/1000", 2, "Resistance_Cell32", "Ohm"],
            ["discard", 6, "discard2", ""],
            ["LittleHex2UInt:r/1000", 4, "Battery_Voltage", "V"],
            ["LittleHex2UInt:r/1000", 4, "Battery_Power", "W"],
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
            ["LittleHex2Short:r/1000", 2, "Current_Charge", "A"],  # Unknown21
            ["LittleHex2Short:r/1000", 2, "Current_Discharge", "A"],  # Unknown22
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
            b'U\xaa\xeb\x90\x02\xdc\xfd\x0c\xfd\x0c\xfd\x0c\xfd\x0c\xfe\x0c\xfe\x0c\xfd\x0c\xfd\x0c\xfd\x0c\xfd\x0c\xfd\x0c\xfe\x0c\xfe\x0c\xfe\x0c\xfe\x0c\xfe\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\xfe\x0c\x04\x00\x05\n2\x002\x002\x002\x001\x002\x001\x001\x001\x001\x001\x001\x001\x001\x001\x001\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf3\x00\x00\x00\x00\x00\xdc\xcf\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc5\x00\xcb\x00\x00\x00\x08\x00\x00\x00\x00Tn\xe1\x03\x00\xb0\x9b\x04\x00\x08\x00\x00\x00\xb3A)\x00d\x00\x00\x00\x12\xdeC\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x01\x00\x00\x00m\x04\x00\x00\x00\x00\xa3\xd2A@\x00\x00\x00\x00\xc9\x14X\x1c\x00\x01\x00\x01\x00\x05\x00\x00\xa77<\x01\x00\x00\x00\x00\xf3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfe\xff\x7f\xdc/\x01\x01\x01\x00\x00\x00\x00_',
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
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}]
        ],
        "test_responses": [
            bytes.fromhex(
                "55aaeb9002b52e0d280dfa0c2e0d2f0d220d220d130d190d1d0d1d0d170d1f0d160dfb0c1f0d00000000000000000000000000000000ffff00001c0d350004029b00c600a000b300bc00cc00be00b100b4002d013d01b000a100ab00b200ad0000000000000000000000000000000000000000000000bcd1000000000000000000001e0116013c010000000000636b0c0300400d030000000000dc4d010064000000781e16000101480a000000000000000000000000070101000000980400000000260141400000000037feffff00000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000080"
            ),
        ],
        "regex": "setCellOVP(\\d\\.\\d*)$",
    },
}


class jkv11(jkAbstractProtocol):
    """
    JKv11 - Handler for JKBMS 2 byte data communication
         - e.g. ASAS = ??V
    """

    def __str__(self):
        return "JKBMS BLE communication protocol handler software v11.x"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"JKv11"
        self.COMMANDS.update(NEW_COMMANDS)
        self.STATUS_COMMANDS = [
            "getCellData",
        ]
        self.SETTINGS_COMMANDS = [
            "getInfo",
        ]
        self.DEFAULT_COMMAND = "getCellData"

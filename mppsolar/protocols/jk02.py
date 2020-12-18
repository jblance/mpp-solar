import logging

from .jkabstractprotocol import jkAbstractProtocol


log = logging.getLogger("MPP-Solar")

NEW_COMMANDS = {
    "getCellData": {
        "name": "getCellData",
        "command_code": "96",
        "description": "BLE Cell Data inquiry",
        "help": " -- queries the ble device for the cell data",
        "type": "QUERY",
        "response": [
            ["hex", 4, "Header", ""],
            ["hex", 1, "Record Type", ""],
            ["int", 1, "Record Counter", ""],
            ["loop", 24, "Voltage Cell", "V", "2ByteHex"],
            ["rem"],
            ["loop", 25, "Resistance Cell", "Ohm", "4ByteHex"],
            ["4ByteHex", 1, "Average Cell Voltage", "V"],
            ["4ByteHex", 1, "Delta Cell Voltage", "V"],
            ["4ByteHex", 1, "Balance Current", "A"],
            ["discard", 20, "", ""],
            ["4ByteHex", 1, "Unknown1", ""],
            ["discard", 52, "", ""],
            ["4ByteHex", 1, "Unknown2", ""],
            ["4ByteHex", 1, "Unknown3", ""],
        ],
        "test_responses": [
            bytes.fromhex(
                "55aaeb9002b52e0d280dfa0c2e0d2f0d220d220d130d190d1d0d1d0d170d1f0d160dfb0c1f0d00000000000000000000000000000000ffff00001c0d350004029b00c600a000b300bc00cc00be00b100b4002d013d01b000a100ab00b200ad0000000000000000000000000000000000000000000000bcd1000000000000000000001e0116013c010000000000636b0c0300400d030000000000dc4d010064000000781e16000101480a000000000000000000000000070101000000980400000000260141400000000037feffff00000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000080"
            ),
        ],
        "regex": "",
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
        self.DEFAULT_COMMAND = "getInfo"

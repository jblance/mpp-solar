import logging

from .jkabstractprotocol import jkAbstractProtocol


log = logging.getLogger("jk04")

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
            ["Hex2Str", 1, "Record Type", ""],
            ["Hex2Int", 1, "Record Counter", ""],
            ["LittleHex2Float", 4, "Voltage Cell01", "V"],
            ["LittleHex2Float", 4, "Voltage Cell02", "V"],
            ["LittleHex2Float", 4, "Voltage Cell03", "V"],
            ["LittleHex2Float", 4, "Voltage Cell04", "V"],
            ["LittleHex2Float", 4, "Voltage Cell05", "V"],
            ["LittleHex2Float", 4, "Voltage Cell06", "V"],
            ["LittleHex2Float", 4, "Voltage Cell07", "V"],
            ["LittleHex2Float", 4, "Voltage Cell08", "V"],
            ["LittleHex2Float", 4, "Voltage Cell09", "V"],
            ["LittleHex2Float", 4, "Voltage Cell10", "V"],
            ["LittleHex2Float", 4, "Voltage Cell11", "V"],
            ["LittleHex2Float", 4, "Voltage Cell12", "V"],
            ["LittleHex2Float", 4, "Voltage Cell13", "V"],
            ["LittleHex2Float", 4, "Voltage Cell14", "V"],
            ["LittleHex2Float", 4, "Voltage Cell15", "V"],
            ["LittleHex2Float", 4, "Voltage Cell16", "V"],
            ["LittleHex2Float", 4, "Voltage Cell17", "V"],
            ["LittleHex2Float", 4, "Voltage Cell18", "V"],
            ["LittleHex2Float", 4, "Voltage Cell19", "V"],
            ["LittleHex2Float", 4, "Voltage Cell20", "V"],
            ["LittleHex2Float", 4, "Voltage Cell21", "V"],
            ["LittleHex2Float", 4, "Voltage Cell22", "V"],
            ["LittleHex2Float", 4, "Voltage Cell23", "V"],
            ["LittleHex2Float", 4, "Voltage Cell24", "V"],
            ["LittleHex2Float", 4, "Resistance Cell01", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell02", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell03", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell04", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell05", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell06", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell07", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell08", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell09", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell10", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell11", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell12", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell13", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell14", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell15", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell16", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell17", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell18", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell19", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell20", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell21", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell22", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell23", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell24", "Ohm"],
            ["LittleHex2Float", 4, "Resistance Cell25", "Ohm"],
            ["LittleHex2Float", 4, "Average Cell Voltage", "V"],
            ["LittleHex2Float", 4, "Delta Cell Voltage", "V"],
            ["discard", 4, "", ""],
            ["discard", 4, "", ""],
            ["Hex2Int:r+1", 1, "Highest Cell", ""],
            ["Hex2Int:r+1", 1, "Lowest Cell", ""],
            ["Hex2Str", 2, "Flags", ""],
            ["discard", 4, "", ""],
            ["discard", 7, "", ""],
            ["discard", 4, "", ""],
            ["discard", 4, "", ""],
            ["discard", 45, "", ""],
            ["uptime", 3, "uptime", ""],
            ["discard", 5, "", ""],
            ["discard", 4, "", ""],
            ["discard", 1, "", ""],
            ["Hex2Str", 1, "Checksum", ""],
            [
                "lookup:'Voltage Cell{:02d}'.format(m['Highest Cell'][0])",
                0,
                "Highest Cell Voltage",
                "V",
            ],
            [
                "lookup:'Voltage Cell{:02d}'.format(m['Lowest Cell'][0])",
                0,
                "Lowest Cell Voltage",
                "V",
            ],
        ],
        "test_responses": [
            bytes.fromhex(
                "55aaeb9002ff5b566240e34e62406e6a62404a506240acd7624011d26240bddd62409ad1624044c86240cedc6240ccc7624079e1624057dc624073a262405f80624088c46240000000000000000000000000000000000000000000000000000000000000000013315c3d0636143d26e0113d8021f03c1153363d8980123d7e7c033dac41233d1ad83c3d9d6f4f3d8eb51e3d6a2c293deb28653d189c523da3724e3deb94493d9ab2c23d00000000000000000000000000000000000000000000000000000000000000001aad62400084053c00000000ffff00000b000000000000000000000000000036a3554c40000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000be0b54001456a43fb876a43f00a2"
            ),
            b"U\xaa\xeb\x90\x02\xfd\x01\x04\x13@\x81\xbc\x16@E\xd2\x10@\xed\xd4\x16@\xed\xd4\x16@2\x1e\x17@\xa8\x10\x14@\xe3\x7f\x17@\x15\xa4\x16@\xf7)\x16@2\x1e\x17@\xb1\xf4\x0b@2\xa3\x14@\x9eJ\r@\x9e\xc5\x0f@\xa8\x8b\x16@\x9e6\x17@\xc6\x05\x17@\xe3\x7f\x17@Y\xed\x16@\xe3\x7f\x17@\xcf\xdf\x13@Y\xed\x16@2\xa3\x14@\xab\xe5p>Yk2>&\xef\xf6=>\xb84>p\xfc~>\xab9\xbc>\xde\xd3\xb6>25\x80>672>\xaeG\xf7=\x86\xc4\xfa=g,\x02>\xf6&\x02>\x97S\x01>\xd8\x1d\x01>\x94%\x05>JF\x00>\x8f\xd83>\xe0a\x92>\x05\xf2\xaa>\xd2\xbaU>\xad\xc0\xf8=\xee\x88\xf7=\xd5\xa2@>\x00\x00\x00\x00\x92\xf2\x14@P,7>\x00\x00\x00\x00\xff\xff\xff\x00\x07\x0b\x01\x01\x00X\xb6?\x00\x00\x00\x00\x00\x00\x00Z{\xedK@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\xd2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa0/\x00\x00\x00\x00\x00\x00\x00X*@\x00\x0b",
            b"U\xaa\xeb\x90\x02\x12O\xa2\x12@\xa8\x8b\x16@\x94p\x10@\xed\xd4\x16@<s\x16@\xed\xd4\x16@\xf7\xae\x13@\xb2\xe0\x15@\x0bO\x17@wg\x17@\x0bO\x17@\x00\x93\x0b@Yr\x14@\xec\xe8\x0c@\xedc\x0f@2\x1e\x17@\xc6\x05\x17@\x81\xbc\x16@\xbc\xb0\x17@\xa8\x8b\x16@\xbc\xb0\x17@\x8a\x96\x13@\x81\xbc\x16@Yr\x14@\xab\xe5p>Yk2>&\xef\xf6=>\xb84>p\xfc~>\xab9\xbc>\xde\xd3\xb6>25\x80>672>\xaeG\xf7=\x86\xc4\xfa=g,\x02>\xf6&\x02>\x97S\x01>\xd8\x1d\x01>\x94%\x05>JF\x00>\x8f\xd83>\xe0a\x92>\x05\xf2\xaa>\xd2\xbaU>\xad\xc0\xf8=\xee\x88\xf7=\xd5\xa2@>\x00\x00\x00\x00\n\xd4\x14@@\xce>>\x00\x00\x00\x00\xff\xff\xff\x00\x07\x0b\x02\x01\x004\x00\xc0\x00\x00\x00\x00\x00\x00\x00\xf6\xc1\xe7K@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\xc9\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd08\x00\x00\x00\x00\x00\x00\x00(*@\x00\xea",
        ],
    },
}


class jk04(jkAbstractProtocol):
    """
    JK04 - Handler for JKBMS 4 byte data communication
         - e.g. 5b566240 = 3.5365V
    """

    def __str__(self):
        return "JK04 - JKBMS BLE 4 byte data communication protocol handler"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"JK04"
        self.COMMANDS.update(NEW_COMMANDS)
        self.STATUS_COMMANDS = [
            "getCellData",
        ]
        self.SETTINGS_COMMANDS = [
            "getInfo",
        ]
        self.DEFAULT_COMMAND = "getCellData"

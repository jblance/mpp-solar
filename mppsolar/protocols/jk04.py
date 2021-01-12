import logging

from .jkabstractprotocol import jkAbstractProtocol


log = logging.getLogger("MPP-Solar")

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
            ["hex", 1, "Record Type", ""],
            ["int", 1, "Record Counter", ""],
            ["loop", 24, "Voltage Cell", "V", "4ByteHex"],
            ["loop", 25, "Resistance Cell", "Ohm", "4ByteHex"],
            ["4ByteHex", 1, "Average Cell Voltage", "V"],
            ["4ByteHex", 1, "Delta Cell Voltage", "V"],
            ["hex", 4, "Unknown", ""],
            ["hex", 4, "unk1", ""],
            ["4ByteHexU", 1, "unk2", ""],
            ["hex", 4, "unk3", ""],
            ["discard", 4, "disc", ""],
            ["hex", 4, "unk4", ""],
            ["4ByteHexU", 1, "Unknown1", ""],
            ["discard", 48, "discard", ""],
            ["uptime", 3, "uptime", ""],
            ["discard", 1, "disc2", ""],
            ["4ByteHexU", 1, "Unknown3", ""],
            ["4ByteHexU", 1, "Unknown4", ""],
            ["rem"],
        ],
        "test_responses": [
            bytes.fromhex(
                "55aaeb9002ff5b566240e34e62406e6a62404a506240acd7624011d26240bddd62409ad1624044c86240cedc6240ccc7624079e1624057dc624073a262405f80624088c46240000000000000000000000000000000000000000000000000000000000000000013315c3d0636143d26e0113d8021f03c1153363d8980123d7e7c033dac41233d1ad83c3d9d6f4f3d8eb51e3d6a2c293deb28653d189c523da3724e3deb94493d9ab2c23d00000000000000000000000000000000000000000000000000000000000000001aad62400084053c00000000ffff00000b000000000000000000000000000036a3554c40000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000be0b54001456a43fb876a43f00a2"
            ),
        ],
        "regex": "",
    },
}


class jk04(jkAbstractProtocol):
    """
    JK04 - Handler for JKBMS 4 byte data communication
         - e.g. 5b566240 = 3.5365V
    """

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

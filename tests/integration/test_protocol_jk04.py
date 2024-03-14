import unittest
from mppsolar.protocols.jk04 import jk04 as pi


class test_jk04_decode(unittest.TestCase):
    maxDiff = None

    def test_getInfo(self):
        """test the decode of a getInfo response"""
        protocol = pi()
        response = bytes.fromhex(
            "55aaeb9003f14a4b2d42324132345300000000000000332e300000000000332e322e330000000876450004000000506f7765722057616c6c203100000000313233340000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c2"
        )
        command = "getInfo"
        expected = {
            "raw_response": [
                "Uªë\x90\x03ñJK-B2A24S\x00\x00\x00\x00\x00\x00\x003.0\x00\x00\x00\x00\x003.2.3\x00\x00\x00\x08vE\x00\x04\x00\x00\x00Power Wall 1\x00\x00\x00\x001234\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Â",
                "",
            ],
            "_command": "getInfo",
            "_command_description": "BLE Device Information inquiry",
            "Header": ["55aaeb90", ""],
            "Record Type": ["03", ""],
            "Record Counter": [241, ""],
            "Device Model": ["JK-B2A24S", ""],
            "Hardware Version": ["3.0", ""],
            "Software Version": ["3.2.3", ""],
            "Device Name": ["Power Wall 1", ""],
            "Device Passcode": ["1234", ""],
            "Manufacturing Date": ["", ""],
            "Serial Number": ["", ""],
            "User Data": ["", ""],
            "Setup Passcode": ["", ""],
            "Passcode": ["", ""],
            "Power-on Times": [4, ""],
            "Up Time": ["52D16H30M0S", ""],
        }
        protocol.get_full_command(command)
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)

    def test_getCellData(self):
        """test the decode of a getCellData response"""
        protocol = pi()
        response = b"U\xaa\xeb\x90\x02\xfd\x01\x04\x13@\x81\xbc\x16@E\xd2\x10@\xed\xd4\x16@\xed\xd4\x16@2\x1e\x17@\xa8\x10\x14@\xe3\x7f\x17@\x15\xa4\x16@\xf7)\x16@2\x1e\x17@\xb1\xf4\x0b@2\xa3\x14@\x9eJ\r@\x9e\xc5\x0f@\xa8\x8b\x16@\x9e6\x17@\xc6\x05\x17@\xe3\x7f\x17@Y\xed\x16@\xe3\x7f\x17@\xcf\xdf\x13@Y\xed\x16@2\xa3\x14@\xab\xe5p>Yk2>&\xef\xf6=>\xb84>p\xfc~>\xab9\xbc>\xde\xd3\xb6>25\x80>672>\xaeG\xf7=\x86\xc4\xfa=g,\x02>\xf6&\x02>\x97S\x01>\xd8\x1d\x01>\x94%\x05>JF\x00>\x8f\xd83>\xe0a\x92>\x05\xf2\xaa>\xd2\xbaU>\xad\xc0\xf8=\xee\x88\xf7=\xd5\xa2@>\x00\x00\x00\x00\x92\xf2\x14@P,7>\x00\x00\x00\x00\xff\xff\xff\x00\x07\x0b\x01\x01\x00X\xb6?\x00\x00\x00\x00\x00\x00\x00Z{\xedK@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\xd2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa0/\x00\x00\x00\x00\x00\x00\x00X*@\x00\x0b"
        command = "getCellData"
        expected = {
            "raw_response": [
                "Uªë\x90\x02ý\x01\x04\x13@\x81¼\x16@EÒ\x10@íÔ\x16@íÔ\x16@2\x1e\x17@¨\x10\x14@ã\x7f\x17@\x15¤\x16@÷)\x16@2\x1e\x17@±ô\x0b@2£\x14@\x9eJ\r@\x9eÅ\x0f@¨\x8b\x16@\x9e6\x17@Æ\x05\x17@ã\x7f\x17@Yí\x16@ã\x7f\x17@Ïß\x13@Yí\x16@2£\x14@«åp>Yk2>&ïö=>¸4>pü~>«9¼>ÞÓ¶>25\x80>672>®G÷=\x86Äú=g,\x02>ö&\x02>\x97S\x01>Ø\x1d\x01>\x94%\x05>JF\x00>\x8fØ3>àa\x92>\x05òª>ÒºU>\xadÀø=î\x88÷=Õ¢@>\x00\x00\x00\x00\x92ò\x14@P,7>\x00\x00\x00\x00ÿÿÿ\x00\x07\x0b\x01\x01\x00X¶?\x00\x00\x00\x00\x00\x00\x00Z{íK@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00Ò\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa0/\x00\x00\x00\x00\x00\x00\x00X*@\x00\x0b",
                "",
            ],
            "_command": "getCellData",
            "_command_description": "BLE Cell Data inquiry",
            "Header": ["55aaeb90", ""],
            "Record Type": ["02", ""],
            "Record Counter": [253, ""],
            "Voltage Cell01": [2.297119379043579, "V"],
            "Voltage Cell02": [2.355255365371704, "V"],
            "Voltage Cell03": [2.262833833694458, "V"],
            "Voltage Cell04": [2.356745958328247, "V"],
            "Voltage Cell05": [2.356745958328247, "V"],
            "Voltage Cell06": [2.361217975616455, "V"],
            "Voltage Cell07": [2.313516616821289, "V"],
            "Voltage Cell08": [2.367180585861206, "V"],
            "Voltage Cell09": [2.353764772415161, "V"],
            "Voltage Cell10": [2.346311330795288, "V"],
            "Voltage Cell11": [2.361217975616455, "V"],
            "Voltage Cell12": [2.186809778213501, "V"],
            "Voltage Cell13": [2.322460651397705, "V"],
            "Voltage Cell14": [2.207679271697998, "V"],
            "Voltage Cell15": [2.246436595916748, "V"],
            "Voltage Cell16": [2.352273941040039, "V"],
            "Voltage Cell17": [2.362708568572998, "V"],
            "Voltage Cell18": [2.359727382659912, "V"],
            "Voltage Cell19": [2.367180585861206, "V"],
            "Voltage Cell20": [2.35823655128479, "V"],
            "Voltage Cell21": [2.367180585861206, "V"],
            "Voltage Cell22": [2.310535192489624, "V"],
            "Voltage Cell23": [2.35823655128479, "V"],
            "Voltage Cell24": [2.322460651397705, "V"],
            "Resistance Cell01": [0.23525111377239227, "Ohm"],
            "Resistance Cell02": [0.17423762381076813, "Ohm"],
            "Resistance Cell03": [0.12057332694530487, "Ohm"],
            "Resistance Cell04": [0.17648407816886902, "Ohm"],
            "Resistance Cell05": [0.2490098476409912, "Ohm"],
            "Resistance Cell06": [0.36762747168540955, "Ohm"],
            "Resistance Cell07": [0.3570851683616638, "Ohm"],
            "Resistance Cell08": [0.25040584802627563, "Ohm"],
            "Resistance Cell09": [0.17403873801231384, "Ohm"],
            "Resistance Cell10": [0.12074218690395355, "Ohm"],
            "Resistance Cell11": [0.12244515120983124, "Ohm"],
            "Resistance Cell12": [0.12712250649929047, "Ohm"],
            "Resistance Cell13": [0.12710174918174744, "Ohm"],
            "Resistance Cell14": [0.12629543244838715, "Ohm"],
            "Resistance Cell15": [0.126090407371521, "Ohm"],
            "Resistance Cell16": [0.13002616167068481, "Ohm"],
            "Resistance Cell17": [0.1252681314945221, "Ohm"],
            "Resistance Cell18": [0.17563079297542572, "Ohm"],
            "Resistance Cell19": [0.2859029769897461, "Ohm"],
            "Resistance Cell20": [0.33387771248817444, "Ohm"],
            "Resistance Cell21": [0.20872047543525696, "Ohm"],
            "Resistance Cell22": [0.12146124988794327, "Ohm"],
            "Resistance Cell23": [0.12086664140224457, "Ohm"],
            "Resistance Cell24": [0.18812115490436554, "Ohm"],
            "Resistance Cell25": [0.0, "Ohm"],
            "Average Cell Voltage": [2.327305316925049, "V"],
            "Delta Cell Voltage": [0.178879976272583, "V"],
            "Highest Cell": [8, ""],
            "Lowest Cell": [12, ""],
            "Flags": ["0101", ""],
            "uptime": ["0D3H23M12S", ""],
            "Checksum": ["0b", ""],
            "Highest Cell Voltage": [2.367180585861206, "V", None],
            "Lowest Cell Voltage": [2.186809778213501, "V", None],
        }

        protocol.get_full_command(command)
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)

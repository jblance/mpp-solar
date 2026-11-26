"""Mixed JK protocols must retain their own decoding and command definitions."""
import unittest

from mppsolar.protocols.jk04 import NEW_COMMANDS as JK04_COMMANDS, jk04
from mppsolar.protocols.jkv11 import NEW_COMMANDS as JKV11_COMMANDS, jkv11


class TestJkProtocolIsolation(unittest.TestCase):
    def check_mixed_protocols(self, first_type, second_type):
        first = first_type()
        second = second_type()
        devices = {first_type: first, second_type: second}
        for cls, commands, field, voltage in (
            (jk04, JK04_COMMANDS, "Voltage Cell01", 3.5365207195281982),
            (jkv11, JKV11_COMMANDS, "Voltage_Cell01", 3.325),
        ):
            with self.subTest(protocol=cls.__name__):
                device = devices[cls]
                # Use the recorded response shipped with each protocol, through
                # the same command preparation/decoding path as a device poll.
                device.get_full_command("getCellData")
                response = commands["getCellData"]["test_responses"][0]
                decoded = device.decode(response, "getCellData")
                self.assertAlmostEqual(decoded[field][0], voltage)
                self.assertEqual(decoded[field][1], "V")

    def test_jk04_then_jkv11(self):
        self.check_mixed_protocols(jk04, jkv11)

    def test_jkv11_then_jk04(self):
        self.check_mixed_protocols(jkv11, jk04)

    def test_repeated_same_protocol(self):
        first = jk04()
        jk04()
        first.get_full_command("getCellData")
        decoded = first.decode(JK04_COMMANDS["getCellData"]["test_responses"][0], "getCellData")
        self.assertAlmostEqual(decoded["Voltage Cell01"][0], 3.5365207195281982)

    def test_other_protocol_setters_do_not_leak(self):
        jkv11()
        device = jk04()
        self.assertIsNone(device.get_full_command("setCellOVP3.65"))
        self.assertIsNotNone(device.get_full_command("getInfo"))

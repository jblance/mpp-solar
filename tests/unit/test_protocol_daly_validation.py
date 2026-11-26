"""Do not turn incomplete or mixed Daly frames into battery measurements."""
import unittest

from mppsolar.protocols.daly import COMMANDS, daly
from mppsolar.protocols.protocol_helpers import crc8


class TestDalyValidation(unittest.TestCase):
    def setUp(self):
        self.protocol = daly()
        self.protocol.get_full_command("cellVoltages")
        self.valid = COMMANDS["cellVoltages"]["test_responses"][0]

    def assert_rejected(self, response):
        decoded = self.protocol.decode(response, "cellVoltages")
        self.assertIn("validity check", decoded)
        self.assertFalse(any(key.startswith("Cell ") for key in decoded))

    def test_reported_unaligned_capture(self):
        # First capture from https://github.com/jblance/mpp-solar/issues/516.
        self.assert_rejected(bytes.fromhex(
            "7b a5019508060cce0cd00cd0a07b a5019508010cd10cd00ccea077 "
            "a5019508020cd00ccf0cd0a078 a5019508030ccf0cd00ccfa078 "
            "a5019508040cd00ccf0cd0a07a a5019508050ccf0cd00ccfa07a "
            "a5019508060ccf0cd00ccfa07b"
        ))

    def test_incomplete_last_frame(self):
        self.assert_rejected(self.valid[:-1])

    def test_bad_checksum_in_later_frame(self):
        response = bytearray(self.valid)
        response[20] ^= 1
        self.assert_rejected(response)

    def test_valid_checksum_wrong_command(self):
        response = bytearray(self.valid)
        response[15] = 0x96
        response[25] = crc8(response[13:25])
        self.assert_rejected(response)

    def test_out_of_order_frames(self):
        self.assert_rejected(self.valid[13:26] + self.valid[:13])

    def test_complete_frames_still_decode(self):
        decoded = self.protocol.decode(self.valid, "cellVoltages")
        self.assertNotIn("validity check", decoded)
        self.assertEqual(decoded["Cell 01 Voltage"], [3.325, "V"])
        self.assertEqual(decoded["Cell 16 Voltage"], [3.324, "V"])

    def test_single_complete_frame(self):
        decoded = self.protocol.decode(self.valid[:13], "cellVoltages")
        self.assertEqual(decoded["Cell 01 Voltage"], [3.325, "V"])

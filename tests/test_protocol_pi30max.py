import subprocess
import unittest

# from mppsolar.protocols.pi30max import pi30max as pi

# Examples
# self.assertRaises(mppinverter.NoDeviceError, mppinverter.mppInverter)
# self.assertEqual(inverter._baud_rate, 2400)
# self.assertIsNone(inverter._serial_number)
# self.assertFalse(inverter._direct_usb)
# self.assertIsInstance(inverter.getAllCommands(), list)
# self.assertTrue(inverter._direct_usb)
# self.assertListEqual(mppcommand.crc(bytes('196', 'utf-8')), [27, 14])


class test_pi30max_decode(unittest.TestCase):
    maxDiff = None

    def test_pi30max_getdevice_id(self):
        try:
            expected = "PI30:044:MKS2-8000\n"
            result = subprocess.run(
                ["mpp-solar", "-p", "test", "-P", "pi30max", "--getDeviceId", "-o", "value"],
                check=True,
                capture_output=True,
                text=True,
            )
            # print(result.stdout)
            self.assertEqual(result.stdout, expected)
            self.assertEqual(result.returncode, 0)
        except subprocess.CalledProcessError as error:
            print(error.stdout)
            print(error.stderr)
            raise error

import unittest
import subprocess
from mppsolar.protocols.pi17 import pi17 as pi


class test_pi17_decode(unittest.TestCase):
    maxDiff = None

    def test_pi17_PI(self):
        """test the decode of a PI response"""
        protocol = pi()
        response = b"^D00517\xca\xec\r"
        command = "PI"
        expected = {
            "raw_response": ["^D00517Êì\r", ""],
            "_command": "PI",
            "_command_description": "Device Protocol Version inquiry",
            "Protocol Version": ["17", ""],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)

    def test_pi17_getdevice_id(self):
        try:
            expected = "17:050\n"
            result = subprocess.run(
                ["mpp-solar", "-p", "test", "-P", "pi17", "--getDeviceId", "-o", "value"],
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

    def test_pi17_HECS(self):
        try:
            expected = "\n"
            result = subprocess.run(
                ["mpp-solar", "-p", "test", "-P", "pi17", "-c", "HECS", "-o", "value"],
                check=True,
                capture_output=True,
                text=True,
            )
            print(result.stdout)
            self.assertEqual(result.stdout, expected)
            self.assertEqual(result.returncode, 0)
        except subprocess.CalledProcessError as error:
            print(error.stdout)
            print(error.stderr)
            raise error

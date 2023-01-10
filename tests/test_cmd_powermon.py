import subprocess
import unittest


# from mppsolar.devices.device import AbstractDevice as _abstractdevice


class test_command_line_powermon(unittest.TestCase):
    maxDiff = 9999

    def test_run_powermon(self):
        try:
            expected = "Command: QPI - Protocol ID inquiry\n--------------------------------------------------------------------------------\nParameter   Value          \tUnit\nprotocol_id PI30           \t    \n"
            result = subprocess.run(
                ["powermon", "--once"], check=True, capture_output=True, text=True
            )
            # print(result.stdout)
            self.assertEqual(result.stdout, expected)
            self.assertEqual(result.returncode, 0)
        except subprocess.CalledProcessError as error:
            print(error.stdout)
            print(error.stderr)
            raise error

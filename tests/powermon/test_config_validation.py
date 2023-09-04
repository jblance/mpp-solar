import subprocess
import unittest

FILES = ['powermon/config/min.yaml',
         'powermon/config/min-api.yaml',
         'powermon/config/format.yaml',
         'powermon/config/powermon.yaml',
         'powermon/config/powermon-hass.yaml',
         'docker/powermon.yaml']


def do_test(self, filename):
    try:
        print(f"testing {filename}", end=' ')
        expected = "Config validation successful\n"
        result = subprocess.run(
            ["powermon", "-V", "-C", filename,], check=True, capture_output=True, text=True
        )
        self.assertEqual(result.stdout, expected)
        self.assertEqual(result.returncode, 0)
        print('OK')
    except subprocess.CalledProcessError as error:
        print(error.stdout)
        print(error.stderr)
        raise error


class test_command_line(unittest.TestCase):
    maxDiff = 9999

    def test_config_validation(self):
        for filename in FILES:
            do_test(self, filename)

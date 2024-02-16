import subprocess
import unittest

FILES = [
    'docker/powermon.yaml',
    'docker/dev/config/powermon.yaml',
    'docker/dev/config/powermon-qpigs.yaml',
    'tests/pmon/config/min.yaml',
    'tests/pmon/config/api.yaml',
    'tests/pmon/config/format.yaml',
    'tests/pmon/config/powermon.yaml',
    'tests/pmon/config/hass.yaml',
    'tests/pmon/config/qed.yaml',
    'docker/powermon.yaml'
    ]


def do_test(self, filename):
    try:
        # print(f"testing {filename}", end=' ')
        expected = "Config validation successful\n"
        result = subprocess.run(
            ["powermon", "-V", "-C", filename,], check=True, capture_output=True, text=True
        )
        self.assertEqual(result.stdout, expected)
        self.assertEqual(result.returncode, 0)
        # print('OK')
    except subprocess.CalledProcessError as error:
        print(error.stdout)
        print(error.stderr)
        raise error


class test_command_line(unittest.TestCase):
    maxDiff = 9999

    def test_config_validation(self):
        for filename in FILES:
            do_test(self, filename)

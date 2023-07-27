import unittest
import subprocess


QUERY_COMMANDS = [
    ("PI", "protocol_version=17\n"),
    ("BATS", """\n"""),
]
# ("", """\n"""),
# ("DI", """\n"""),
# ("PS", """\n"""),


def do_test(self, command, expected, respno=0):
    try:
        print(command, end=" ")
        result = subprocess.run(
            [
                "mppsolar",
                "-p",
                "test0",
                "-P",
                "PI17m058",
                "-c",
                command,
                "-o",
                "simpleunits"
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        print(result.stdout)
        # print(result.stderr)
        # print(".")
        self.assertEqual(f"CMD: {command}\n{result.stdout}", f"CMD: {command}\n{expected}")
        self.assertEqual(result.returncode, 0)
        print("OK")
    except subprocess.CalledProcessError as error:
        print(error.stdout)
        print(error.stderr)
        raise error


class test_pi17_decode(unittest.TestCase):
    maxDiff = None

    def test_pi17_query_commands(self):
        for command, expected in QUERY_COMMANDS:
            do_test(self, command, expected, 1)

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

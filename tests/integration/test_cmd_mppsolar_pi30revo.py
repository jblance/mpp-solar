import subprocess
import unittest


# from mppsolar.devices.device import AbstractDevice as _abstractdevice
# from powermon.protocols.pi30max import SETTER_COMMANDS

QUERY_COMMANDS = [
    ("PQSE", """language=English
work_mode=Utility Priority
input_range=Wide
output_voltage=230V
output_frequency=50Hz
battery_type=Lead Acid
battery_bulk_charge_voltage=56.0(V)
battery_float_charge_voltage=54.0(V)
battery_low_voltage_alarm_point=44.0(V)
battery_low_voltage_cutoff_point=42.0(V)
total_charging_current=30(A)
ac_charging_current=10(A)
year=2018
month=06
day=01
hour=20
minute=00
buzzer=Enabled
grid=Not Connected
battery_full_recovery_point=0.0(V)\n"""),
]


def do_test(self, command, expected, respno=0):
    try:
        # print(command, end=" ")
        result = subprocess.run(
            [
                "mppsolar",
                "-p",
                "test0",
                "-P",
                "pi30revo",
                "-c",
                command,
                "-o",
                "simpleunits"
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        # print(result.stdout)
        # print(result.stdout)
        # print(result.stderr)
        self.assertEqual(f"CMD: {command}\n{result.stdout}", f"CMD: {command}\n{expected}")
        self.assertEqual(result.returncode, 0)
        # print("OK")
    except subprocess.CalledProcessError as error:
        print(error.stdout)
        print(error.stderr)
        raise error


class test_cmd_mppsolar_pi30revo(unittest.TestCase):
    maxDiff = 9999

    def test_pi30max_query_commands(self):
        for command, expected in QUERY_COMMANDS:
            do_test(self, command, expected)

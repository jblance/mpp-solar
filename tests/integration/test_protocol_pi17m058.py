import unittest
import subprocess


QUERY_COMMANDS = [
    ("PI", "protocol_version=17\n"),
    ("BATS", """battery_maximum_charge_current=175.0(A)
battery_constant_charge_voltage=56.0(V)
battery_floating_charge_voltage=54.0(V)
battery_stop_charger_current_level_in_floating_charging=0.0(A)
keep_charged_time_of_battery_catch_stopped_charging_current_level=60(Minutes)
battery_voltage_of_recover_to_charge_when_battery_stop_charger_in_floating_charging=53.0(V)
battery_under_voltage=42.0(V)
battery_under_voltage_release=48.0(V)
battery_weak_voltage_in_hybrid_mode=48.0(V)
battery_weak_voltage_release_in_hybrid_mode=54.0(V)
battery_type=Ordinary
ac_charger_keep_battery_voltage_function_enable/diable=Disabled
ac_charger_keep_battery_voltage=48.0(V)
battery_temperature_sensor_compensation=0.0(mV)
max._ac_charging_current=10.0(A)
battery_discharge_max_current_in_hybrid_mode=175(A)
battery_under_soc=10(%)
battery_under_back_soc=20(%)
battery_weak_soc_in_hybrid_mode=20(%)
battery_weak_back_soc_in_hybrid_mode=80(%)
unknown=0\n"""),
]
# ("", """\n"""),
# ("DI", """\n"""),
# ("PS", """\n"""),


def do_test(self, command, expected, respno=0):
    try:
        # print(command, end=" ")
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

        # print(result.stdout)
        # print(result.stderr)
        # print(".")
        self.assertEqual(f"CMD: {command}\n{result.stdout}", f"CMD: {command}\n{expected}")
        self.assertEqual(result.returncode, 0)
        # print("OK")
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

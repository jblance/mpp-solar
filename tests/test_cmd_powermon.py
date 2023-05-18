import subprocess
import unittest


# from mppsolar.devices.device import AbstractDevice as _abstractdevice


class test_command_line_powermon(unittest.TestCase):
    maxDiff = 9999

    def test_run_powermon_qpi_cmd(self):
        try:
            expected = "protocol_id=PI30\n"
            result = subprocess.run(
                ["powermon", "--once", "--config", '{"device": {"port":{"type":"test"}}, "commands": [{"command":"QPI"}]}'],
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

    def test_run_powermon_output1(self):
        try:
            expected = "protocol_id=PI30\n"
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test"}}, "commands": [{"command": "QPI", "outputs": {"format": "simple"}}]}',
                ],
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

    def test_run_powermon_many_output(self):
        try:
            expected = """ac_input_voltage=0.0V
ac_input_frequency=0.0Hz
ac_output_voltage=230.0V
ac_output_frequency=49.9Hz
ac_output_apparent_power=161VA
ac_output_active_power=119W
ac_output_load=3%
bus_voltage=460V
battery_voltage=57.5V
battery_charging_current=12A
battery_capacity=100%
inverter_heat_sink_temperature=69°C
pv_input_current_for_battery=14.0A
pv_input_voltage=103.8V
battery_voltage_from_scc=57.45V
battery_discharge_current=0A
is_sbu_priority_version_added=0bool
is_configuration_changed=0bool
is_scc_firmware_updated=1bool
is_load_on=1bool
is_battery_voltage_to_steady_while_charging=0bool
is_charging_on=1bool
is_scc_charging_on=1bool
is_ac_charging_on=0bool
rsv1=0A
rsv2=0A
pv_input_power=856W
is_charging_to_float=0bool
is_switched_on=1bool
is_reserved=0bool
ac_input_voltage=0.0V
ac_input_frequency=0.0Hz
ac_output_voltage=230.0V
ac_output_frequency=49.9Hz
ac_output_apparent_power=161VA
ac_output_active_power=119W
ac_output_load=3%
bus_voltage=460V
battery_voltage=57.5V
battery_charging_current=12A
battery_capacity=100%
inverter_heat_sink_temperature=69°C
pv_input_current_for_battery=14.0A
pv_input_voltage=103.8V
battery_voltage_from_scc=57.45V
battery_discharge_current=0A
is_sbu_priority_version_added=0bool
is_configuration_changed=0bool
is_scc_firmware_updated=1bool
is_load_on=1bool
is_battery_voltage_to_steady_while_charging=0bool
is_charging_on=1bool
is_scc_charging_on=1bool
is_ac_charging_on=0bool
rsv1=0A
rsv2=0A
pv_input_power=856W
is_charging_to_float=0bool
is_switched_on=1bool
is_reserved=0bool
protocol_id=PI30
validity_check=Error: Invalid response CRCs\n"""
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"commands": [{"command": "QPIGS", "type": "basic", "trigger": {"every": 25}, "outputs": [{"type": "screen", "format": "simple"}, {"type": "screen", "format": {"type": "simple"}}]}, {"command": "QPI", "outputs": {"format": "simple"}}, {"command": "QID", "outputs": "screen", "trigger": {"at": "12:56"}}, {"command": "QMOD", "trigger": {"loops": 50}}], "device": {"port": {"type": "test"}}}',
                ],
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

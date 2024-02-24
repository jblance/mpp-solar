import json
import subprocess
import unittest


class test_command_line(unittest.TestCase):
    maxDiff = 9999

    def test_run_mppsolar(self):
        try:
            expected = "serial_number=9293333010501\n"
            result = subprocess.run(
                ["mpp-solar", "-c", "QID", "-p", "test0", "-o", "simple"], check=True, capture_output=True, text=True
            )
            # print(result.stdout)
            self.assertEqual(result.stdout, expected)
            self.assertEqual(result.returncode, 0)
        except subprocess.CalledProcessError as error:
            print(error.stdout)
            print(error.stderr)
            raise error

    def test_run_mppsolar_screen(self):
        try:
            expected = """Command: QPI - Protocol ID inquiry
--------------------------------------------------------------------------------
Parameter   Value          \tUnit
protocol_id PI30           \t    
--------------------------------------------------------------------------------\n\n\n"""
            result = subprocess.run(
                ["mpp-solar", "-c", "QPI", "-p", "test0"], check=True, capture_output=True, text=True
            )
            # print(result.stdout)
            self.assertEqual(result.stdout, expected)
            self.assertEqual(result.returncode, 0)
        except subprocess.CalledProcessError as error:
            print(error.stdout)
            print(error.stderr)
            raise error

    def test_run_mppsolar_test(self):
        try:
            expected = {
                "_command": "QPIGS",
                "_command_description": "General Status Parameters inquiry",
                "ac_input_voltage": {"value": 0.0, "unit": "V"},
                "ac_input_frequency": {"value": 0.0, "unit": "Hz"},
                "ac_output_voltage": {"value": 230.0, "unit": "V"},
                "ac_output_frequency": {"value": 49.9, "unit": "Hz"},
                "ac_output_apparent_power": {"value": 161, "unit": "VA"},
                "ac_output_active_power": {"value": 119, "unit": "W"},
                "ac_output_load": {"value": 3, "unit": "%"},
                "bus_voltage": {"value": 460, "unit": "V"},
                "battery_voltage": {"value": 57.5, "unit": "V"},
                "battery_charging_current": {"value": 12, "unit": "A"},
                "battery_capacity": {"value": 100, "unit": "%"},
                "inverter_heat_sink_temperature": {"value": 69, "unit": "°C"},
                "pv_input_current_for_battery": {"value": 14.0, "unit": "A"},
                "pv_input_voltage": {"value": 103.8, "unit": "V"},
                "battery_voltage_from_scc": {"value": 57.45, "unit": "V"},
                "battery_discharge_current": {"value": 0, "unit": "A"},
                "is_sbu_priority_version_added": {"value": 0, "unit": "bool"},
                "is_configuration_changed": {"value": 0, "unit": "bool"},
                "is_scc_firmware_updated": {"value": 1, "unit": "bool"},
                "is_load_on": {"value": 1, "unit": "bool"},
                "is_battery_voltage_to_steady_while_charging": {
                    "value": 0,
                    "unit": "bool",
                },
                "is_charging_on": {"value": 1, "unit": "bool"},
                "is_scc_charging_on": {"value": 1, "unit": "bool"},
                "is_ac_charging_on": {"value": 0, "unit": "bool"},
                "rsv1": {"value": 0, "unit": "A"},
                "rsv2": {"value": 0, "unit": "A"},
                "pv_input_power": {"value": 856, "unit": "W"},
                "is_charging_to_float": {"value": 0, "unit": "bool"},
                "is_switched_on": {"value": 1, "unit": "bool"},
                "is_reserved": {"value": 0, "unit": "bool"},
            }
            result = subprocess.run(
                ["mpp-solar", "-c", "QPIGS", "-p", "test", "-o", "json_units"],
                check=True,
                capture_output=True,
                text=True,
            )
            res = json.loads(result.stdout)
            # print(res)
            self.assertEqual(res, expected)
            self.assertEqual(result.returncode, 0)
        except subprocess.CalledProcessError as error:
            print(error.stdout)
            print(error.stderr)
            raise error

    def test_mppsolar_mqtt(self):
        try:
            expected = "mqtt debug output only as broker name is 'screen' - topic: 'QPI/status/protocol_id/value', payload: 'PI30'\n"
            result = subprocess.run(
                ["mpp-solar", "-p", "test", "-o", "mqtt", "-q", "screen"],
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

import subprocess
import unittest


# from mppsolar.devices.device import AbstractDevice as _abstractdevice
# from powermon.protocols.pi30max import SETTER_COMMANDS

QUERY_COMMANDS = [
    ("QVFW3", "remote_cpu_firmware_version=00072.70\n"),
    ("VERFW", "bluetooth_firmware_version=00072.70\n"),
    (
        "QPIRI",
        """ac_input_voltage=230.0V
ac_input_current=21.7A
ac_output_voltage=230.0V
ac_output_frequency=50.0Hz
ac_output_current=21.7A
ac_output_apparent_power=5000VA
ac_output_active_power=4000W
battery_voltage=48.0V
battery_recharge_voltage=46.0V
battery_under_voltage=42.0V
battery_bulk_charge_voltage=56.4V
battery_float_charge_voltage=54.0V
battery_type=AGM
max_ac_charging_current=10A
max_charging_current=10A
input_voltage_range=UPS
output_source_priority=Utility Solar Battery
charger_source_priority=Utility first
max_parallel_units=6
machine_type=Off Grid
topology=transformerless
output_mode=single machine
battery_redischarge_voltage=54.0V
pv_ok_condition=As long as one unit of inverters has connect PV, parallel system will consider PV OK
pv_power_balance=PV input max power will be the sum of the max charged power and loads power\n""",
    ),
    (
        "QFLAG",
        """buzzer=enabled
lcd_reset_to_default=enabled
lcd_backlight=enabled
primary_source_interrupt_alarm=enabled
overload_bypass=disabled
solar_feed_to_grid=disabled
overload_restart=disabled
over_temperature_restart=disabled
record_fault_code=disabled\n""",
    ),
    (
        "QPIGS",
        """ac_input_voltage=227.2V
ac_input_frequency=50.0Hz
ac_output_voltage=230.3V
ac_output_frequency=50.0Hz
ac_output_apparent_power=829VA
ac_output_active_power=751W
ac_output_load=10%
bus_voltage=447V
battery_voltage=54.5V
battery_charging_current=20A
battery_capacity=83%
inverter_heat_sink_temperature=54°C
pv1_input_current=2.7A
pv1_input_voltage=323.6V
battery_voltage_from_scc=0.0V
battery_discharge_current=0A
is_sbu_priority_version_added=0bool
is_configuration_changed=0bool
is_scc_firmware_updated=0bool
is_load_on=1bool
is_battery_voltage_to_steady_while_charging=0bool
is_charging_on=1bool
is_scc_charging_on=1bool
is_ac_charging_on=0bool
battery_voltage_offset_for_fans_on_(10mv)=0V
eeprom_version=0
pv1_charging_power=879W
is_charging_to_float=0bool
is_switched_on=1bool
is_dustproof_installed=0bool\n""",
    ),
    (
        "QPIGS2",
        """pv2_input_current=3.1A
pv2_input_voltage=327.3V
pv2_charging_power=1026W\n""",
    ),
    (
        "QPGS0",
        """parallel_instance_number=Not valid
serial_number=92932105105315
work_mode=Battery Mode
fault_code=No fault
grid_voltage=0.0V
grid_frequency=0.0Hz
ac_output_voltage=230.0V
ac_output_frequency=50.0Hz
ac_output_apparent_power=989VA
ac_output_active_power=907W
load_percentage=12%
battery_voltage=53.2V
battery_charging_current=9A
battery_capacity=90%
pv1_input_voltage=349.8V
total_charging_current=9A
total_ac_output_apparent_power=989VA
total_output_active_power=907W
total_ac_output_percentage=11%
is_scc_ok=1bool
is_ac_charging=0bool
is_scc_charging=1bool
is_battery_over_voltage=0bool
is_battery_under_voltage=0bool
is_line_lost=1bool
is_load_on=1bool
is_configuration_changed=0bool
output_mode=single machine
charger_source_priority=Solar first
max_charger_current=100A
max_charger_range=120A
max_ac_charger_current=30A
pv1_input_current=2A
battery_discharge_current=0A
pv2_input_voltage=275.3V
pv2_input_current=2A\n""",
    ),
    (
        "QMOD",
        "device_mode=Standby\n",
    ),
    (
        "QPIWS",
        """pv_loss_warning=0bool
inverter_fault=0bool
bus_over_fault=0bool
bus_under_fault=0bool
bus_soft_fail_fault=0bool
line_fail_warning=1bool
opv_short_warning=0bool
inverter_voltage_too_low_fault=0bool
inverter_voltage_too_high_fault=0bool
over_temperature_fault=0bool
fan_locked_fault=0bool
battery_voltage_to_high_fault=0bool
battery_low_alarm_warning=0bool
reserved=0bool
battery_under_shutdown_warning=0bool
battery_derating_warning=0bool
overload_fault=1bool
eeprom_fault=0bool
inverter_over_current_fault=0bool
inverter_soft_fail_fault=0bool
self_test_fail_fault=0bool
op_dc_voltage_over_fault=0bool
bat_open_fault=0bool
current_sensor_fail_fault=0bool
battery_short_fault=0bool
power_limit_warning=0bool
pv_voltage_high_warning=0bool
mppt_overload_fault=0bool
mppt_overload_warning=0bool
battery_too_low_to_charge_warning=0bool
battery_weak=0bool\n""",
    ),
    (
        "QDI",
        """ac_output_voltage=230.0V
ac_output_frequency=50.0Hz
max_ac_charging_current=30A
battery_under_voltage=44.0V
battery_float_charge_voltage=54.0V
battery_bulk_charge_voltage=56.4V
battery_recharge_voltage=46.0V
max_charging_current=60A
input_voltage_range=Appliance
output_source_priority=Utility first
charger_source_priority=Solar + Utility
battery_type=AGM
buzzer=enabled
power_saving=disabled
overload_restart=disabled
over_temperature_restart=disabled
lcd_backlight=enabled
primary_source_interrupt_alarm=enabled
record_fault_code=enabled
overload_bypass=disabled
lcd_reset_to_default=enabled
output_mode=single machine
battery_redischarge_voltage=54.0V
pv_ok_condition=As long as one unit of inverters has connect PV, parallel system will consider PV OK
pv_power_balance=PV input max power will be the sum of the max charged power and loads power
max_charging_time_at_cv=224min\n""",
    ),
    (
        "QOPPT",
        """output_source_priority_00_hours=Solar + Utility
output_source_priority_01_hours=Solar + Utility
output_source_priority_02_hours=Solar + Utility
output_source_priority_03_hours=Solar + Utility
output_source_priority_04_hours=Solar + Utility
output_source_priority_05_hours=Solar + Utility
output_source_priority_06_hours=Solar + Utility
output_source_priority_07_hours=Solar + Utility
output_source_priority_08_hours=Solar + Utility
output_source_priority_09_hours=Solar + Utility
output_source_priority_10_hours=Solar + Utility
output_source_priority_11_hours=Solar + Utility
output_source_priority_12_hours=Solar + Utility
output_source_priority_13_hours=Solar + Utility
output_source_priority_14_hours=Solar + Utility
output_source_priority_15_hours=Solar + Utility
output_source_priority_16_hours=Solar + Utility
output_source_priority_17_hours=Solar + Utility
output_source_priority_18_hours=Solar + Utility
output_source_priority_19_hours=Solar + Utility
output_source_priority_20_hours=Solar + Utility
output_source_priority_21_hours=Solar + Utility
output_source_priority_22_hours=Solar + Utility
output_source_priority_23_hours=Solar + Utility
device_output_source_priority=Solar + Utility
selection_of_output_source_priority_order_1=Utility
selection_of_output_source_priority_order_2=Solar + Utility
selection_of_output_source_priority_order_3=Solar first\n""",
    ),
    (
        "QCHPT",
        """charger_source_priority_00_hours=Only Solar
charger_source_priority_01_hours=Only Solar
charger_source_priority_02_hours=Only Solar
charger_source_priority_03_hours=Only Solar
charger_source_priority_04_hours=Only Solar
charger_source_priority_05_hours=Only Solar
charger_source_priority_06_hours=Only Solar
charger_source_priority_07_hours=Only Solar
charger_source_priority_08_hours=Only Solar
charger_source_priority_09_hours=Only Solar
charger_source_priority_10_hours=Only Solar
charger_source_priority_11_hours=Only Solar
charger_source_priority_12_hours=Only Solar
charger_source_priority_13_hours=Only Solar
charger_source_priority_14_hours=Only Solar
charger_source_priority_15_hours=Only Solar
charger_source_priority_16_hours=Only Solar
charger_source_priority_17_hours=Only Solar
charger_source_priority_18_hours=Only Solar
charger_source_priority_19_hours=Only Solar
charger_source_priority_20_hours=Only Solar
charger_source_priority_21_hours=Only Solar
charger_source_priority_22_hours=Only Solar
charger_source_priority_23_hours=Only Solar
device_charger_source_priority=Only Solar
selection_of_charger_source_priority_order_1=Utility
selection_of_charger_source_priority_order_2=Utility
selection_of_charger_source_priority_order_3=Utility\n""",
    ),
    (
        "QT",
        "device_time=20210726122606\n",
    ),
    (
        "QBEQI",
        """equalization_enabled=Enabled
equalization_time=30min
equalization_period=30days
equalization_max_current=80A
reserved1=021
equalization_voltage=55.4V
reserved2=224
equalization_over_time=30min
equalization_active=Inactive
equalization_elasped_time=234hours\n""",
    ),
    ("QET", """total_pv_generated_energy=238800Wh\n""",),
    ("QEY2023", """pv_generated_energy_for_year=238800Wh\nyear=2023\n""",),
    ("QEM202301", """pv_generated_energy_for_month=238800Wh\nyear=2023\nmonth=January\n""",),
    ("QED20230113", """pv_generated_energy_for_day=238800Wh\nyear=2023\nmonth=January\nday=13\n""",),
    ("QLT", """total_output_load_energy=238800Wh\n""",),
    ("QLY2023", """output_load_energy_for_year=238800Wh\nyear=2023\n""",),
    ("QLM202302", """output_load_energy_for_month=238800Wh\nyear=2023\nmonth=February\n""",),
    ("QLD20230315", """output_load_energy_for_day=238800Wh\nyear=2023\nmonth=March\nday=15\n""",),
    ("QLED", """led_enabled=Enabled
led_speed=Medium
led_effect=Solid
led_brightness=5
led_number_of_colors=3
rgb=148000211255255255000255255\n""",),
]
SETTER_COMMANDS = [
    ("PLEDE0", """enable-disable_led_function=Succeeded\n"""),
    ("PLEDS1", """set_led_speed=Succeeded\n"""),
    ("PLEDM2", """set_led_effect=Succeeded\n"""),
    ("PLEDB4", """set_led_brightness=Succeeded\n"""),
    ("PLEDT3", """set_led_total_number_of_colors=Succeeded\n"""),
    ("PLEDC2333444555", """set_led_color=Succeeded\n"""),
]


def do_test(self, command, expected, respno=0):
    try:
        # print(command, end=" ")
        result = subprocess.run(
            [
                "powermon",
                "--once",
                "--config",
                '{"device": {"port":{"type":"test", "response_number": %s, "protocol": "PI30MAX"}}, "commands": [{"command":"%s"}]}' % (respno, command),
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
        # print(".", end="")
    except subprocess.CalledProcessError as error:
        print(error.stdout)
        print(error.stderr)
        raise error


class test_cmd_powermon_pi30max(unittest.TestCase):
    maxDiff = 9999

    def test_pi30max_query_commands(self):
        for command, expected in QUERY_COMMANDS:
            do_test(self, command, expected)

    def test_pi30max_setter_commands(self):
        for command, expected in SETTER_COMMANDS:
            do_test(self, command, expected, 1)

    def test_powermon_QSID(self):
        try:
            expected = "serial_number=92932105105335\n"
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test", "response_number": 0, "protocol": "PI30MAX"}}, "commands": [{"command":"QSID"}]}',
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            # print(result.stdout)
            # print(result.stdout)
            # print(result.stderr)
            self.assertEqual(result.stdout, expected)
            self.assertEqual(result.returncode, 0)
        except subprocess.CalledProcessError as error:
            print(error.stdout)
            print(error.stderr)
            raise error

    def test_powermon_QPI(self):
        try:
            expected = "protocol_id=PI30\n"
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test", "response_number": 0, "protocol": "PI30MAX"}}, "commands": [{"command":"QPI"}]}',
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

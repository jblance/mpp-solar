""" tests / pmon / integration / test_cmd_powermon_pi30.py """
import subprocess
import unittest


SETTER_COMMANDS = [
    ("F50", """set_device_output_frequency=Succeeded\n"""),
    ("MCHGC040", """set_max_charging_current_(for_parallel_units)=Succeeded\n"""),
    ("MNCHGC1120", """set_utility_max_charging_current_(more_than_100a)_(for_4000/5000)=Succeeded\n"""),
    ("MUCHGC130", """set_utility_max_charging_current=Succeeded\n"""),
    ("PBCV44.0", """set_battery_re-charge_voltage=Succeeded\n"""),
    ("PBDV48.0", """set_battery_re-discharge_voltage=Succeeded\n"""),
    ("PBFT58.0", """set_battery_float_charging_voltage=Succeeded\n"""),
    ("PBT01", """set_battery_type=Succeeded\n"""),
    ("PCP03", """set_device_charger_priority=Succeeded\n"""),
    ("PCVV48.0", """set_battery_c.v._(constant_voltage)_charging_voltage=Succeeded\n"""),
    ("PEa", """set_the_enabled_state_of_an_inverter_setting=Succeeded\n"""),
    ("PDb", """set_the_disabled_state_of_an_inverter_setting=Succeeded\n"""),
    ("PF", """set_control_parameters_to_default_values=Succeeded\n"""),
    ("PGR01", """set_grid_working_range=Succeeded\n"""),
    ("POP02", """set_device_output_source_priority=Succeeded\n"""),
    ("POPLG00", """set_device_operation_logic=Succeeded\n"""),
    ("POPM10", """set_device_output_mode_(for_4000/5000)=Succeeded\n"""),
    ("PPCP000", """set_parallel_device_charger_priority_(for_4000/5000)=Succeeded\n"""),
    ("PPVOKC1", """set_pv_ok_condition=Succeeded\n"""),
    ("PSDV40.0", """set_battery_cut-off_voltage=Succeeded\n"""),
    ("PSPB0", """set_solar_power_balance=Succeeded\n"""),
    ("PBATCD010", """battery_charge/discharge_controlling_command=Succeeded\n"""),
    ("DAT20230115091533", """set_date_time=Succeeded\n"""),
    ("PBATMAXDISC150", """battery_max_discharge_current=Succeeded\n"""),
    ("BTA-01", """calibrate_inverter_battery_voltage=Succeeded\n"""),
    ("BTA+09", """calibrate_inverter_battery_voltage=Succeeded\n"""),
    ("PSAVE", """save_eeprom_changes=Succeeded\n"""),
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
        # print("OK")
        # print(".", end="")
    except subprocess.CalledProcessError as error:
        print(error.stdout)
        print(error.stderr)
        raise error


class test_command_line_powermon(unittest.TestCase):
    maxDiff = 9999

    def test_pi30_setter_commands(self):
        for command, expected in SETTER_COMMANDS:
            do_test(self, command, expected, 1)

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
                    '{"device": {"port":{"type":"test"}}, "commands": [{"command": "QPI", "outputs": [{"type": "screen", "format": "simple"}]}]}',
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

    def test_run_powermon_qboot(self):
        try:
            expected = "dsp_has_bootstrap=False\n"
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test"}}, "commands": [{"command": "QBOOT", "outputs": [{"type": "screen", "format": "simple"}]}]}',
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

    def test_run_powermon_qflag(self):
        try:
            expected = """buzzer=enabled
lcd_reset_to_default=enabled
lcd_backlight=enabled
primary_source_interrupt_alarm=enabled
overload_bypass=disabled
power_saving=disabled
overload_restart=disabled
over_temperature_restart=disabled
record_fault_code=disabled\n"""
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test"}}, "commands": [{"command": "QFLAG", "outputs": [{"type": "screen", "format": "simple"}]}]}',
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

    def test_run_powermon_qdi(self):
        try:
            expected = """ac_output_voltage=230.0V
ac_output_frequency=50.0Hz
max_ac_charging_current=30A
battery_under_voltage=42.0V
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
record_fault_code=disabled
overload_bypass=disabled
lcd_reset_to_default=enabled
output_mode=single machine output
battery_redischarge_voltage=54.0V
pv_ok_condition=As long as one unit of inverters has connect PV, parallel system will consider PV OK
pv_power_balance=PV input max power will be the sum of the max charged power and loads power
unknown_value=000\n"""
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test"}}, "commands": [{"command": "QDI", "outputs": [{"type": "screen", "format": "simple"}]}]}',
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

    def test_run_powermon_q1(self):
        try:
            expected = """time_until_the_end_of_absorb_charging=0sec
time_until_the_end_of_float_charging=0sec
scc_flag=SCC is powered and communicating
allowscconflag=SCC allowed to charge
chargeaveragecurrent=0A
scc_pwm_temperature=59°C
inverter_temperature=45°C
battery_temperature=53°C
transformer_temperature=68°C
parallel_mode=New
fan_lock_status=Not locked
not_used=000
fan_pwm_speed=40%
scc_charge_power=580W
parallel_warning=0000
sync_frequency=50.0Hz
inverter_charge_status=float
"""
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test"}}, "commands": [{"command": "Q1", "outputs": [{"type": "screen", "format": "simple"}]}]}',
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
pv_input_current=14.0A
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
pv_input_current=14.0A
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
device_mode=Standby\n"""
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"commands": [{"command": "QPIGS", "type": "basic", "trigger": {"every": 25}, "outputs": [{"type": "screen", "format": "simple"}, {"type": "screen", "format": {"type": "simple"}}]}, {"command": "QPI", "outputs": [{"type": "screen", "format": "simple"}]}, {"command": "QID", "outputs": "screen", "trigger": {"at": "12:56"}}, {"command": "QMOD", "trigger": {"loops": 50}}], "device": {"port": {"type": "test"}}}',
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

    def test_run_powermon_QID(self):
        try:
            expected = "serial_number=9293333010501\n"
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test"}}, "commands": [{"command": "QID", "outputs": [{"type": "screen", "format": "simple"}]}]}',
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

    def test_run_powermon_QMCHGCR(self):
        try:
            expected = """max_charging_current_options=010 020 030 040 050 060 070 080 090 100 110 120A\n"""
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test"}}, "commands": [{"command": "QMCHGCR", "outputs": [{"type": "screen", "format": "simple"}]}]}',
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

    def test_run_powermon_QMOD(self):
        try:
            expected = "device_mode=Standby\n"
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test"}}, "commands": [{"command": "QMOD", "outputs": [{"type": "screen", "format": "simple"}]}]}',
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

    def test_run_powermon_QMN(self):
        try:
            expected = "model_name=MKS2-8000\n"
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test"}}, "commands": [{"command": "QMN", "outputs": [{"type": "screen", "format": "simple"}]}]}',
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

    def test_run_powermon_QGMN(self):
        try:
            expected = "general_model_number=044\n"
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test"}}, "commands": [{"command": "QGMN", "outputs": [{"type": "screen", "format": "simple"}]}]}',
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

    def test_run_powermon_QMUCHGCR(self):
        try:
            expected = "max_utility_charging_current=002 010 020 030 040 050 060 070 080 090 100 110 120A\n"
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test"}}, "commands": [{"command": "QMUCHGCR", "outputs": [{"type": "screen", "format": "simple"}]}]}',
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

    def test_run_powermon_QOPM(self):
        try:
            expected = "output_mode=single machine output\n"
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test"}}, "commands": [{"command": "QOPM", "outputs": [{"type": "screen", "format": "simple"}]}]}',
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

    def test_run_powermon_QPGS(self):
        try:
            expected = """parallel_instance_number=valid
serial_number=92931701100510
work_mode=Battery Mode
fault_code=No fault
grid_voltage=0.0V
grid_frequency=0.0Hz
ac_output_voltage=230.6V
ac_output_frequency=50.0Hz
ac_output_apparent_power=275VA
ac_output_active_power=141W
load_percentage=5%
battery_voltage=51.4V
battery_charging_current=1A
battery_capacity=100%
pv_input_voltage=83.3V
total_charging_current=2A
total_ac_output_apparent_power=574VA
total_output_active_power=312W
total_ac_output_percentage=3%
is_scc_ok=1bool
is_ac_charging=0bool
is_scc_charging=1bool
is_battery_over_voltage=0bool
is_battery_under_voltage=0bool
is_line_lost=1bool
is_load_on=1bool
is_configuration_changed=0bool
output_mode=parallel output
charger_source_priority=Solar + Utility
max_charger_current=60A
max_charger_range=120A
max_ac_charger_current=10A
pv_input_current=4A
battery_discharge_current=0A\n"""
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test", "response_number": 0}}, "commands": [{"command": "QPGS0", "outputs": [{"type": "screen", "format": "simple"}]}]}',
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

    def test_run_powermon_QPIRI(self):
        try:
            expected = """ac_input_voltage=120.0V
ac_input_current=25.0A
ac_output_voltage=120.0V
ac_output_frequency=60.0Hz
ac_output_current=25.0A
ac_output_apparent_power=3000VA
ac_output_active_power=3000W
battery_voltage=48.0V
battery_recharge_voltage=46.0V
battery_under_voltage=44.0V
battery_bulk_charge_voltage=58.4V
battery_float_charge_voltage=54.4V
battery_type=User
max_ac_charging_current=30A
max_charging_current=60A
input_voltage_range=UPS
output_source_priority=SBU first
charger_source_priority=Utility first
max_parallel_units=9
machine_type=Off Grid
topology=transformerless
output_mode=Phase 2 of 2 phase output
battery_redischarge_voltage=54.0V
pv_ok_condition=As long as one unit of inverters has connect PV, parallel system will consider PV OK
pv_power_balance=PV input max power will be the sum of the max charged power and loads power
max_charging_time_for_cv_stage=0min
operation_logic=Automatic mode\n"""
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test", "response_number": 2}}, "commands": [{"command": "QPIRI", "outputs": [{"type": "screen", "format": "simple"}]}]}',
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

    def test_run_powermon_QPIGS(self):
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
pv_input_current=14.0A
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
is_reserved=0bool\n"""
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test"}}, "commands": [{"command": "QPIGS", "outputs": [{"type": "screen", "format": "simple"}]}]}',
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

    def test_run_powermon_QPIWS(self):
        try:
            expected = """inverter_fault=0bool
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
battery_too_low_to_charge_warning=0bool\n"""
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test"}}, "commands": [{"command": "QPIWS", "outputs": [{"type": "screen", "format": "simple"}]}]}',
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

    def test_run_powermon_QVFW(self):
        try:
            expected = "main_cpu_firmware_version=00072.70\n"
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test"}}, "commands": [{"command": "QVFW", "outputs": [{"type": "screen", "format": "simple"}]}]}',
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

    def test_run_powermon_QVFW2(self):
        try:
            expected = "secondary_cpu_firmware_version=00072.70\n"
            result = subprocess.run(
                [
                    "powermon",
                    "--once",
                    "--config",
                    '{"device": {"port":{"type":"test"}}, "commands": [{"command": "QVFW2", "outputs": [{"type": "screen", "format": "simple"}]}]}',
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

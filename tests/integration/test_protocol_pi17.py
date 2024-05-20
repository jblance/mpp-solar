import unittest
import subprocess


QUERY_COMMANDS = [
    ("PI", "protocol_version=17\n"),
    ("ID", "serial_number=1496161704100242000000\n"),
    ("VFW", "cpu_version=VERFW:00001.01\n"),
    ("VFW2", "cpu_2_version=VERFW2:00001.01\n"),
    ("MD", """machine_number=Infini-Solar 10KW/3P
output_rated_va=10000(kW)
output_power_factor=99(pf)
ac_input_phase_number=3(number)
ac_output_phase_number=3(number)
norminal_ac_output_voltage=230.0(V)
norminal_ac_input_voltage=230.0(V)
battery_piece_number=4(ea)
battery_standard_voltage_per_unit=12.0(V)\n"""),
    ("DM", """model_code=050\n"""),
    ("INGS", """input_current_r=2.0(A)
input_current_s=1.9(A)
input_current_t=2.1(A)
output_current_r=0.2(A)
output_current_s=0.4(A)
output_current_t=0.5(A)
pbusvolt=380.9(V)
nbusvolt=380.9(V)
pbusavgv=381.0(V)
nbusavgv=380.7(V)
nlintcur=0.0(A)\n"""),
    ("EMINFO", """emfirst=1
deffeed-inpow=10000
actpvpow=5
actfeedpow=10
reservpow=0
emlast=1\n"""),
    ("PIRI", """ac_input_rated_voltage=240.0(V)
ac_input_rated_frequency=50.0(Hz)
ac_input_rated_current=41.6(A)
ac_output_rated_voltage=240.0(V)
ac_output_rated_current=41.6(A)
mppt_rated_current_per_string=18.7(A)
battery_rated_voltage=48.0(V)
mppt_track_number=2(ea)
machine_type=Hybrid type
topology=transformerless
parallel_for_output=enabled\n"""),
    ("GS", """solar_input_voltage_1=0.0(V)
solar_input_voltage_2=0.0(V)
solar_input_current_1=0.0(A)
solar_input_current_2=0.0(A)
battery_voltage=39.4(V)
battery_capacity=0(%)
battery_current=0.0(A)
ac_input_voltage_r=238.9(V)
ac_input_voltage_s=242.7(V)
ac_input_voltage_t=245.9(V)
ac_input_frequency=50.02(Hz)
ac_input_current_r=0.0(A)
ac_input_current_s=0.0(A)
ac_input_current_t=0.0(A)
ac_output_voltage_r=237.8(V)
ac_output_voltage_s=243.4(V)
ac_output_voltage_t=245.5(V)
ac_output_frequency=50.01(Hz)
ac_output_current_r=0.0(A)
ac_output_current_s=0.0(A)
ac_output_current_t=0.0(A)
inner_temperature=29(°C)
component_max_temperature=29(°C)
external_battery_temperature=0(°C)
setting_change_bit=No setting change\n"""),
    ("MOD", """working_mode=Hybrid mode (Line mode, Grid mode)\n"""),
    ("WS", """solar_input_1_loss=enabled
solar_input_2_loss=enabled
solar_input_1_voltage_too_high=disabled
solar_input_2_voltage_too_high=disabled
battery_under_voltage=enabled
battery_low_voltage=enabled
battery_disconnected=disabled
battery_over_voltage=disabled
battery_low_in_hybrid_mode=enabled
grid_voltage_high_loss=disabled
grid_voltage_low_loss=disabled
grid_frequency_high_loss=disabled
grid_frequency_low_loss=disabled
ac_input_long-time_average_voltage_over=disabled
ac_input_voltage_loss=disabled
ac_input_frequency_loss=disabled
ac_input_island=disabled
ac_input_phase_dislocation=disabled
over_temperature=disabled
over_load=disabled
emergency_power_off_active=disabled
ac_input_wave_loss=disabled\n"""),
    ("FLAG", """mute_buzzer_beep=Disabled
mute_buzzer_beep_in_standby_mode=Disabled
mute_buzzer_beep_only_on_battery_discharged_status=Enabled
generator_as_ac_input=Disabled
wide_ac_input_range=Enabled\n"""),
    ("T", """datetime=20210521234743(YYYYMMDDHHMMSS)\n"""),
    ("ET", """generated_energy_total=6591(kWh)\n"""),
    ("BATS", """battery_maximum_charge_current=200.0(A)
battery_constant_charge_voltage(c.v.)=58.4(V)
battery_floating_charge_voltage=57.6(V)
battery_stop_charger_current_level_in_floating_charging=0.0(A)
keep_charged_time_of_battery_catch_stopped_charging_current_level=0(Minutes)
battery_voltage_of_recover_to_charge_when_battery_stop_charger_in_floating_charging=57.6(V)
battery_under_voltage=46.0(V)
battery_under_voltage_release=51.0(V)
battery_weak_voltage_in_hybrid_mode=46.0(V)
battery_weak_voltage_release_in_hybrid_mode=51.0(V)
battery_type=Li-Fe
reserved=
battery_install_date=(YYYYMMDDHHMMSS)
ac_charger_keep_battery_voltage_function_enable/diable=Enabled
ac_charger_keep_battery_voltage=54.0(V)
battery_temperature_sensor_compensation=0.0(mV)
max._ac_charging_current=200.0(A)
battery_discharge_max_current_in_hybrid_mode=250(A)\n"""),
    ("HECS", """solar_energy_distribution_priority=Battery-Load-Grid
solar_charge_battery=disabled
ac_charge_battery=disabled
feed_power_to_utility=disabled
battery_discharge_to_loads_when_solar_input_normal=disabled
battery_discharge_to_loads_when_solar_input_loss=disabled
battery_discharge_to_feed_grid_when_solar_input_normal=disabled
battery_discharge_to_feed_grid_when_solar_input_loss=disabled\n"""),
    ("EY2023", """generated_energy_year=6591(Wh)\n"""),
    ("EM202301", """generated_energy_month=6591(Wh)\n"""),
    ("ED20230213", """generated_energy_day=91(Wh)\n"""),
    ("EH2023021323", """generated_energy_hour=1(Wh)\n"""),
]
# ("", """\n"""),
# ("DI", """\n"""),
# ("PS", """\n"""),


def do_test(self, command, expected, respno=0):
    try:
        # print(command, end=" ")
        respno += 1
        result = subprocess.run(
            [
                "mppsolar",
                "-p",
                "test0",
                "-P",
                "PI17",
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


class TestPi17(unittest.TestCase):
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

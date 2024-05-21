""" tests / unit / test_output_screen.py """
import contextlib
import io
import unittest

from mppsolar.outputs.screen import screen as op


class TestScreenOutput(unittest.TestCase):
    """ test the screen output module """
    maxDiff = 9999

    def test_screen_default(self):
        """ test the screen 'default' output """
        result = []
        # Get a mqtt output processor
        # op = get_outputs("mqtt")[0]
        tag = "test"
        data = {
            "raw_response": [
                "(1 92931701100510 B  0141 005 51.4 Ì#\r",
                "",
            ],
            "_command": "QPGS0",
            "_command_description": "Parallel Information inquiry",
            "Battery voltage": [51.4, "V"],
        }

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            op().output(data=data, tag=tag, keep_case=False, filter=None, excl_filter=None)
        result = f.getvalue()

        # needed to initialise variables
        expected = """Command: QPGS0 - Parallel Information inquiry
--------------------------------------------------------------------------------
Parameter       Value          Unit
battery_voltage 51.4           V
--------------------------------------------------------------------------------\n\n\n"""

        # print(result)
        self.assertEqual(result, expected)

    def test_screen_filter(self):
        """ test the screen filtered output """
        result = []
        # Get a mqtt output processor
        # op = get_outputs("mqtt")[0]
        tag = "test"
        inc_filter = "ac_output_active_power"
        excl_filter = None
        data = {'_command': 'QPIGS', '_command_description': 'General Status Parameters inquiry', 'raw_response': ['(000.0 00.0 230.0 49.9 0161 0119 003 460 57.50 012 100 0069 0014 103.8 57.45 00000 00110110 00 00 00856 010$\x8c\r', ''], 'AC Input Voltage': [0.0, 'V', {'icon': 'mdi:lightning'}], 'AC Input Frequency': [0.0, 'Hz'], 'AC Output Voltage': [230.0, 'V'], 'AC Output Frequency': [49.9, 'Hz'], 'AC Output Apparent Power': [161, 'VA'], 'AC Output Active Power': [119, 'W'], 'AC Output Load': [3, '%'], 'BUS Voltage': [460, 'V'], 'Battery Voltage': [57.5, 'V'], 'Battery Charging Current': [12, 'A'], 'Battery Capacity': [100, '%'], 'Inverter Heat Sink Temperature': [69, '°C'], 'PV Input Current for Battery': [14.0, 'A'], 'PV Input Voltage': [103.8, 'V'], 'Battery Voltage from SCC': [57.45, 'V'], 'Battery Discharge Current': [0, 'A'], 'Is SBU Priority Version Added': [0, 'bool'], 'Is Configuration Changed': [0, 'bool'], 'Is SCC Firmware Updated': [1, 'bool'], 'Is Load On': [1, 'bool'], 'Is Battery Voltage to Steady While Charging': [0, 'bool'], 'Is Charging On': [1, 'bool'], 'Is SCC Charging On': [1, 'bool'], 'Is AC Charging On': [0, 'bool'], 'RSV1': [0, 'A'], 'RSV2': [0, 'A'], 'PV Input Power': [856, 'W'], 'Is Charging to Float': [0, 'bool'], 'Is Switched On': [1, 'bool'], 'Is Reserved': [0, 'bool']}

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            op().output(data=data, tag=tag, keep_case=False, filter=inc_filter, excl_filter=excl_filter)
        result = f.getvalue()

        # needed to initialise variables
        expected = """Command: QPIGS - General Status Parameters inquiry
--------------------------------------------------------------------------------
Parameter              Value          Unit
ac_output_active_power 119            W
--------------------------------------------------------------------------------\n\n\n"""

        # print(result)
        self.assertEqual(result, expected)

    def test_screen_excl_filter(self):
        """ test the screen exclude filter output """
        result = []
        # Get a mqtt output processor
        # op = get_outputs("mqtt")[0]
        tag = "test"
        inc_filter = None
        excl_filter = "^ac|^pv|^is"
        data = {'_command': 'QPIGS', '_command_description': 'General Status Parameters inquiry', 'raw_response': ['(000.0 00.0 230.0 49.9 0161 0119 003 460 57.50 012 100 0069 0014 103.8 57.45 00000 00110110 00 00 00856 010$\x8c\r', ''], 'AC Input Voltage': [0.0, 'V', {'icon': 'mdi:lightning'}], 'AC Input Frequency': [0.0, 'Hz'], 'AC Output Voltage': [230.0, 'V'], 'AC Output Frequency': [49.9, 'Hz'], 'AC Output Apparent Power': [161, 'VA'], 'AC Output Active Power': [119, 'W'], 'AC Output Load': [3, '%'], 'BUS Voltage': [460, 'V'], 'Battery Voltage': [57.5, 'V'], 'Battery Charging Current': [12, 'A'], 'Battery Capacity': [100, '%'], 'Inverter Heat Sink Temperature': [69, '°C'], 'PV Input Current for Battery': [14.0, 'A'], 'PV Input Voltage': [103.8, 'V'], 'Battery Voltage from SCC': [57.45, 'V'], 'Battery Discharge Current': [0, 'A'], 'Is SBU Priority Version Added': [0, 'bool'], 'Is Configuration Changed': [0, 'bool'], 'Is SCC Firmware Updated': [1, 'bool'], 'Is Load On': [1, 'bool'], 'Is Battery Voltage to Steady While Charging': [0, 'bool'], 'Is Charging On': [1, 'bool'], 'Is SCC Charging On': [1, 'bool'], 'Is AC Charging On': [0, 'bool'], 'RSV1': [0, 'A'], 'RSV2': [0, 'A'], 'PV Input Power': [856, 'W'], 'Is Charging to Float': [0, 'bool'], 'Is Switched On': [1, 'bool'], 'Is Reserved': [0, 'bool']}

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            op().output(data=data, tag=tag, keep_case=False, filter=inc_filter, excl_filter=excl_filter)
        result = f.getvalue()

        # needed to initialise variables
        expected = """Command: QPIGS - General Status Parameters inquiry
--------------------------------------------------------------------------------
Parameter                      Value          Unit
bus_voltage                    460            V
battery_voltage                57.5           V
battery_charging_current       12             A
battery_capacity               100            %
inverter_heat_sink_temperature 69             °C
battery_voltage_from_scc       57.45          V
battery_discharge_current      0              A
rsv1                           0              A
rsv2                           0              A
--------------------------------------------------------------------------------\n\n\n"""

        # print(result)
        self.assertEqual(result, expected)

    def test_screen_both_filter(self):
        """ test the screen include and exclude filter output """
        result = []
        # Get a mqtt output processor
        # op = get_outputs("mqtt")[0]
        tag = "test"
        inc_filter = "current"
        excl_filter = "battery$"
        data = {'_command': 'QPIGS', '_command_description': 'General Status Parameters inquiry', 'raw_response': ['(000.0 00.0 230.0 49.9 0161 0119 003 460 57.50 012 100 0069 0014 103.8 57.45 00000 00110110 00 00 00856 010$\x8c\r', ''], 'AC Input Voltage': [0.0, 'V', {'icon': 'mdi:lightning'}], 'AC Input Frequency': [0.0, 'Hz'], 'AC Output Voltage': [230.0, 'V'], 'AC Output Frequency': [49.9, 'Hz'], 'AC Output Apparent Power': [161, 'VA'], 'AC Output Active Power': [119, 'W'], 'AC Output Load': [3, '%'], 'BUS Voltage': [460, 'V'], 'Battery Voltage': [57.5, 'V'], 'Battery Charging Current': [12, 'A'], 'Battery Capacity': [100, '%'], 'Inverter Heat Sink Temperature': [69, '°C'], 'PV Input Current for Battery': [14.0, 'A'], 'PV Input Voltage': [103.8, 'V'], 'Battery Voltage from SCC': [57.45, 'V'], 'Battery Discharge Current': [0, 'A'], 'Is SBU Priority Version Added': [0, 'bool'], 'Is Configuration Changed': [0, 'bool'], 'Is SCC Firmware Updated': [1, 'bool'], 'Is Load On': [1, 'bool'], 'Is Battery Voltage to Steady While Charging': [0, 'bool'], 'Is Charging On': [1, 'bool'], 'Is SCC Charging On': [1, 'bool'], 'Is AC Charging On': [0, 'bool'], 'RSV1': [0, 'A'], 'RSV2': [0, 'A'], 'PV Input Power': [856, 'W'], 'Is Charging to Float': [0, 'bool'], 'Is Switched On': [1, 'bool'], 'Is Reserved': [0, 'bool']}

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            op().output(data=data, tag=tag, keep_case=False, filter=inc_filter, excl_filter=excl_filter)
        result = f.getvalue()

        # needed to initialise variables
        expected = """Command: QPIGS - General Status Parameters inquiry
--------------------------------------------------------------------------------
Parameter                 Value          Unit
battery_charging_current  12             A
battery_discharge_current 0              A
--------------------------------------------------------------------------------\n\n\n"""

        # print(result)
        self.assertEqual(result, expected)

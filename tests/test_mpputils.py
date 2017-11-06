import unittest
from mppsolar import mpputils
from mppsolar import mppcommands


class test_mpputils(unittest.TestCase):
    def test_failed_initialisation(self):
        """ Initialisation should fail if no device provided """
        self.assertRaises(mppcommands.NoDeviceError, mpputils.mppUtils)

    def test_getserialnumber(self):
        """ Should return serial number """
        mp = mpputils.mppUtils('TEST')
        self.assertEqual(mp.getSerialNumber(), '9293333010501')

    def test_getknowncommands(self):
        """ Should return the list of commands """
        testCommands = ['-------- List of known commands --------', 'PBTnn: Set Battery Type', 'PSDVnn.n: Set Battery Cut-off Voltage', 'Q1: Q1 query', 'QBOOT: DSP Has Bootstrap inquiry', 'QDI: Device Default Settings inquiry', 'QDM: QDM query', 'QFLAG: Device Flag Status inquiry', 'QID: Device Serial Number inquiry', 'QMCHGCR: Max Charging Current Options inquiry', 'QMN: QMN query', 'QMUCHGCR: Max Utility Charging Current Options inquiry', 'QOPM: Output Mode inquiry', 'QPGSn: Parallel Information inquiry', 'QPI: Device Protocol ID inquiry', 'QPIGS: Device General Status Parameters inquiry', 'QPIRI: Device Current Settings inquiry', 'QPIWS: Device warning status inquiry', 'QVFW: Main CPU firmware version inquiry', 'QVFW2: Secondary CPU firmware version inquiry']
        mp = mpputils.mppUtils('TEST')
        knownCommands = mp.getKnownCommands()
        self.assertListEqual(testCommands, knownCommands)

    def test_getreponse(self):
        """ Should return test response """
        mp = mpputils.mppUtils('TEST')
        self.assertEqual(mp.getResponse('QID'), '9293333010501')

    def test_getreponsedict(self):
        """ Should return test response as a dict"""
        responseDict = {'serial_number': ['9293333010501', '']}
        mp = mpputils.mppUtils('TEST')
        self.assertDictEqual(mp.getResponseDict('QID'), responseDict)

    def test_getfullstatus(self):
        """ Should return full status """
        testStatus = {'sync_frequency': {'unit': '', 'value': '49.99'}, 'pv_input_current_for_battery': {'unit': 'A', 'value': '0014'}, 'ac_input_frequency': {'unit': 'Hz', 'value': '00.0'}, 'inverter_charge_status': {'unit': '', 'value': 'absorb'}, 'pv_input_voltage': {'unit': 'V', 'value': '103.8'}, 'inverter_temperature': {'unit': 'Deg_C', 'value': '044'}, 'battery_charging_current': {'unit': 'A', 'value': '012'}, 'ac_output_frequency': {'unit': 'Hz', 'value': '49.9'}, 'ac_input_voltage': {'unit': 'V', 'value': '00.0'}, 'battery_temperature': {'unit': 'Deg_C', 'value': '054'}, 'chargeaveragecurrent': {'unit': '', 'value': '00'}, 'battery_discharge_current': {'unit': 'A', 'value': '00000'}, 'battery_voltage': {'unit': 'V', 'value': '57.50'}, 'scc_pwm_temperature': {'unit': 'Deg_C', 'value': '062'}, 'battery_voltage_from_scc': {'unit': 'V', 'value': '57.45'}, 'fan_lock_status': {'unit': '', 'value': 'Not locked'}, 'allowscconflag': {'unit': '', 'value': '01'}, 'ac_output_load': {'unit': '%', 'value': '003'}, 'inverter_heat_sink_temperature': {'unit': 'Deg_C', 'value': '0069'}, 'fan_pwm_speed': {'unit': 'Percent', 'value': '0038'}, 'ac_output_active_power': {'unit': 'W', 'value': '0119'}, 'bus_voltage': {'unit': 'V', 'value': '460'}, 'scc_charge_power': {'unit': 'W', 'value': '0608'}, 'ac_output_voltage': {'unit': 'V', 'value': '230.0'}, 'battery_capacity': {'unit': '%', 'value': '100'}, 'transformer_temperature': {'unit': 'Deg_C', 'value': '069'}, 'scc_flag': {'unit': '', 'value': 'SCC is powered and communicating'}, 'ac_output_apparent_power': {'unit': 'VA', 'value': '0161'}}
        mp = mpputils.mppUtils('TEST')
        status = mp.getFullStatus()
        self.assertDictEqual(status, testStatus)

    def test_getSettings(self):
        """ Should return the settings """
        self.maxDiff = 3000
        testSettings = {'ac_output_frequency': {'default': '50.0', 'unit': 'Hz', 'value': '50.0'},
                'ac_output_voltage': {'default': '30.0', 'unit': 'V', 'value': '230.0'},
                'battery_bulk_charge_voltage': {'default': '56.4', 'unit': 'V', 'value': '56.4'},
                'battery_float_charge_voltage': {'default': '54.0', 'unit': 'V', 'value': '54.0'},
                'battery_recharge_voltage': {'default': '46.0', 'unit': 'V', 'value': '46.0'},
                'battery_redischarge_voltage': {'default': '54.0', 'unit': 'V', 'value': '54.0'},
                'battery_type': {'default': 'AGM', 'unit': '', 'value': 'AGM'},
                'battery_under_voltage': {'default': '42.0', 'unit': 'V', 'value': '42.0'},
                'buzzer': {'default': 'Enable', 'unit': '', 'value': ''},
                'charger_source_priority': {'default': 'Solar + Utility', 'unit': '', 'value': 'Utility first'},
                'input_voltage_range': {'default': 'Appliance', 'unit': '', 'value': 'UPS'},
                'lcd_backlight': {'default': 'On', 'unit': '', 'value': ''},
                'lcd_reset_to_default': {'default': '', 'unit': '', 'value': ''},
                'machine_type': {'default': '', 'unit': '', 'value': 'Off Grid'},
                'max_ac_charging_current': {'default': '0030', 'unit': 'A', 'value': '10'},
                'max_charging_current': {'default': '60', 'unit': 'A', 'value': '010'},
                'output_mode': {'default': 'single machine output', 'unit': '', 'value': 'single machine output'},
                'output_source_priority': {'default': 'Utility first', 'unit': '', 'value': 'Utility first'},
                'over_temperature_restart': {'default': 'Disable', 'unit': '', 'value': ''},
                'overload_bypass': {'default': 'Disable', 'unit': '', 'value': ''},
                'overload_restart': {'default': 'Disable', 'unit': '', 'value': ''},
                'power_saving': {'default': 'Disable', 'unit': '', 'value': ''},
                'primary_source_interrupt_alarm': {'default': 'Enable', 'unit': '', 'value': ''},
                'pv_ok_condition': {'default': 'As long as one unit of inverters has connect PV, parallel system will consider PV OK', 'unit': '',
                    'value': 'As long as one unit of inverters has connect PV, parallel system will consider PV OK'},
                'pv_power_balance': {'default': 'PV input max power will be the sum of the max charged power and loads power', 'unit': '',
                    'value': 'PV input max power will be the sum of the max charged power and loads power'},
                'record_fault_code': {'default': 'Disable', 'unit': '', 'value': ''}}
        mp = mpputils.mppUtils('TEST')
        settings = mp.getSettings()
        self.assertDictEqual(settings, testSettings)


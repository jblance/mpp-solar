"""
MPP Solar Inverter Command Library
library of utility and helpers for MPP Solar PIP-4048MS inverters
mpputils.py
"""

import logging
import mppcommands

logger = logging.getLogger()


def getVal(_dict, key, ind=None):
    if key not in _dict:
        return ""
    if ind is None:
        return _dict[key]
    else:
        return _dict[key][ind]


class mppUtils:
    """
    MPP Solar Inverter Utility Library
    """

    def __init__(self, serial_device=None, baud_rate=2400):
        if (serial_device is None):
            raise mppcommands.NoDeviceError("A serial device must be supplied, e.g. /dev/ttyUSB0")
        self.mp = mppcommands.mppCommands(serial_device, baud_rate)
        self._serial_number = None

    def getKnownCommands(self):
        return mppcommands.getKnownCommands()

    def getResponseDict(self, cmd):
        return self.mp.getResponseDict(cmd)

    def getResponse(self, cmd):
        return self.mp.getResponse(cmd)

    def getSerialNumber(self):
        if self._serial_number is None:
            response = self.mp.getResponseDict("QID")
            self._serial_number = response["serial_number"][0]
        return self._serial_number

    def getInverterStatus(self):
        """
        Helper function that returns the inverter status
        """
        response = self.mp.getResponseDict('Q1')
        # TODO: fix etc
        # is this better? - if so need to be able to build a dict of responses
        return response['inverter charge status']

    def getFullStatus(self):
        """
        Helper function that returns all the status data
        """
        status = {}
        # serial_number = self.getSerialNumber()
        data = self.mp.getResponseDict("Q1")
        data.update(self.mp.getResponseDict("QPIGS"))  # TODO: check if this actually works...

        # Need to get 'Parallel' info, but dont know what the parallel number for the correct inverter is...
        # parallel_data = self.mp.getResponseDict("QPGS0")
        # This 'hack' only works for 2 inverters in parallel.
        # if parallel_data['serial_number'][0] != self.getSerialNumber():
        #    parallel_data = self.mp.getResponseDict("QPGS1")
        # status_data.update(parallel_data)

        items = ['SCC Flag', 'AllowSccOnFlag', 'ChargeAverageCurrent', 'SCC PWM temperature',
                 'Inverter temperature', 'Battery temperature', 'Transformer temperature',
                 'Fan lock status', 'Fan PWM speed', 'SCC charge power', 'Sync frequency',
                 'Inverter charge status', 'AC Input Voltage', 'AC Input Frequency',
                 'AC Output Voltage', 'AC Output Frequency', 'AC Output Apparent Power',
                 'AC Output Active Power', 'AC Output Load', 'BUS Voltage', 'Battery Voltage',
                 'Battery Charging Current', 'Battery Capacity', 'Inverter Heat Sink Temperature',
                 'PV Input Current for Battery', 'PV Input Voltage', 'Battery Voltage from SCC',
                 'Battery Discharge Current']

        for item in items:
            key = '{}'.format(item).lower().replace(" ", "_")
            status[key] = {"value": data[key][0], "unit": data[key][1]}
        # Still have 'Device Status' from QPIGS
        # Still have QPGSn
        return status

    def getSettings(self):
        """
        Query inverter for all current settings
        """
        # serial_number = self.getSerialNumber()
        default_settings = self.mp.getResponseDict("QDI")
        current_settings = self.mp.getResponseDict("QPIRI")
        flag_settings = self.mp.getResponseDict("QFLAG")
        # current_settings.update(flag_settings)  # Combine current and flag settings dicts

        settings = {}
        # {"Battery Bulk Charge Voltage": {"unit": "V", "default": 56.4, "value": 57.4}}

        items = ["Battery Type", "Output Mode", "Battery Bulk Charge Voltage", "Battery Float Charge Voltage",
                 "Battery Under Voltage", "Battery Redischarge Voltage", "Battery Recharge Voltage", "Input Voltage Range",
                 "Charger Source Priority", "Max AC Charging Current", "Max Charging Current", "Output Source Priority",
                 "AC Output Voltage", "AC Output Frequency", "PV OK Condition", "PV Power Balance",
                 "Buzzer", "Power Saving", "Overload Restart", "Over Temperature Restart", "LCD Backlight", "Primary Source Interrupt Alarm",
                 "Record Fault Code", "Overload Bypass", "LCD Reset to Default", "Machine Type"]

        for item in items:
            key = '{}'.format(item).lower().replace(" ", "_")
            settings[key] = {"value": getVal(current_settings, key, 0),
                             "unit": getVal(current_settings, key, 1),
                             "default": getVal(default_settings, key, 0)}
        for key in flag_settings:
            _key = '{}'.format(key).lower().replace(" ", "_")
            settings[_key]['value'] = getVal(flag_settings, key, 0)
#        QPIRI
#        ['float', 'AC Input Voltage', 'V'],
#        ['float', 'AC Input Current', 'A'],
#        ['float', 'AC output rating current', 'A'],
#        ['int', 'AC output rating apparent power', 'VA'],
#        ['int', 'AC output rating active power', 'W'],
#        ['float', 'Battery rating voltage', 'V'],
#        ['int', 'Parallel max num', 'units'],
#        ['option', 'Topology', ['transformerless', 'transformer']],
        return settings

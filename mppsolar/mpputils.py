"""
MPP Solar Inverter Command Library
library of utility and helpers for MPP Solar PIP-4048MS inverters
mpputils.py
"""

import logging
logger = logging.getLogger()

import mppcommands

class mppUtils:
    """
    MPP Solar Inverter Utility Library
    """
    
    def __init__(self, serial_device, baud_rate=2400):
        self.mp = mppcommands.mppCommands(serial_device, baud_rate)
        self._serial_number = None
    
    def getSerialNumber(self):
        if self._serial_number == None:
            response = self.mp.getResponseDict("QID")
            self._serial_number = response["serial_number"]
        return self._serial_number
        
    def getInverterStatus(self):
        """
        Helper function that returns the inverter status
        """
        response = self.mp.getResponseDict('Q1')
        # TODO: fix etc  
        #is this better? - if so need to be able to build a dict of responses
        return response['inverter charge status']

    def getFullStatus(self):
        """
        Helper function that returns all the status data 
        """
        status = {}
        #serial_number = self.getSerialNumber()
        data = self.mp.getResponseDict("Q1")
        data.update(self.mp.getResponseDict("QPIGS")) #TODO: check if this actually works...
        
        #Need to get 'Parallel' info, but dont know what the parallel number for the correct inverter is...
        #parallel_data = self.mp.getResponseDict("QPGS0") 
        #This 'hack' only works for 2 inverters in parallel.
        #if parallel_data['serial_number'][0] != self.getSerialNumber():
        #    parallel_data = self.mp.getResponseDict("QPGS1") 
        #status_data.update(parallel_data)
        
        items = ['SCC Flag', 'AllowSccOnFlag', 'ChargeAverageCurrent', 'SCC PWM temperature', 'Inverter temperature', 'Battery temperature', 'Transformer temperature', 'Fan lock status', 'Fan PWM speed', 'SCC charge power', 'Sync frequency', 'Inverter charge status', 
        'AC Input Voltage', 'AC Input Frequency', 'AC Output Voltage', 'AC Output Frequency', 'AC Output Apparent Power', 'AC Output Active Power', 'AC Output Load', 'BUS Voltage', 'Battery Voltage', 'Battery Charging Current', 'Battery Capacity', 'Inverter Heat Sink Temperature', 'PV Input Current for Battery', 'PV Input Voltage', 'Battery Voltage from SCC', 'Battery Discharge Current', 
        ]
 
        for item in items:
            key = '{}'.format(item).lower().replace(" ", "_")
            status[key] = {"value": data[key][0], "unit": data[key][1]} 
        
        return status
        # 'QPIGS': ...
                      # ['flags', 'Device Status', [['Add SBU priority version - No', 'Add SBU priority version - Yes'],
                                                  # ['Configuration unchanged', 'Configuration changed'],
                                                  # ['SCC firmware version unchanged', 'SCC firmware version updated'],
                                                  # ['Load off', 'Load on'],
                                                  # ['Battery voltage not to steady while charging', 'Battery voltage to steady while charging'],
                                                  # ['Charging off', 'Charging on'],
                                                  # ['SCC charging off', 'SCC charging on'],
                                                  # ['AC charging off', 'AC charging on']]],     

        # 'QPGSn': [['option', 'Parallel instance number', ['Not valid', 'valid']],
                      # ['int', 'Serial number', ''],
                      # ['keyed', 'Work mode', {'P': 'Power On Mode',
                                              # 'S': 'Standby Mode',
                                              # 'L': 'Line Mode',
                                              # 'B': 'Battery Mode',
                                              # 'F': 'Fault Mode',
                                              # 'H': 'Power Saving Mode'}],
                      # ['keyed', 'Fault code', {'00': 'No fault',
                                               # '01': 'Fan is locked',
                                               # '02': 'Over temperature',
                                               # '03': 'Battery voltage is too high',
                                               # '04': 'Battery voltage is too low',
                                               # '05': 'Output short circuited or Over temperature',
                                               # '06': 'Output voltage is too high',
                                               # '07': 'Over load time out',
                                               # '08': 'Bus voltage is too high',
                                               # '09': 'Bus soft start failed',
                                               # '11': 'Main relay failed',
                                               # '51': 'Over current inverter',
                                               # '52': 'Bus soft start failed',
                                               # '53': 'Inverter soft start failed',
                                               # '54': 'Self-test failed',
                                               # '55': 'Over DC voltage on output of inverter',
                                               # '56': 'Battery connection is open',
                                               # '57': 'Current sensor failed',
                                               # '58': 'Output voltage is too low',
                                               # '60': 'Inverter negative power',
                                               # '71': 'Parallel version different',
                                               # '72': 'Output circuit failed',
                                               # '80': 'CAN communication failed',
                                               # '81': 'Parallel host line lost',
                                               # '82': 'Parallel synchronized signal lost',
                                               # '83': 'Parallel battery voltage detect different',
                                               # '84': 'Parallel Line voltage or frequency detect different',
                                               # '85': 'Parallel Line input current unbalanced',
                                               # '86': 'Parallel output setting different'}],
                      # ['float', 'Grid voltage', 'V'],
                      # ['float', 'Grid frequency', 'Hz'],
                      # ['float', 'AC output voltage', 'V'],
                      # ['float', 'AC output frequency', 'Hz'],
                      # ['int', 'AC output apparent power', 'VA'],
                      # ['int', 'AC output active power', 'W'],
                      # ['int', 'Load percentage', '%'],
                      # ['float', 'Battery voltage', 'V'],
                      # ['int', 'Battery charging current', 'A'],
                      # ['int', 'Battery capacity', '%'],
                      # ['float', 'PV Input Voltage', 'V'],
                      # ['int', 'Total charging current', 'A'],
                      # ['int', 'Total AC output apparent power', 'VA'],
                      # ['int', 'Total output active power', 'W'],
                      # ['int', 'Total AC output percentage', '%'],
                      # ['flags', 'Inverter Status', [['SCC Loss', 'SCC OK'],
                                                    # ['AC not charging', 'AC charging'],
                                                    # ['SCC not charging', 'SCC charging'],
                                                    # ['Battery not over', 'Battery over?'],
                                                    # ['Battery normal', 'Battery under'],
                                                    # ['Line ok', 'Line loss'],
                                                    # ['Load off', 'Load on'],
                                                    # ['Configuration unchanged', 'Configuration changed']
                                                    # ]],
                      # ['option', 'Output mode', ['single machine',
                                                 # 'parallel output',
                                                 # 'Phase 1 of 3 phase output',
                                                 # 'Phase 2 of 3 phase output',
                                                 # 'Phase 3 of 3 phase output']],
                      # ['option', 'Charger source priority', ['Utility first', 'Solar first', 'Solar + Utility', 'Solar only']],
                      # ['int', 'Max charger current', 'A'],
                      # ['int', 'Max charger range', 'A'],
                      # ['int', 'Max AC charger current', 'A'],
                      # ['int', 'PV input current', 'A'],
                      # ['int', 'Battery discharge current', 'A']],                                                  
    
    def getSettings(self):
        """
        Query inverter for all current settings
        """
        #serial_number = self.getSerialNumber()
        default_settings = self.mp.getResponseDict("QDI")
        current_settings = self.mp.getResponseDict("QPIRI")
        flag_settings = self.mp.getResponseDict("QFLAG")
        current_settings.update(flag_settings) #Combine current and flag settings dicts
        
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
            settings[key] = {"value": current_settings[key][0], "unit": current_settings[key][1], "default": default_settings[key][0]}
            
        return settings

        """
        QPIRI
        ['float', 'AC Input Voltage', 'V'],
        ['float', 'AC Input Current', 'A'],
        ['float', 'AC output rating current', 'A'],
        ['int', 'AC output rating apparent power', 'VA'],
        ['int', 'AC output rating active power', 'W'],
        ['float', 'Battery rating voltage', 'V'],
        ['int', 'Parallel max num', 'units'],
        ['option', 'Topology', ['transformerless', 'transformer']],
        """
       

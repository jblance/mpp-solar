"""
MPP Solar Inverter Command Library
reference library of serial commands (and responses) for PIP-4048MS inverters
mppcommands.py
"""
# TODO: check with pylint...

import ctypes
import serial
import time
import re
import logging
logger = logging.getLogger()


class MppSolarError(Exception):
    pass


class NoDeviceError(MppSolarError):
    pass


COMMAND = {'QPIRI': {'description': 'Device Current Settings inquiry', 'resp_code': 'QPIRI', 'type': 'QUERY'},
           'QDI': {'description': 'Device Default Settings inquiry', 'resp_code': 'QDI', 'type': 'QUERY'},
           'QPIGS': {'description': 'Device General Status Parameters inquiry', 'resp_code': 'QPIGS', 'type': 'QUERY'},
           'QPGSn': {'description': 'Parallel Information inquiry', 'resp_code': 'QPGSn', 'regex': re.compile(r'QPGS\d$'), 'type': 'QUERY'},
           'QFLAG': {'description': 'Device Flag Status inquiry', 'resp_code': 'QFLAG', 'type': 'QUERY'},
           'QVFW': {'description': 'Main CPU firmware version inquiry', 'resp_code': 'QVFW', 'type': 'QUERY'},
           'QVFW2': {'description': 'Secondary CPU firmware version inquiry', 'resp_code': 'QVFW2', 'type': 'QUERY'},
           'QPIWS': {'description': 'Device warning status inquiry', 'resp_code': 'QPIWS', 'type': 'QUERY'},
           'Q1': {'description': 'Q1 query', 'resp_code': 'Q1', 'type': 'QUERY'},
           'QMN': {'description': 'QMN query', 'resp_code': 'QMN', 'type': 'QUERY'},
           'QDM': {'description': 'QDM query', 'resp_code': 'QPGSn', 'type': 'QUERY'},
           'QPI': {'description': 'Device Protocol ID inquiry', 'resp_code': 'QPI', 'type': 'QUERY'},
           'QID': {'description': 'Device Serial Number inquiry', 'resp_code': 'QID', 'type': 'QUERY'},
           'QBOOT': {'description': 'DSP Has Bootstrap inquiry', 'resp_code': 'QBOOT', 'type': 'QUERY'},
           'QOPM': {'description': 'Output Mode inquiry', 'resp_code': 'QOPM', 'type': 'QUERY'},
           'QMCHGCR': {'description': 'Max Charging Current Options inquiry', 'resp_code': 'Q', 'type': 'QUERY'},
           'QMUCHGCR': {'description': 'Max Utility Charging Current Options inquiry', 'resp_code': 'Q', 'type': 'QUERY'},
           'PBTnn': {'description': 'Set Battery Type', 'resp_code': 'SET', 'regex': re.compile(r'PBT0[012]$'), 'type': 'SETTER'},
           'PSDVnn.n': {'description': 'Set Battery Cut-off Voltage', 'resp_code': 'SET', 'regex': re.compile(r'PSDV\d\d\.\d$'), 'type': 'SETTER'},
           }

RESPONSE = {'QPIRI': [['float', 'AC Input Voltage', 'V'],
                      ['float', 'AC Input Current', 'A'],
                      ['float', 'AC Output Voltage', 'V'],
                      ['float', 'AC Output Frequency', 'Hz'],
                      ['float', 'AC Output Current', 'A'],
                      ['int', 'AC Output Apparent Power', 'VA'],
                      ['int', 'AC Output Active Power', 'W'],
                      ['float', 'Battery Voltage', 'V'],
                      ['float', 'Battery Recharge Voltage', 'V'],
                      ['float', 'Battery Under Voltage', 'V'],
                      ['float', 'Battery Bulk Charge Voltage', 'V'],
                      ['float', 'Battery Float Charge Voltage', 'V'],
                      ['option', 'Battery Type', ['AGM', 'Flooded', 'User']],
                      ['int', 'Max AC Charging Current', 'A'],
                      ['int', 'Max Charging Current', 'A'],
                      ['option', 'Input Voltage Range', ['Appliance', 'UPS']],
                      ['option', 'Output Source Priority', ['Utility first', 'Solar first', 'SBU first']],
                      ['option', 'Charger Source Priority', ['Utility first', 'Solar first', 'Solar + Utility', 'Only solar charging permitted']],
                      ['int', 'Parallel Max Num', 'units'],
                      ['keyed', 'Machine Type', {'00': 'Grid tie', '01': 'Off Grid', '10': 'Hybrid'}],
                      ['option', 'Topology', ['transformerless', 'transformer']],
                      ['option', 'Output Mode', ['single machine output',
                                                 'parallel output',
                                                 'Phase 1 of 3 Phase output',
                                                 'Phase 2 of 3 Phase output',
                                                 'Phase 3 of 3 Phase output']],
                      ['float', 'Battery Redischarge Voltage', 'V'],
                      ['option', 'PV OK Condition', ['As long as one unit of inverters has connect PV, parallel system will consider PV OK',
                                                     'Only All of inverters have connect PV, parallel system will consider PV OK']],
                      ['option', 'PV Power Balance', ['PV input max current will be the max charged current',
                                                      'PV input max power will be the sum of the max charged power and loads power']],
                      ],
            'QPIGS': [['float', 'AC Input Voltage', 'V'],
                      ['float', 'AC Input Frequency', 'Hz'],
                      ['float', 'AC Output Voltage', 'V'],
                      ['float', 'AC Output Frequency', 'Hz'],
                      ['int', 'AC Output Apparent Power', 'VA'],
                      ['int', 'AC Output Active Power', 'W'],
                      ['int', 'AC Output Load', '%'],
                      ['int', 'BUS Voltage', 'V'],
                      ['float', 'Battery Voltage', 'V'],
                      ['int', 'Battery Charging Current', 'A'],
                      ['int', 'Battery Capacity', '%'],
                      ['int', 'Inverter Heat Sink Temperature', 'Deg_C'],
                      ['int', 'PV Input Current for Battery', 'A'],
                      ['float', 'PV Input Voltage', 'V'],
                      ['float', 'Battery Voltage from SCC', 'V'],
                      ['int', 'Battery Discharge Current', 'A'],
                      ['flags', 'Device Status', [['Add SBU priority version - No', 'Add SBU priority version - Yes'],
                                                  ['Configuration unchanged', 'Configuration changed'],
                                                  ['SCC firmware version unchanged', 'SCC firmware version updated'],
                                                  ['Load off', 'Load on'],
                                                  ['Battery voltage not to steady while charging', 'Battery voltage to steady while charging'],
                                                  ['Charging off', 'Charging on'],
                                                  ['SCC charging off', 'SCC charging on'],
                                                  ['AC charging off', 'AC charging on']]],
                      ],
            'QPGSn': [['option', 'Parallel instance number', ['Not valid', 'valid']],
                      ['int', 'Serial number', ''],
                      ['keyed', 'Work mode', {'P': 'Power On Mode',
                                              'S': 'Standby Mode',
                                              'L': 'Line Mode',
                                              'B': 'Battery Mode',
                                              'F': 'Fault Mode',
                                              'H': 'Power Saving Mode'}],
                      ['keyed', 'Fault code', {'00': 'No fault',
                                               '01': 'Fan is locked',
                                               '02': 'Over temperature',
                                               '03': 'Battery voltage is too high',
                                               '04': 'Battery voltage is too low',
                                               '05': 'Output short circuited or Over temperature',
                                               '06': 'Output voltage is too high',
                                               '07': 'Over load time out',
                                               '08': 'Bus voltage is too high',
                                               '09': 'Bus soft start failed',
                                               '11': 'Main relay failed',
                                               '51': 'Over current inverter',
                                               '52': 'Bus soft start failed',
                                               '53': 'Inverter soft start failed',
                                               '54': 'Self-test failed',
                                               '55': 'Over DC voltage on output of inverter',
                                               '56': 'Battery connection is open',
                                               '57': 'Current sensor failed',
                                               '58': 'Output voltage is too low',
                                               '60': 'Inverter negative power',
                                               '71': 'Parallel version different',
                                               '72': 'Output circuit failed',
                                               '80': 'CAN communication failed',
                                               '81': 'Parallel host line lost',
                                               '82': 'Parallel synchronized signal lost',
                                               '83': 'Parallel battery voltage detect different',
                                               '84': 'Parallel Line voltage or frequency detect different',
                                               '85': 'Parallel Line input current unbalanced',
                                               '86': 'Parallel output setting different'}],
                      ['float', 'Grid voltage', 'V'],
                      ['float', 'Grid frequency', 'Hz'],
                      ['float', 'AC output voltage', 'V'],
                      ['float', 'AC output frequency', 'Hz'],
                      ['int', 'AC output apparent power', 'VA'],
                      ['int', 'AC output active power', 'W'],
                      ['int', 'Load percentage', '%'],
                      ['float', 'Battery voltage', 'V'],
                      ['int', 'Battery charging current', 'A'],
                      ['int', 'Battery capacity', '%'],
                      ['float', 'PV Input Voltage', 'V'],
                      ['int', 'Total charging current', 'A'],
                      ['int', 'Total AC output apparent power', 'VA'],
                      ['int', 'Total output active power', 'W'],
                      ['int', 'Total AC output percentage', '%'],
                      ['flags', 'Inverter Status', [['SCC Loss', 'SCC OK'],
                                                    ['AC not charging', 'AC charging'],
                                                    ['SCC not charging', 'SCC charging'],
                                                    ['Battery not over', 'Battery over?'],
                                                    ['Battery normal', 'Battery under'],
                                                    ['Line ok', 'Line loss'],
                                                    ['Load off', 'Load on'],
                                                    ['Configuration unchanged', 'Configuration changed']
                                                    ]],
                      ['option', 'Output mode', ['single machine',
                                                 'parallel output',
                                                 'Phase 1 of 3 phase output',
                                                 'Phase 2 of 3 phase output',
                                                 'Phase 3 of 3 phase output']],
                      ['option', 'Charger source priority', ['Utility first', 'Solar first', 'Solar + Utility', 'Solar only']],
                      ['int', 'Max charger current', 'A'],
                      ['int', 'Max charger range', 'A'],
                      ['int', 'Max AC charger current', 'A'],
                      ['int', 'PV input current', 'A'],
                      ['int', 'Battery discharge current', 'A']],
            'QFLAG': [['enflags', 'Device Status', {'a': {'name': 'Buzzer', 'state': 'disabled'},
                                                    'b': {'name': 'Overload Bypass', 'state': 'disabled'},
                                                    'j': {'name': 'Power Saving', 'state': 'disabled'},
                                                    'k': {'name': 'LCD Reset to Default', 'state': 'disabled'},
                                                    'u': {'name': 'Overload Restart', 'state': 'disabled'},
                                                    'v': {'name': 'Over Temperature Restart', 'state': 'disabled'},
                                                    'x': {'name': 'LCD Backlight', 'state': 'disabled'},
                                                    'y': {'name': 'Primary Source Interrupt Alarm', 'state': 'disabled'},
                                                    'z': {'name': 'Record Fault Code', 'state': 'disabled'}}]],
            'QVFW': [['string', 'Main CPU firmware version', '']],
            'QVFW2': [['string', 'Secondary CPU firmware version', '']],
            'QPI': [['string', 'Protocol ID', '']],
            'Q': [['string', 'Response', '']],
            'QBOOT': [['option', 'DSP Has Bootstrap', ['No', 'Yes']]],
            'QID': [['string', 'Serial Number', '']],
            'QOPM': [['option', 'Output mode', ['single machine output',
                                                'parallel output',
                                                'Phase 1 of 3 Phase output',
                                                'Phase 2 of 3 Phase output',
                                                'Phase 3 of 3 Phase output']]],
            'QMN': [['string', 'QMN response', '']],
            'SET': [['ack', 'Command execution', {'NAK': 'Failed', 'ACK': 'Successful'}]],
            'QDI': [['float', 'AC Output Voltage', 'V'],
                    ['float', 'AC Output Frequency', 'Hz'],
                    ['int', 'Max AC Charging Current', 'A'],
                    ['float', 'Battery Under Voltage', 'V'],
                    ['float', 'Battery Float Charge Voltage', 'V'],
                    ['float', 'Battery Bulk Charge Voltage', 'V'],
                    ['float', 'Battery Recharge Voltage', 'V'],
                    ['int', 'Max Charging Current', 'A'],
                    ['option', 'Input Voltage Range', ['Appliance', 'UPS']],
                    ['option', 'Output Source Priority', ['Utility first', 'Solar first', 'SBU first']],
                    ['option', 'Charger Source Priority', ['Utility first', 'Solar first', 'Solar + Utility', 'Only solar charging permitted']],
                    ['option', 'Battery Type', ['AGM', 'Flooded', 'User']],
                    ['option', 'Buzzer', ['Enable', 'Disable']],
                    ['option', 'Power saving', ['Disable', 'Enable']],
                    ['option', 'Overload restart', ['Disable', 'Enable']],
                    ['option', 'Over temperature restart', ['Disable', 'Enable']],
                    ['option', 'LCD Backlight', ['Off', 'On']],
                    ['option', 'Primary source interrupt alarm', ['Disable', 'Enable']],
                    ['option', 'Record fault code', ['Disable', 'Enable']],
                    ['option', 'Overload bypass', ['Disable', 'Enable']],
                    ['option', 'LCD reset to default after 1min', ['Disable', 'Enable']],
                    ['option', 'Output mode', ['single machine output',
                                               'parallel output',
                                               'Phase 1 of 3 Phase output',
                                               'Phase 2 of 3 Phase output',
                                               'Phase 3 of 3 Phase output']],
                    ['float', 'Battery Redischarge Voltage', 'V'],
                    ['option', 'PV OK condition', ['As long as one unit of inverters has connect PV, parallel system will consider PV OK',
                                                   'Only All of inverters have connect PV, parallel system will consider PV OK']],
                    ['option', 'PV Power Balance', ['PV input max current will be the max charged current',
                                                    'PV input max power will be the sum of the max charged power and loads power']]],
            'Q1': [['int', 'Time until the end of absorb charging', 'sec'],
                   ['int', 'Time until the end of float charging', 'sec'],
                   ['option', 'SCC Flag', ['SCC not communicating?', 'SCC is powered and communicating']],
                   ['string', 'AllowSccOnFlag', ''],
                   ['string', 'ChargeAverageCurrent', ''],
                   ['int', 'SCC PWM temperature', 'Deg_C'],
                   ['int', 'Inverter temperature', 'Deg_C'],
                   ['int', 'Battery temperature', 'Deg_C'],
                   ['int', 'Transformer temperature', 'Deg_C'],
                   ['int', 'GPIO13', ''],
                   ['option', 'Fan lock status', ['Not locked', 'Locked']],
                   ['string', 'Not used', ''],
                   ['int', 'Fan PWM speed', 'Percent'],
                   ['int', 'SCC charge power', 'W'],
                   ['string', 'Parallel Warning??', ''],
                   ['float', 'Sync frequency', ''],
                   ['keyed', 'Inverter charge status', {'10': 'nocharging', '11': 'bulk stage', '12': 'absorb', '13': 'float'}]],
            'QPIWS': [['stat_flags', 'Warning status', ['Reserved',
                                                        'Inverter fault',
                                                        'Bus over fault',
                                                        'Bus under fault',
                                                        'Bus soft fail fault',
                                                        'Line fail warning',
                                                        'OPV short warning',
                                                        'Inverter voltage too low fault',
                                                        'Inverter voltage too high fault',
                                                        'Over temperature fault',
                                                        'Fan locked fault',
                                                        'Battery voltage to high fault',
                                                        'Battery low alarm warning',
                                                        'Reserved',
                                                        'Battery under shutdown warning',
                                                        'Reserved',
                                                        'Overload fault',
                                                        'EEPROM fault',
                                                        'Inverter over current fault',
                                                        'Inverter soft fail fault',
                                                        'Self test fail fault',
                                                        'OP DC voltage over fault',
                                                        'Bat open fault',
                                                        'Current sensor fail fault',
                                                        'Battery short fault',
                                                        'Power limit warning',
                                                        'PV voltage high warning',
                                                        'MPPT overload fault',
                                                        'MPPT overload warning',
                                                        'Battery too low to charge warning',
                                                        'Reserved',
                                                        'Reserved']]]
            }


def trunc(text):
    """
    Truncates / right pads supplied text
    """
    if len(text) >= 30:
        text = text[:30]
        return '{:<30}...'.format(text)
    return '{:<30}   '.format(text)


def crc(cmd):
    """
    Calculates CRC for supplied text
    """
    logging.info('Calculating CRC for %s', cmd)

    crc = 0
    da = 0
    crc_ta = [0x0000, 0x1021, 0x2042, 0x3063,
              0x4084, 0x50a5, 0x60c6, 0x70e7,
              0x8108, 0x9129, 0xa14a, 0xb16b,
              0xc18c, 0xd1ad, 0xe1ce, 0xf1ef]

    for c in cmd:
        logging.debug('Encoding %s', c)
        t_da = ctypes.c_uint8(crc >> 8)
        da = t_da.value >> 4
        crc <<= 4
        index = da ^ (ord(c) >> 4)
        crc ^= crc_ta[index]
        t_da = ctypes.c_uint8(crc >> 8)
        da = t_da.value >> 4
        crc <<= 4
        index = da ^ (ord(c) & 0x0f)
        crc ^= crc_ta[index]

    crc_low = ctypes.c_uint8(crc).value
    crc_high = ctypes.c_uint8(crc >> 8).value

    if (crc_low == 0x28 or crc_low == 0x0d or crc_low == 0x0a):
        crc_low += 1
    if (crc_high == 0x28 or crc_high == 0x0d or crc_high == 0x0a):
        crc_high += 1

    crc = crc_high << 8
    crc += crc_low

    logging.debug('Generated CRC %x %x %x', crc_high, crc_low, crc)
    return [crc_high, crc_low]


class mppCommands:
    """
    MPP Solar Inverter Command Library
    """
    """
    boolean setBatteryType(String value) # PBT<NN><cr>: Setting battery type
    result = excuteCommand("PBT", getFomatStr(value, 2));

    boolean setBatteryUnder(double value) # PSDV<nn.n><cr>:
        Setting battery cut-off voltage (Battery under voltage)
    result = excuteCommand("PSDV", String.format("%04.01f", new Object[]
        { Double.valueOf(value) }));
    """

    def __init__(self, serial_device=None, baud_rate=2400):
        if (serial_device is None):
            raise self.NoDeviceError()
        self._baud_rate = baud_rate
        self._serial_device = serial_device

    def getKnownCommands(self):
        """
        Provides a human readable list of all defined commands
        """
        msgs = []
        msgs.append('-------- List of known commands --------')
        for cmd in sorted(COMMAND):
            msgs.append('{}: {}'.format(cmd, COMMAND[cmd]['description']))
        return msgs

    def getCommandFullString(self, cmd):
        """
        Generates a full command including CRC and CR
        """
        logging.debug('Generate full command for %s', cmd)
        crc_high, crc_low = crc(cmd)
        full_command = '{}{}{}\x0d'.format(cmd, chr(crc_high), chr(crc_low))
        logging.debug('Full command: %s', full_command)
        return full_command

    def getCommandType(self, cmd):
        """
        Determines the type of command (QUERY, SETTER, UNKNOWN)
        """
        # Check if it is a known command
        # if not self.isValidCommand(cmd):
        #    return False
        if (cmd in COMMAND):
            logging.debug('Command %s is a %s - simple match', cmd, COMMAND[cmd]['type'])
            return COMMAND[cmd]['type']
        # Look through more complex matches
        for item in COMMAND:
            logging.debug('Checking %s', item)
            # If a regex is defined...
            if ('regex' in COMMAND[item]):
                logging.debug('Checking regex %s', COMMAND[item]['regex'])
                # ...check if the regex matches the supplied cmd
                if (COMMAND[item]['regex'].match(cmd)):
                    logging.debug('Command %s is a %s - complex match', cmd, COMMAND[item]['type'])
                    return COMMAND[item]['type']
        logging.info('Command %s is unknown', cmd)
        return 'UNKNOWN'

    def getCommandCode(self, cmd):
        """
        Returns reference for supplied command
        """
        if (cmd in COMMAND):
            logging.debug('Command %s reference is %s - simple match', cmd, cmd)
            return cmd  # This is the simple cast where cmd matches COMMAND keys (i.e. most queries)

        # What about complex cases like cmd = PBT01 (PBTnn) or PSDV44.0 (PSDVnn.n)
        # Loop through all known commands
        for item in COMMAND:
            logging.debug('Checking %s', item)
            # If a regex is defined...
            if ('regex' in COMMAND[item]):
                logging.debug('Checking regex %s', COMMAND[item]['regex'])
                # ...check if the regex matches the supplied cmd
                if (COMMAND[item]['regex'].match(cmd)):
                    logging.debug('Command %s reference is %s - complex match', cmd, item)
                    return item
        logging.info('Command %s has no reference', cmd)
        return None

    def getResponseDefinition(self, cmd):
        """
        Gets response definition of supplied command
        """
        logging.debug('Looking for a response for %s', cmd)
        cmd_reference = self.getCommandCode(cmd)
        if (cmd_reference is None):
            return None
        else:
            return RESPONSE[COMMAND[cmd_reference]['resp_code']]

    def isCommandValid(self, cmd):
        """
        Checks if supplied command is valid (i.e. a known command with a defined response)
        """
        if (cmd in COMMAND):
            logging.debug('Command %s is valid - simple match', cmd)
            return True  # This is the simple cast where cmd matches COMMAND keys (i.e. most queries)

        # What about complex cases like cmd = PBT01 (PBTnn) or PSDV44.0 (PSDVnn.n)
        # Loop through all known commands
        for item in COMMAND:
            logging.debug('Checking %s', item)
            # If a regex is defined...
            if ('regex' in COMMAND[item]):
                logging.debug('Checking regex %s', COMMAND[item]['regex'])
                # ...check if the regex matches the supplied cmd
                if (COMMAND[item]['regex'].match(cmd)):
                    logging.debug('Command %s is valid - complex match', cmd)
                    return True
        logging.info('Command %s is invalid', cmd)
        return False

    def isResponseValid(self, cmd, response):
        """
        Checks the response is valid
        - if command is not a query then valid responses are (NAK and (ACK
        - for queries
            - check that the response if the correct length
            - check CRC is correct
        """
        # Check length of response
        logging.debug('Response length: %d', len(response))
        if len(response) < 3:
            logging.debug('Response invalid as too short')
            return False
        # Check we got a CRC response that matches the data
        resp = response[:-3]
        resp_crc = response[-3:-1]
        logging.debug('CRC resp\t%x %x', ord(resp_crc[0]), ord(resp_crc[1]))
        calc_crc_h, calc_crc_l = crc(resp)
        logging.debug('CRC calc\t%x %x', calc_crc_h, calc_crc_l)
        if ((ord(resp_crc[0]) == calc_crc_h) and (ord(resp_crc[1]) == calc_crc_l)):
            logging.debug('CRCs match')
        else:
            logging.debug('Response invalid as calculated CRC does not match response CRC')
            return False

        # Check if this is a query or set command
        cmd_type = self.getCommandType(cmd)
        if (cmd_type != 'QUERY'):
            # Is set command - default to 'is valid'
            # TODO: what are valid responses...
            logging.debug('Response valid as is not query')
            return True
        # Check if we know about the command
        cmd_reference = self.getCommandCode(cmd)
        if (cmd_reference is None):
            logging.debug('Response invalid as no COMMAND defined for %s', cmd)
            return False
        # Check if valid response is defined for this command
        resp = self.getResponseDefinition(cmd)
        if (resp is None):
            logging.debug('Response invalid as no RESPONSE defined for %s', cmd)
            return False
        # Check we got the expected number of responses
        responses = response.split(" ")
        if (len(responses) < len(resp)):
            logging.error("Response invalid as insufficient number of elements in response. Got %d, expected as least %d", len(responses), len(resp))
            return False
        logging.debug('Response valid as no invalid situations found')
        return True

    def getResponse(self, cmd):
        """
        Returns the response unchanged
        """
        return self.execute(cmd)

    def getResponseDict(self, cmd):
        """
        Returns the response in a dict (with value, unit array)
        """
        msgs = {}

        # Execute command
        response = self.execute(cmd)
        if (response is None):
            logging.info('Command execution failed')
            return msgs

        # cmd_reference = self.getCommandCode(cmd)
        response_definition = self.getResponseDefinition(cmd)
        if (response_definition is None):
            logging.info('Was not valid response')
            return msgs

        responses = response.split(" ")
        for i, result in enumerate(responses):
            # Check if we are past the 'known' responses
            if (i >= len(response_definition)):
                resp_format = ['string', 'Unknown value in response', '']
            else:
                resp_format = response_definition[i]

            key = '{}'.format(resp_format[1]).lower().replace(" ", "_")
            # Process results
            if (resp_format[0] == 'float') or (resp_format[0] == 'int') or (resp_format[0] == 'string'):
                msgs[key] = [result, resp_format[2]]
            # eg. ['option', 'Output source priority', ['Utility first', 'Solar first', 'SBU first']],
            elif (resp_format[0] == 'option'):
                msgs[key] = [resp_format[2][int(result)], '']
            # eg. ['keyed', 'Machine type', {'00': 'Grid tie', '01': 'Off Grid', '10': 'Hybrid'}],
            elif (resp_format[0] == 'keyed'):
                msgs[key] = [resp_format[2][result], '']
            # eg. ['flags', 'Device status', [ ['Add SBU - No', 'Add SBU - ...
            elif (resp_format[0] == 'flags'):
                output = ''
                for j, flag in enumerate(result):
                    output = '{}\n\t- {}'.format(output,
                                                 resp_format[2][j][int(flag)])
                msgs[key] = [output, '']
            # eg. ['stat_flags', 'Warning status', ['Reserved', 'Inver...
            elif (resp_format[0] == 'stat_flags'):
                output = ''
                for j, flag in enumerate(result):
                    if (flag == '1'):
                        output = ('{}\n\t- {}'.format(output,
                                                      resp_format[2][j]))
                msgs[key] = [output, '']
            # eg. ['enflags', 'Device Status', {'a': {'name': 'Buzzer', 'state': 'disabled'},
            elif (resp_format[0] == 'enflags'):
                # output = {}
                status = 'unknown'
                for item in result:
                    if (item == 'E'):
                        status = 'enabled'
                    elif (item == 'D'):
                        status = 'disabled'
                    else:
                        # output[resp_format[2][item]['name']] = status
                        msgs[resp_format[2][item]['name']] = [status, '']
                # msgs[key] = [output, '']
            else:
                msgs[i] = [result, '']
        return msgs

    def getResponsePretty(self, cmd):
        """
        Returns the response in a human readable format
        """
        msgs = []

        # Execute command
        response = self.execute(cmd)
        if (response is None):
            logging.info('Command execution failed')
            return msgs

        cmd_reference = self.getCommandCode(cmd)
        response_definition = self.getResponseDefinition(cmd)
        if (response_definition is None):
            logging.info('Was not valid response')
            return msgs

        msgs.append('-------- {} --------'.format(COMMAND[cmd_reference]['description']))
        responses = response.split(" ")
        for i, result in enumerate(responses):
            # Check if we are past the 'known' responses
            if (i >= len(response_definition)):
                resp_format = ['string', 'Unknown value in response', '']
            else:
                resp_format = response_definition[i]

            # Process results
            # eg. ['float','Battery voltage','V'],
            if (resp_format[0] == 'float'):
                msg = '{}:{:0.1f}{}'.format(trunc(resp_format[1]), float(result), resp_format[2])
                msgs.append(msg)
            # eg. ['int', 'AC output rating apparent power', 'VA'],
            elif (resp_format[0] == 'int'):
                msg = '{}:{:d}{}'.format(trunc(resp_format[1]), int(result), resp_format[2])
                msgs.append(msg)
            # eg. ['option', 'Output source priority', ['Utility first', 'Solar first', 'SBU first']],
            elif (resp_format[0] == 'option'):
                msg = '{}:{}'.format(trunc(resp_format[1]), resp_format[2][int(result)])
                msgs.append(msg)
            # eg. ['keyed', 'Machine type', {'00': 'Grid tie', '01': 'Off Grid', '10': 'Hybrid'}],
            elif (resp_format[0] == 'keyed'):
                msg = '{}:{}'.format(trunc(resp_format[1]), resp_format[2][result])
                msgs.append(msg)
            # eg. ['flags', 'Device status', [ ['Add SBU - No', 'Add SBU - ...
            elif (resp_format[0] == 'flags'):
                output = ''
                for j, flag in enumerate(result):
                    output = '{}\n\t- {}'.format(output,
                                                 resp_format[2][j][int(flag)])
                msg = '{}{}'.format(trunc(resp_format[1]), output)
                msgs.append(msg)
            # eg. ['stat_flags', 'Warning status', ['Reserved', 'Inver...
            elif (resp_format[0] == 'stat_flags'):
                output = ''
                for j, flag in enumerate(result):
                    if (flag == '1'):
                        output = ('{}\n\t- {}'.format(output,
                                                      resp_format[2][j]))
                msg = '{}{}'.format(trunc(resp_format[1]), output)
                msgs.append(msg)
            # eg. ['string', 'QPI response', '']
            elif (resp_format[0] == 'string'):
                msg = '{}:{}'.format(trunc(resp_format[1]), result)
                msgs.append(msg)
            # eg. ['enflags', 'Device status', {'a': 'Buzzer', 'b': 'O ...
            # eg. ['enflags', 'Device Status', {'a': {'name': 'Buzzer', 'state': 'disabled'},
            elif (resp_format[0] == 'enflags'):
                output = ''
                status = 'unknown'
                for item in result:
                    if (item == 'E'):
                        status = 'enabled'
                    elif (item == 'D'):
                        status = 'disabled'
                    else:
                        output = '{}\n\t- {} {} '.format(output,
                                                         resp_format[2][item]['name'],
                                                         status)
                msg = '{}{}'.format(trunc(resp_format[1]), output)
                msgs.append(msg)
            else:
                msg = 'Unknown type {}: {}'.format(trunc(resp_format), result)
                msgs.append(msg)
        return msgs

    def doSerialCommand(self, full_cmd, cmd):
        """
        Opens serial connection, sends command (multiple times if needed)
        and returns the response
        """
        response_line = None
        logging.debug('port %s, baudrate %s', self._serial_device, self._baud_rate)
        with serial.serial_for_url(self._serial_device, self._baud_rate) as s:
            # Execute command multiple times, increase timeouts each time
            for x in (1, 2, 3, 4):
                logging.debug('Command execution attempt %d...', x)
                s.timeout = 1 + x
                s.write_timeout = 1 + x
                s.flushInput()
                s.flushOutput()
                s.write(full_cmd)
                time.sleep(0.5 * x)  # give serial port time to receive the data
                response_line = s.readline()
                logging.debug('serial response was: %s', response_line)
                if self.isResponseValid(cmd, response_line):
                    # return response without the start byte and the crc
                    return response_line[1:-3]
            logging.critical('Command execution failed')
            return None

    def execute(self, cmd):
        """
        Sends a command (as supplied) to inverter and returns the raw response
        """
        # Execute logic is different for a query compared to a setter
        cmd_type = self.getCommandType(cmd)
        full_cmd = self.getCommandFullString(cmd)
        logging.debug('called: execute with query %s', full_cmd)
        logging.debug('\t%s command type is %s', cmd, cmd_type)
        if (cmd_type == 'QUERY'):
            return self.doSerialCommand(full_cmd, cmd)
        elif (cmd_type == 'SETTER'):
            # TODO: now what...
            # ie. execute with cmd = PBT01 or PSDV44.0
            # how to show valid options?
            # show before and after?
            return self.doSerialCommand(full_cmd, cmd)
        else:
            # TODO: unknown command
            # Unknown command
            return self.doSerialCommand(full_cmd, cmd)

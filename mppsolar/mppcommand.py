"""
MPP Solar Inverter Command Library
reference library of serial commands (and responses) for PIP-4048MS inverters
mppcommand.py
"""
import ctypes
import logging
import random

log = logging.getLogger('MPP-Solar')


def crc(cmd):
    """
    Calculates CRC for supplied text
    """
    log.debug('Calculating CRC for %s', cmd)

    crc = 0
    da = 0
    crc_ta = [0x0000, 0x1021, 0x2042, 0x3063,
              0x4084, 0x50a5, 0x60c6, 0x70e7,
              0x8108, 0x9129, 0xa14a, 0xb16b,
              0xc18c, 0xd1ad, 0xe1ce, 0xf1ef]

    for c in cmd:
        # log.debug('Encoding %s', c)
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

    log.debug('Generated CRC %x %x %x', crc_high, crc_low, crc)
    return [crc_high, crc_low]


def get_full_command(cmd):
    """
    Generates a full command including CRC and CR
    """
    log.debug('Generate full command for %s', cmd)
    crc_high, crc_low = crc(cmd)
    full_command = '{}{}{}\x0d'.format(cmd, chr(crc_high), chr(crc_low))
    log.debug('Full command: %s', full_command)
    return full_command


class mppCommand(object):
    """
    Base Class for MPP Inverter Commands
    Each command (as stored in a <command>.json file) will be an instance of this class
    """

    def __str__(self):
        """ String representation of the command (including response) """
        if(self.response is None or len(self.response) < 3):
            return "{}\n{}\n{}\n".format(self.name, self.description, self.help)
        else:
            response = self.response[:-3]
            response_dict = self.response_dict
        return "{}\n{}\n{}\n{}\n{}".format(self.name, self.description, self.help, response, response_dict)

    def __init__(self, name, description, command_type, response_definition, test_responses=[], regex="", value=None, help=""):
        """ Return a command object """
        self.name = name
        self.description = description
        self.help = help
        self.command_type = command_type
        self.response_definition = response_definition
        self.response = None
        self.response_dict = None
        self.test_responses = test_responses
        self.regex = regex
        self.value = value
        if value is None:
            cmd_str = self.name
        else:
            cmd_str = "{}{}".format(self.name, self.value)
        self.full_command = get_full_command(cmd_str)
        self.valid_response = False

    def setValue(self, value):
        self.value = value
        self.full_command = get_full_command("{}{}".format(self.name, self.value))

    def clearResponse(self):
        self.response = None

    def setResponse(self, response):
        self.response = response
        self.valid_response = self.isResponseValid(response)
        if self.valid_response:
            self.response_dict = self.getResponseDict()

    def getResponse(self):
        return self.response

    def getTestResponse(self):
        """
        Return a random one of the test_responses
        """
        return self.test_responses[random.randrange(len(self.test_responses))]

    def isResponseValid(self, response):
        """
        Checks the response is valid
        +
        - if command is not a query then valid responses are (NAK and (ACK
        - for queries
            - check that the response if the correct length
            - check CRC is correct
        """
        # Check length of response
        log.debug('Response length: %d', len(response))
        if len(response) < 3:
            log.debug('Response invalid as too short')
            return False
        # Check we got a CRC response that matches the data
        resp = response[:-3]
        resp_crc = response[-3:-1]
        log.debug('CRC resp\t%x %x', ord(resp_crc[0]), ord(resp_crc[1]))
        calc_crc_h, calc_crc_l = crc(resp)
        log.debug('CRC calc\t%x %x', calc_crc_h, calc_crc_l)
        if ((ord(resp_crc[0]) == calc_crc_h) and (ord(resp_crc[1]) == calc_crc_l)):
            log.debug('CRCs match')
        else:
            log.debug('Response invalid as calculated CRC does not match response CRC')
            return False
        # Check if this is a query or set command
        if (self.command_type == 'SETTER'):
            if (response == '(ACK9 \r'):
                log.debug('Response valid as setter with ACK resp')
                return True
            if (response == '(NAKss\r'):
                log.debug('Response valid as setter with NAK resp')
                return True
            return False
        # Check if valid response is defined for this command
        if (self.response_definition is None):
            log.debug('Response invalid as no RESPONSE defined for %s', self.name)
            return False
        # Check we got the expected number of responses
        responses = response.split(" ")
        if (len(responses) < len(self.response_definition)):
            log.debug("Response invalid as insufficient number of elements in response. Got %d, expected as least %d", len(responses), len(self.response_definition))
            return False
        log.debug('Response valid as no invalid situations found')
        return True

    def getResponseDict(self):
        """
        Returns the response in a dict (with value, unit array)
        """
        msgs = {}

        if (self.response is None):
            log.info('No response')
            msgs['error'] = ['No response', '']
            return msgs
        if (not self.valid_response):
            log.info('Invalid response')
            msgs['error'] = ['Invalid response', '']
            msgs['result'] = [self.response.replace('\r', ''), '']
            return msgs
        if (self.response_definition is None):
            log.info('No response definition')
            msgs['error'] = ['No response definition', '']
            msgs['result'] = [self.response.replace('\r', ''), '']
            return msgs

        responses = self.response[1:-3].split(" ")
        for i, result in enumerate(responses):
            # Check if we are past the 'known' responses
            if (i >= len(self.response_definition)):
                resp_format = ['string', 'Unknown value in response', '']
            else:
                resp_format = self.response_definition[i]

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
            # eg. ['flags', 'Device status', [ 'is_load_on', 'is_charging_on' ...
            elif (resp_format[0] == 'flags'):
                for j, flag in enumerate(result):
                    msgs[resp_format[2][j]] = [int(flag), 'True - 1/False - 0']
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
            elif self.command_type == 'SETTER':
                msgs[self.name] = [result, '']
            else:
                msgs[i] = [result, '']
        return msgs

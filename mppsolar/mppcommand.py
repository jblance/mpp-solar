"""
MPP Solar Inverter Command Library
reference library of serial commands (and responses) for PIP-4048MS inverters
mppcommand.py
"""
import ctypes
import logging
import random

logger = logging.getLogger()


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


def get_full_command(cmd):
    """
    Generates a full command including CRC and CR
    """
    logging.debug('Generate full command for %s', cmd)
    crc_high, crc_low = crc(cmd)
    full_command = '{}{}{}\x0d'.format(cmd, chr(crc_high), chr(crc_low))
    logging.debug('Full command: %s', full_command)
    return full_command


class mppCommand(object):
    """
   Base Class for MPP Inverter Commands
    """

    def __str__(self):
        sb = []
        for key in sorted(self.__dict__):
            sb.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))
        return ', '.join(sb)

    def __repr__(self):
        return self.__str__()

    def __init__(self, name, description, command_type, response_definition, test_responses=[], regex="", value=None):
        """ Return a command object """
        self.name = name
        self.description = description
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

    def set_value(self, value):
        self.value = value
        self.full_command = get_full_command("{}{}".format(self.name, self.value))

    def set_response(self, response):
        self.response = response
        self.valid_response = self.is_response_valid(response)
        if self.valid_response:
            self.response_dict = self.get_response_dict()

    def get_test_response(self):
        """
        Return a random one of the test_responses
        """
        return self.test_responses[random.randrange(len(self.test_responses))]

    def is_response_valid(self, response):
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
            print ('Response invalid as calculated CRC does not match response CRC')
            return False
        # Check if this is a query or set command
        if (self.command_type == 'SETTER'):
            # Is set command - default to 'is valid'
            # TODO: what are valid responses...
            if (response == '(ACK9 \r'):
                logging.debug('Response valid as setter with ACK resp')
                return True
            if (response == '(NAKss\r'):
                logging.debug('Response valid as setter with NAK resp')
                return True
            return False
        # Check if valid response is defined for this command
        if (self.response_definition is None):
            logging.debug('Response invalid as no RESPONSE defined for %s', self.name)
            return False
        # Check we got the expected number of responses
        responses = response.split(" ")
        if (len(responses) < len(self.response_definition)):
            logging.error("Response invalid as insufficient number of elements in response. Got %d, expected as least %d", len(responses), len(self.response_definition))
            return False
        logging.debug('Response valid as no invalid situations found')
        return True

    def get_response_dict(self):
        """
        Returns the response in a dict (with value, unit array)
        """
        msgs = {}

        if (self.response is None):
            logging.info('No response')
            return msgs
        if (not self.valid_response):
            logging.info('Invalid response')
            return msgs
        if (self.response_definition is None):
            logging.info('No response definition')
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

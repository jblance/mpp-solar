"""
MPP Solar Inverter Command Library
reference library of serial commands (and responses) for PIP-4048MS inverters
mppcommand.py
"""

# Backward compatibility to python2
# from builtins import bytes

import ctypes
import logging
import random

log = logging.getLogger('MPP-Solar')


def nocrc(byte_cmd):
    """
    CRC function to provide no crc
    """
    return ['', '']


def crc(byte_cmd):
    """
    Calculates CRC for supplied byte_cmd
    """
    # assert type(byte_cmd) == bytes
    log.debug('Calculating CRC for %s', byte_cmd)

    crc = 0
    da = 0
    crc_ta = [0x0000, 0x1021, 0x2042, 0x3063,
              0x4084, 0x50a5, 0x60c6, 0x70e7,
              0x8108, 0x9129, 0xa14a, 0xb16b,
              0xc18c, 0xd1ad, 0xe1ce, 0xf1ef]

    for c in byte_cmd:
        # todo fix spaces
        if c == ' ':
            continue
        # log.debug('Encoding %s', c)
        # todo fix response for older python
        if type(c) == str:
            c = ord(c)
        t_da = ctypes.c_uint8(crc >> 8)
        da = t_da.value >> 4
        crc <<= 4
        index = da ^ (c >> 4)
        crc ^= crc_ta[index]
        t_da = ctypes.c_uint8(crc >> 8)
        da = t_da.value >> 4
        crc <<= 4
        index = da ^ (c & 0x0f)
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


def get_byte_command(cmd, crc_function):
    """
    Generates a byte command including CRC and CR
    """
    log.debug('Generate full byte command for %s', cmd)
    # Encode ASCII string to bytes
    byte_cmd = bytes(cmd, 'utf-8')
    # calculate the CRC
    crc_high, crc_low = crc_function(byte_cmd)
    if crc_high:
        # combine byte_cmd, CRC , return
        full_byte_command = byte_cmd + bytes([crc_high, crc_low, 13])
    else:
        full_byte_command = byte_cmd + bytes([13])
    log.debug('Full byte command: %s', full_byte_command)
    return full_byte_command


class mppCommand(object):
    """
    Base Class for MPP Inverter Commands
    Each command (as stored in a <command>.json file) will be an instance of this class
    """

    def __str__(self):
        """ String representation of the command (including byte_response) """
        if(self.byte_response is None or len(self.byte_response) < 3):
            return "{}\n{}\n{}\n".format(self.name, self.description, self.help)
        else:
            response = self.byte_response[:-3]
            response_dict = self.response_dict
        return "{}\n{}\n{}\n{}\n{}".format(self.name, self.description, self.help, response, response_dict)

    def __init__(self, name, description, command_type, response_definition, test_responses=[], regex='', value='', help='', crc_function='', prefix='', protocol=None):
        """ Return a command object """
        self.name = name
        self.description = description
        self.help = help
        self.prefix = prefix
        self.protocol = protocol
        self.command_type = command_type
        self.response_definition = response_definition
        self.byte_response = None
        self.response_dict = None
        self.test_responses = test_responses
        self.regex = regex
        self.value = value
        self.cmd_str = '{}{}{}'.format(self.prefix, self.name, self.value)
        if crc_function == 'nocrc':
            self.crc_function = nocrc
        else:
            self.crc_function = crc
        self.byte_command = get_byte_command(self.cmd_str, self.crc_function)
        self.valid_response = False

    def setValue(self, value):
        self.value = value
        self.cmd_str = "{}{}".format(self.name, self.value)
        self.byte_command = get_byte_command("{}{}".format(self.name, self.value), self.crc_function)

    def clearByteResponse(self):
        self.byte_response = None

    def setByteResponse(self, byte_response):
        self.byte_response = byte_response
        self.valid_response = self.isByteResponseValid(self.byte_response)
        if self.valid_response:
            self.response_dict = self.getResponseDict()

    def getByteResponse(self):
        return self.byte_response

    def getResponse(self):
        result = ''
        try:
            if self.protocol == 'PI18':
                result = self.byte_response[5:-3].decode('utf-8')
                result = result.split(',')
            else:
                result = self.byte_response[1:-3].decode('utf-8')
                result = result.split(' ')
        except:  # noqa: E722
            pass
        return result

    def getTestByteResponse(self):
        """
        Return a random one of the test_responses
        """
        response = self.test_responses[random.randrange(len(self.test_responses))]
        if not response:
            return ''
        resp_data, crc_hex = response
        try:
            result = bytes(resp_data, 'utf-8') + bytes(bytearray.fromhex(crc_hex)) + bytes('\r', 'utf-8')
        except:  # noqa: E722
            result - ''
        return result

    def isByteResponseValid(self, byte_response):
        """
        Checks the byte byte_response is valid
        +
        - if command is not a query then valid responses are (NAK and (ACK
        - for queries
            - check that the byte_response if the correct length
            - check CRC is correct
        """
        # Check length of byte_response
        log.debug('Byte_Response length: %d', len(byte_response))
        if len(byte_response) < 3:
            log.debug('Byte Response invalid as too short')
            return False
        # Check we got a CRC byte_response that matches the data
        resp = byte_response[:-3]
        resp_crc = byte_response[-3:-1]
        if type(resp_crc) == str:
            resp_crc = bytes()
            resp_crc = (ord(byte_response[-3:-2]), ord(byte_response[-2:-1]))
        log.debug('CRC resp\t {}, {}'.format(resp_crc[0], resp_crc[1]))
        calc_crc_h, calc_crc_l = crc(resp)
        log.debug('CRC calc\t {} {}'.format(calc_crc_h, calc_crc_l))
        if ((resp_crc[0] == calc_crc_h) and (resp_crc[1] == calc_crc_l)):
            log.debug('CRCs match')
        else:
            log.debug('Response invalid as calculated CRC does not match byte_response CRC')
            return False

        # Check if this is a query or set command
        if (self.command_type == 'SETTER'):
            if (byte_response == bytes('(ACK9 \r', 'utf-8')):
                log.debug('Response valid as setter with ACK resp')
                return True
            if (byte_response == bytes('(NAKss\r', 'utf-8')):
                log.debug('Response valid as setter with NAK resp')
                return True
            return False
        else:
            if (byte_response == bytes('(NAKss\r', 'utf-8')):
                log.debug('Response invalid as query with NAK resp')
                return False
        # Check if valid byte_response is defined for this command
        if (self.response_definition is None):
            log.debug('Response invalid as no RESPONSE defined for %s', self.name)
            return False
        # Omit the CRC checksum and convert back to a string
        response = resp.decode()
        # Check we got the expected number of responses
        responses = response.split(" ")
        if (len(responses) < len(self.response_definition)):
            log.debug("Response invalid as insufficient number of elements in byte_response. Got %d, expected as least %d", len(responses), len(self.response_definition))
            return False
        log.debug('Response valid as no invalid situations found')
        return True

    def getInfluxLineProtocol2(self):
        """
        Returns the byte_response in InfluxDB line protocol format
        """
        msgs = []

        # Deal with non-valid responses
        if (self.byte_response is None):
            log.info('No byte_response')
            return msgs
        if (not self.valid_response):
            log.info('Invalid byte_response')
            return msgs
        if (self.response_definition is None):
            log.info('No byte_response definition')
            return msgs
        # mpp-solar,command=QPGS0 max_charger_range=120.0
        # +-----------+--------+-+---------+-+---------+
        # |measurement,tag_set field_set
        # +-----------+--------+-+---------+-+---------+
        # msgs.append('{}={}'.format(key, float(result)))

        # Build array of Influx Line Protocol messages
        responses = self.getResponse()
        for i, result in enumerate(responses):
            # result = result.decode('utf-8')
            # Check if we are past the 'known' responses
            if (i >= len(self.response_definition)):
                # If we dont know what this value is, we'll ignore it
                log.info('No byte_response definition - ignoring')
            else:
                resp_format = self.response_definition[i]

            key = '{}'.format(resp_format[1]).lower().replace(" ", "_")
            # Process results
            if (resp_format[0] == 'float') or (resp_format[0] == 'int'):
                msgs.append('{}={}'.format(key, float(result)))
            elif (resp_format[0] == '10int'):
                msgs.append('{}={}'.format(key, float(result) / 10))
            elif (resp_format[0] == 'string'):
                msgs.append('{}="{}"'.format(key, result))
            # eg. ['option', 'Output source priority', ['Utility first', 'Solar first', 'SBU first']],
            elif (resp_format[0] == 'option'):
                value = resp_format[2][int(result)]
                msgs.append('{}="{}"'.format(key, value))
            # eg. ['keyed', 'Machine type', {'00': 'Grid tie', '01': 'Off Grid', '10': 'Hybrid'}],
            elif (resp_format[0] == 'keyed'):
                value = resp_format[2][result]
                msgs.append('{}="{}"'.format(key, value))
            # eg. ['flags', 'Device status', [ 'is_load_on', 'is_charging_on' ...
            elif (resp_format[0] == 'flags'):
                for j, flag in enumerate(result):
                    key = resp_format[2][j]
                    value = int(flag)
                    msgs.append('{}={}'.format(key, value))
            # eg. ['stat_flags', 'Warning status', ['Reserved', 'Inver...
            elif (resp_format[0] == 'stat_flags'):
                # output = ''
                # TODO
                log.warning("StatFlags not implemented in Influx Line Protocol yet")
                # for j, flag in enumerate(result):
                #    if (flag == '1'):
                #        output = ('{}\n\t- {}'.format(output,
                #                                      resp_format[2][j]))
                # msgs[key] = [output, '']
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
                        key = resp_format[2][item]['name']
                        msgs.append('{}={}'.format(key, status))
                # msgs[key] = [output, '']
            elif self.command_type == 'SETTER':
                return msgs
            else:
                pass
                # msgs[i] = [result, '']
        return msgs

    def getInfluxLineProtocol(self):
        """
        Returns the byte_response in InfluxDB line protocol format
        """
        msgs = []

        # Deal with non-valid responses
        if (self.byte_response is None):
            log.info('No byte_response')
            return msgs
        if (not self.valid_response):
            log.info('Invalid byte_response')
            return msgs
        if (self.response_definition is None):
            log.info('No byte_response definition')
            return msgs
        # weather,location=us-midwest temperature=82 1465839830100400200
        # |    -------------------- --------------  |
        # |             |             |             |
        # |             |             |             |
        # +-----------+--------+-+---------+-+---------+
        # |measurement|,tag_set| |field_set| |timestamp|
        # +-----------+--------+-+---------+-+---------+
        # measurement not included
        # setting=<setting> unit=<value>>

        # Build array of Influx Line Protocol messages
        # responses = self.byte_response[1:-3].split(b" ")
        responses = self.getResponse()
        for i, result in enumerate(responses):
            # Check if we are past the 'known' responses
            if (i >= len(self.response_definition)):
                # If we dont know what this value is, we'll ignore it
                log.info('No byte_response definition - ignoring')
            else:
                resp_format = self.response_definition[i]

            key = '{}'.format(resp_format[1]).lower().replace(" ", "_")
            # Process results
            if (resp_format[0] == 'float') or (resp_format[0] == 'int'):
                msgs.append('setting={} nvalue={},unit="{}"'.format(key, float(result), resp_format[2]))
            elif (resp_format[0] == '10int'):
                msgs.append('setting={} nvalue={},unit="{}"'.format(key, float(result) / 10, resp_format[2]))
            elif (resp_format[0] == 'string'):
                msgs.append('setting={} value="{}",unit="{}"'.format(key, result, resp_format[2]))
            # eg. ['option', 'Output source priority', ['Utility first', 'Solar first', 'SBU first']],
            elif (resp_format[0] == 'option'):
                value = resp_format[2][int(result)]
                msgs.append('setting={} value="{}",unit="{}"'.format(key, value, ''))
            # eg. ['keyed', 'Machine type', {'00': 'Grid tie', '01': 'Off Grid', '10': 'Hybrid'}],
            elif (resp_format[0] == 'keyed'):
                value = resp_format[2][result]
                msgs.append('setting={} value="{}",unit="{}"'.format(key, value, ''))
            # eg. ['flags', 'Device status', [ 'is_load_on', 'is_charging_on' ...
            elif (resp_format[0] == 'flags'):
                for j, flag in enumerate(result):
                    key = resp_format[2][j]
                    value = int(flag)
                    msgs.append('setting={} nvalue={},unit="{}"'.format(key, value, ''))
            # eg. ['stat_flags', 'Warning status', ['Reserved', 'Inver...
            elif (resp_format[0] == 'stat_flags'):
                # output = ''
                # TODO
                log.warning("StatFlags not implemented in Influx Line Protocol yet")
                # for j, flag in enumerate(result):
                #    if (flag == '1'):
                #        output = ('{}\n\t- {}'.format(output,
                #                                      resp_format[2][j]))
                # msgs[key] = [output, '']
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
                        key = resp_format[2][item]['name']
                        msgs.append('setting={} value={},unit="{}"'.format(key, status, ''))
                # msgs[key] = [output, '']
            elif self.command_type == 'SETTER':
                return msgs
            else:
                pass
                # msgs[i] = [result, '']
        return msgs

    def getResponseDict(self):
        """
        Returns the byte_response in a dict (with value, unit array)
        """
        msgs = {}

        if (self.byte_response is None):
            log.info('No byte_response')
            msgs['error'] = ['No byte_response', '']
            return msgs
        if (not self.valid_response):
            log.info('Invalid byte_response')
            msgs['error'] = ['Invalid byte_response', '']
            msgs['response'] = [' '.join(self.getResponse()), '']
            return msgs
        if (self.response_definition is None):
            log.info('No byte_response definition')
            msgs['error'] = ['No byte_response definition', '']
            msgs['response'] = [' '.join(self.getResponse()), '']
            return msgs

        # Omit the CRC and convert to string
        # response = self.getResponse()
        # responses = response.split(" ")
        responses = self.getResponse()
        for i, result in enumerate(responses):
            # Check if we are past the 'known' responses
            if (i >= len(self.response_definition)):
                resp_format = ['string', 'Unknown value in byte_response', '']
            else:
                resp_format = self.response_definition[i]

            key = '{}'.format(resp_format[1]).lower().replace(" ", "_")
            # Process results
            if (resp_format[0] == 'float'):
                msgs[key] = [float(result), resp_format[2]]
            elif (resp_format[0] == 'int'):
                msgs[key] = [int(result), resp_format[2]]
            elif (resp_format[0] == 'string'):
                msgs[key] = [result, resp_format[2]]
            elif (resp_format[0] == '10int'):
                msgs[key] = [float(result) / 10, resp_format[2]]
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

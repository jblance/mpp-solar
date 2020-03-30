"""
MPP Solar Inverter Command Library
reference library of serial commands (and responses) for PIP-4048MS inverters
mppcommand.py
"""
import ctypes
import logging
import random

log = logging.getLogger('MPP-Solar')


def crc2(cmd):
    crc_tb =  [0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7, 0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef, 0x1231, 0x0210, 0x3273, 0x2252, 0x52b5, 0x4294, 0x72f7, 0x62d6, 0x9339, 0x8318, 0xb37b, 0xa35a, 0xd3bd, 0xc39c, 0xf3ff, 0xe3de, 0x2462, 0x3443, 0x0420, 0x1401, 0x64e6, 0x74c7, 0x44a4, 0x5485, 0xa56a, 0xb54b, 0x8528, 0x9509, 0xe5ee, 0xf5cf, 0xc5ac, 0xd58d, 0x3653, 0x2672, 0x1611, 0x0630, 0x76d7, 0x66f6, 0x5695, 0x46b4, 0xb75b, 0xa77a, 0x9719, 0x8738, 0xf7df, 0xe7fe, 0xd79d, 0xc7bc, 0x48c4, 0x58e5, 0x6886, 0x78a7, 0x0840, 0x1861, 0x2802, 0x3823, 0xc9cc, 0xd9ed, 0xe98e, 0xf9af, 0x8948, 0x9969, 0xa90a, 0xb92b, 0x5af5, 0x4ad4, 0x7ab7, 0x6a96, 0x1a71, 0x0a50, 0x3a33, 0x2a12, 0xdbfd, 0xcbdc, 0xfbbf, 0xeb9e, 0x9b79, 0x8b58, 0xbb3b, 0xab1a, 0x6ca6, 0x7c87, 0x4ce4, 0x5cc5, 0x2c22, 0x3c03, 0x0c60, 0x1c41, 0xedae, 0xfd8f, 0xcdec, 0xddcd, 0xad2a, 0xbd0b, 0x8d68, 0x9d49, 0x7e97, 0x6eb6, 0x5ed5, 0x4ef4, 0x3e13, 0x2e32, 0x1e51, 0x0e70, 0xff9f, 0xefbe, 0xdfdd, 0xcffc, 0xbf1b, 0xaf3a, 0x9f59, 0x8f78, 0x9188, 0x81a9, 0xb1ca, 0xa1eb, 0xd10c, 0xc12d, 0xf14e, 0xe16f, 0x1080, 0x1080, 0x30c2, 0x20e3, 0x5004, 0x4025, 0x7046, 0x6067, 0x83b9, 0x9398, 0xa3fb, 0xb3da, 0xc33d, 0xd31c, 0xe37f, 0xf35e, 0x02b1, 0x1290, 0x22f3, 0x32d2, 0x4235, 0x5214, 0x6277, 0x7256, 0xb5ea, 0xa5cb, 0x95a8, 0x8589, 0xf56e, 0xe54f, 0xd52c, 0xc50d, 0x34e2, 0x24c3, 0x14a0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405, 0xa7db, 0xb7fa, 0x8799, 0x97b8, 0xe75f, 0xf77e, 0xc71d, 0xd73c, 0x26d3, 0x36f2, 0x0691, 0x16b0, 0x6657, 0x7676, 0x4615, 0x5634, 0xd94c, 0xc96d, 0xf90e, 0xe92f, 0x99c8, 0x89e9, 0xb98a, 0xa9ab, 0x5844, 0x4865, 0x7806, 0x6827, 0x18c0, 0x08e1, 0x3882, 0x28a3, 0xcb7d, 0xdb5c, 0xeb3f, 0xfb1e, 0x8bf9, 0x9bd8, 0xabbb, 0xbb9a, 0x4a75, 0x5a54, 0x6a37, 0x7a16, 0x0af1, 0x1ad0, 0x2ab3, 0x3a92, 0xfd2e, 0xed0f, 0xdd6c, 0xcd4d, 0xbdaa, 0xad8b, 0x9de8, 0x8dc9, 0x7c26, 0x6c07, 0x5c64, 0x4c45, 0x3ca2, 0x2c83, 0x1ce0, 0x0cc1, 0xef1f, 0xff3e, 0xcf5d, 0xdf7c, 0xaf9b, 0xbfba, 0x8fd9, 0x9ff8, 0x6e17, 0x7e36, 0x4e55, 0x5e74, 0x2e93, 0x3eb2, 0x0ed1, 0x1ef0 ]

    crc = 0
    da = 0
    for c in cmd:
        log.debug('Encoding %s', c)
        # int da = 0xFF & (0xFF & crc >> 8) >> 4;               # java
        t_da = ctypes.c_uint8(crc >> 8)           # CRC Orig
        da = t_da.value >> 4                        # CRC Orig
        # crc <<= 4;                                            # java
        crc <<= 4                                   # CRC Orig
        # crc ^= CRCUtil.crc_tb[0xFF & (da ^ pByte[i] >> 4)];   # java
        # index = da ^ (ord(c) >> 4)                # CRC Orig
        index = da ^ ord(c) >> 4
        crc ^= crc_tb[index]
        # da = (0xFF & (0xFF & crc >> 8) >> 4);                 # java
        t_da = ctypes.c_uint8(crc >> 8)           # CRC Orig
        # t_da = 0xFF & (ctypes.c_uint8(0xFF & crc >> 8))
        da = t_da.value >> 4                        # CRC Orig
        # crc <<= 4;                                            # java
        crc <<= 4                                   # CRC Orig
        # final int temp = 0xFF & (da ^ (pByte[i] & 0xF));      # java
        index = da ^ (ord(c) & 0x0f)              # CRC Orig
        #index = 0xFF & (da ^ (ord(c) & 0x0f))
        # crc ^= CRCUtil.crc_tb[temp];                          # java
        # crc ^= crc_ta[index]                      # CRC Orig
        crc ^= crc_tb[index]
        # ++i;
        #}
    # end of for loop
    # int bCRCLow = 0xFF & crc;                                 # java
    crc_low = ctypes.c_uint8(crc).value             # CRC Orig
    #         int bCRCHign = 0xFF & crc >> 8;
    crc_high = ctypes.c_uint8(crc >> 8).value  # CRC Orig
    #         if (bCRCLow == 40 || bCRCLow == 13 || bCRCLow == 10) {
    #             ++bCRCLow;
    #         }
    if (crc_low == 0x28 or crc_low == 0x0d or crc_low == 0x0a):  # CRC Orig
        crc_low += 1  # CRC Orig
    #         if (bCRCHign == 40 || bCRCHign == 13 || bCRCHign == 10) {
    #             ++bCRCHign;
    #         }
    if (crc_high == 0x28 or crc_high == 0x0d or crc_high == 0x0a):  # CRC Orig
        crc_high += 1  # CRC Orig
    #         crc = (0xFF & bCRCHign) << 8;
    crc = crc_high << 8  # CRC Orig
    #         crc += bCRCLow;
    crc += crc_low  # CRC Orig
    #         return crc;
    #     }
    #     catch (Exception ex) {
    #         ex.printStackTrace();
    #         return 0;
    #     }
    # }
    log.debug('Generated CRC %x %x %x', crc_high, crc_low, crc)  # CRC Orig
    return [crc_high, crc_low]          # CRC Orig


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
            msgs['response'] = [self.response.replace('\r', ''), '']
            return msgs
        if (self.response_definition is None):
            log.info('No response definition')
            msgs['error'] = ['No response definition', '']
            msgs['response'] = [self.response.replace('\r', ''), '']
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

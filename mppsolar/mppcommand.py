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
    crc_tb =  ['\0', '\u1021', '\u2042', '\u3063', '\u4084', '\u50a5', '\u60c6', '\u70e7', '\u8108', '\u9129', '\ua14a', '\ub16b', '\uc18c', '\ud1ad', '\ue1ce', '\uf1ef', '\u1231', '\u0210', '\u3273', '\u2252', '\u52b5', '\u4294', '\u72f7', '\u62d6', '\u9339', '\u8318', '\ub37b', '\ua35a', '\ud3bd', '\uc39c', '\uf3ff', '\ue3de', '\u2462', '\u3443', '\u0420', '\u1401', '\u64e6', '\u74c7', '\u44a4', '\u5485', '\ua56a', '\ub54b', '\u8528', '\u9509', '\ue5ee', '\uf5cf', '\uc5ac', '\ud58d', '\u3653', '\u2672', '\u1611', '\u0630', '\u76d7', '\u66f6', '\u5695', '\u46b4', '\ub75b', '\ua77a', '\u9719', '\u8738', '\uf7df', '\ue7fe', '\ud79d', '\uc7bc', '\u48c4', '\u58e5', '\u6886', '\u78a7', '\u0840', '\u1861', '\u2802', '\u3823', '\uc9cc', '\ud9ed', '\ue98e', '\uf9af', '\u8948', '\u9969', '\ua90a', '\ub92b', '\u5af5', '\u4ad4', '\u7ab7', '\u6a96', '\u1a71', '\u0a50', '\u3a33', '\u2a12', '\udbfd', '\ucbdc', '\ufbbf', '\ueb9e', '\u9b79', '\u8b58', '\ubb3b', '\uab1a', '\u6ca6', '\u7c87', '\u4ce4', '\u5cc5', '\u2c22', '\u3c03', '\u0c60', '\u1c41', '\uedae', '\ufd8f', '\ucdec', '\uddcd', '\uad2a', '\ubd0b', '\u8d68', '\u9d49', '\u7e97', '\u6eb6', '\u5ed5', '\u4ef4', '\u3e13', '\u2e32', '\u1e51', '\u0e70', '\uff9f', '\uefbe', '\udfdd', '\ucffc', '\ubf1b', '\uaf3a', '\u9f59', '\u8f78', '\u9188', '\u81a9', '\ub1ca', '\ua1eb', '\ud10c', '\uc12d', '\uf14e', '\ue16f', '\u1080', 'ยก', '\u30c2', '\u20e3', '\u5004', '\u4025', '\u7046', '\u6067', '\u83b9', '\u9398', '\ua3fb', '\ub3da', '\uc33d', '\ud31c', '\ue37f', '\uf35e', '\u02b1', '\u1290', '\u22f3', '\u32d2', '\u4235', '\u5214', '\u6277', '\u7256', '\ub5ea', '\ua5cb', '\u95a8', '\u8589', '\uf56e', '\ue54f', '\ud52c', '\uc50d', '\u34e2', '\u24c3', '\u14a0', '\u0481', '\u7466', '\u6447', '\u5424', '\u4405', '\ua7db', '\ub7fa', '\u8799', '\u97b8', '\ue75f', '\uf77e', '\uc71d', '\ud73c', '\u26d3', '\u36f2', '\u0691', '\u16b0', '\u6657', '\u7676', '\u4615', '\u5634', '\ud94c', '\uc96d', '\uf90e', '\ue92f', '\u99c8', '\u89e9', '\ub98a', '\ua9ab', '\u5844', '\u4865', '\u7806', '\u6827', '\u18c0', '\u08e1', '\u3882', '\u28a3', '\ucb7d', '\udb5c', '\ueb3f', '\ufb1e', '\u8bf9', '\u9bd8', '\uabbb', '\ubb9a', '\u4a75', '\u5a54', '\u6a37', '\u7a16', '\u0af1', '\u1ad0', '\u2ab3', '\u3a92', '\ufd2e', '\ued0f', '\udd6c', '\ucd4d', '\ubdaa', '\uad8b', '\u9de8', '\u8dc9', '\u7c26', '\u6c07', '\u5c64', '\u4c45', '\u3ca2', '\u2c83', '\u1ce0', '\u0cc1', '\uef1f', '\uff3e', '\ucf5d', '\udf7c', '\uaf9b', '\ubfba', '\u8fd9', '\u9ff8', '\u6e17', '\u7e36', '\u4e55', '\u5e74', '\u2e93', '\u3eb2', '\u0ed1', '\u1ef0' ]
    hexString = "0123456789ABCDEF"

    # ord(c)¶
    # Given a string representing one Unicode character, return an integer representing the Unicode code point of that character.
    # For example, ord('a') returns the integer 97 and ord('\u2020') returns 8224. This is the inverse of chr().


    # CRCutil.java
    # public static String getCRC(final String command) {
    #     final int crcint = caluCRC(command.getBytes());                   # turns string in ascii ints
    #     final int crclow = crcint & 0xFF;                                 # get last 8 bits(2 bytes) of command
    #     final int crchigh = crcint >> 8 & 0xFF;
    #     return new String(new byte[] { (byte)crchigh, (byte)crclow });
    # }

    #
    # private static int caluCRC(final byte[] pByte) {
    #     try {
    #         int len = pByte.length;
    i = 0
    crc = 0
    da = 0
    # int i = 0;                                                # java
    # int crc = 0;                                              # java
    # while (len-- != 0) {                                      # java
    for c in cmd:
        log.debug('Encoding %s', c)
        # int da = 0xFF & (0xFF & crc >> 8) >> 4;               # java
        t_da = ctypes.c_uint8(crc >> 8)           # CRC Orig
        da = t_da.value >> 4                        # CRC Orig
        # crc <<= 4;                                            # java
        crc <<= 4                                   # CRC Orig
        # crc ^= CRCUtil.crc_tb[0xFF & (da ^ pByte[i] >> 4)];   # java
        # index = da ^ (ord(c) >> 4)                # CRC Orig
        index = (da ^ ord(c) >> 4)
        crc ^= crc_tb[index]
        # da = (0xFF & (0xFF & crc >> 8) >> 4);                 # java
        t_da = ctypes.c_uint8(crc >> 8)           # CRC Orig
        # t_da = 0xFF & (ctypes.c_uint8(0xFF & crc >> 8))
        da = t_da.value >> 4                        # CRC Orig
        # crc <<= 4;                                            # java
        crc <<= 4                                   # CRC Orig
        # final int temp = 0xFF & (da ^ (pByte[i] & 0xF));      # java
        index = (da ^ (ord(c) & 0x0f))              # CRC Orig
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

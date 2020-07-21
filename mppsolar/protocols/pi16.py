import logging

from .protocol import AbstractProtocol
# from .pi30 import COMMANDS

log = logging.getLogger('MPP-Solar')

# (AAA BBB CCC DDD EEE
# (000 001 002 003 004

COMMANDS = {
    'QED': {
        "name": "QED",
        "description": "Query energy produced for a specific day",
        "help": " -- Query device for energy produced in the specific day at date in YYYYMMDD format",
        "type": "QUERY",
        "checksum_required": 'True',
        "response": [
                ["int", "Energy produced", "Wh"],
        ],
        "test_responses": [
            b'(012345\x9c\xaf\r',
        ],
        "regex": "QED(\\d\\d\\d\\d\\d\\d\\d\\d)$",
    },
    'QMOD': {
        "name": "QMOD",
        "description": "Operational mode query",
        "help": " -- Query device for actual operational mode",
        "type": "QUERY",
        "response": [
                ["keyed", "Device Mode", {
                    "B": "Inverter (Battery) Mode",
                    "C": "PV charging Mode",
                    "D": "Shutdown Mode",
                    "F": "Fault Mode",
                    "G": "Grid Mode",
                    "L": "Line Mode",
                    "P": "Power on Mode",
                    "S": "Standby Mode",
                    "Y": "Bypass Mode"
                }]
        ],
        "test_responses": [
            b'(B\x9c\xaf\r',
        ],
        "regex": "",
    },
    'QPIBI': {
        "name": "QPIBI",
        "description": "Battery information query",
        "help": " -- Query device for battery information",
        "type": "QUERY",
        "response": [
                ["int", "unknown", ""],
                ["int", "Number of batteries", "#"],
                ["int", "Battery total capacity", "Ah"],
                ["int", "unknown_2", ""],
                ["int", "Battery remaining time", "min"],
        ],
        "test_responses": [
            b'',
        ],
        "regex": "",
    },
    'QPIGS': {
        "name": "QPIGS",
        "description": "General status query",
        "help": " -- Query general status information",
        "type": "QUERY",
        "response": [
                ["float", "Grid voltage", "V"],
                ["int", "Output power", "W"],
                ["float", "Grid frequency", "Hz"],
                ["float", "Output current", "A"],
                ["float", "AC output voltage R", "V"],
                ["int", "AC output power R", "W"],
                ["float", "AC output frequency", "Hz"],
                ["float", "AC output current R", "A"],
                ["int", "Output load percent", "%"],
                ["float", "PBUS voltage", "V"],
                ["float", "SBUS voltage", "V"],
                ["float", "Positive battery voltage", "V"],
                ["float", "Negative battery voltage", "V"],
                ["int", "Battery capacity", "%"],
                ["int", "PV1 input power", "W"],
                ["int", "PV2 input power", "W"],
                ["int", "PV3 input power", "W"],
                ["float", "PV1 input voltage", "V"],
                ["float", "PV2 input voltage", "V"],
                ["float", "PV3 input voltage", "V"],
                ["float", "Max temperature", "°C"],
                ["string", "status TODO", ""],
        ],
        "test_responses": [
            b'(224.6 000000 49.9 0006.8 232.4 01594 49.9 006.8 029 415.0 415.0 057.9 ---.- 100 00000 00000 ----- 000.0 000.0 ---.- 035.0 D---110001k\xdb\r',
        ],
        "regex": "",
    },
    'QPI': {
        "name": "QPI",
        "description": "Device Protocol Version inquiry",
        "help": " -- queries the device protocol version",
        "type": "QUERY",
        "response": [
                ["string", "Protocol Version", ""]
        ],
        "test_responses": [
            b'(PI16\x9c\xaf\r',
        ],
        "regex": "",
    },
}


class pi16(AbstractProtocol):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b'PI16'
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = ['QPIGS', ]
        self.SETTINGS_COMMANDS = ['QPI', ]
        self.DEFAULT_COMMAND = 'QPI'

    def checksum(self, data):
        # QED20150620106

        _sum = 0
        _len = data.find('%')
        if _len == -1:
            _len = len(data)
        while _len > 0:
            _len -= 1
            _sum += ord(data[_len])
        _sum &= 0xff
        _sum = f'{_sum:03}'
        _sum = _sum.encode()
        return _sum

    def get_full_command(self, command) -> bytes:
        '''
        Override the default get_full_command as its different for PI16
        '''
        log.info(f'Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands')
        # These need to be set to allow other functions to work`
        self._command = command
        self._command_defn = self.get_command_defn(command)
        # End of required variables setting
        cmd = bytes(self._command, 'utf-8')
        if self._command_defn and 'checksum_required' in self._command_defn and self._command_defn['checksum_required'] == 'True':
            # calculate the CRC
            checksum = self.checksum(self._command)
            log.debug(f'checksum {checksum}')
            # combine byte_cmd, CRC , return
            full_command = cmd + checksum + bytes([13])
        else:
            full_command = cmd + bytes([13])
        log.debug(f'full command: {full_command}')
        return full_command

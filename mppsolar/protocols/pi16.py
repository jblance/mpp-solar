import logging

from .protocol import AbstractProtocol
# from .pi30 import COMMANDS

log = logging.getLogger('MPP-Solar')

# (AAA.A BBBBBB CC.C DDDD.D EEE.E FFFFF GG.G HHH.H III JJJ.J KKK.K LLL.L MMM.M NNN OOOOO PPPPP QQQQQ RRR.R SSS.S TTT.T UUU.U VWWWWWWWWW
# (226.1 000378 50.0 0001.7 226.8 00378 49.9 001.6 013 436.4 436.4 052.6 ---.- 077 00920 00292 ----- 196.1 ---.- ---.- 027.0 A---101001

COMMANDS = {
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

    def get_full_command(self, command, show_raw) -> bytes:
        '''
        Override the default get_full_command as its different for PI16
        '''
        log.info(f'Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands')
        # These need to be set to allow other functions to work`
        self._command = command
        self._show_raw = show_raw
        self._command_defn = self.get_command_defn(command)
        # End of required variables setting

        cmd = bytes(self._command, 'utf-8')
        full_command = cmd + bytes([13])
        log.debug(f'full command: {full_command}')
        return full_command

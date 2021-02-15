import logging

from .protocol import AbstractProtocol

# from .pi30 import COMMANDS

log = logging.getLogger("MPP-Solar")

# (AAA BBB CCC DDD EEE
# (000 001 002 003 004

COMMANDS = {
    "default": {
        "name": "default",
        "description": "VE Direct Text",
        "help": " -- the output of the VE Direct text protocol",
        "type": "KEYED",
        "response": [
            ["V", "Main or channel 1 (battery) voltage", "V", "mFloat"],
            ["V2", "Channel 2 (battery) voltage", "V", "mFloat"],
            ["V3", "Channel 3 (battery) voltage", "V", "mFloat"],
            ["VS", "Auxiliary (starter) voltage", "V", "mFloat"],
            ["VM", "Mid-point voltage of the battery bank", "V", "mFloat"],
            ["DM", "Mid-point deviation of the battery bank", "‰", "float"],
            ["VPV", "Panel voltage", "V", "mFloat"],
            ["PPV", "Panel power", "W", "float"],
            ["I", "Main or channel 1 battery current", "A", "mFloat"],
            ["I2", "Channel 2 battery current", "A", "mFloat"],
            ["I3", "Channel 3 battery current", "A", "mFloat"],
            ["IL", "Load current", "A", "mFloat"],
            ["LOAD", "Load output state (ON/OFF)", "", ""],
            ["T", "Battery temperature", "°C", "float"],
            ["P", "Instantaneous power", "W", "float"],
            ["CE", "Consumed Amp Hours", "Ah", "mFloat"],
            ["SOC", "State-of-charge", "‰ ", "float"],
            ["TTG", "Time-to-go", "Minutes", "float"],
            ["Alarm", "Alarm condition active", "", ""],
            ["Relay", "Relay state", "", ""],
            ["AR", "Alarm reason", "", ""],
            ["OR", "Off reason", "", ""],
            ["H1", "Depth of the deepest discharge", "Ah", "mFloat"],
            ["H2", "Depth of the last discharge", "Ah", "mFloat"],
            ["H3", "Depth of the average discharge", "Ah", "mFloat"],
            ["H4", "Number of charge cycles", "", ""],
            ["H5", "Number of full discharges", "", ""],
            ["H6", "Cumulative Amp Hours drawn", "Ah", "mFloat"],
            ["H7", "Minimum main (battery) voltage", "V", "mFloat"],
            ["H8", "Maximum main (battery) voltage", "V", "mFloat"],
            ["H9", "Number of seconds since last full charge", "Seconds", "float"],
            ["H10", "Number of automatic synchronizations", "", ""],
            ["H11", "Number of low main voltage alarms", "", ""],
            ["H12", "Number of high main voltage alarms", "", ""],
            ["H13", "Number of low auxiliary voltage alarms", "", ""],
            ["H14", "Number of high auxiliary voltage alarms", "", ""],
            ["H15", "Minimum auxiliary (battery) voltage", "V", "mFloat"],
            ["H16", "Maximum auxiliary (battery) voltage", "V", "mFloat"],
            ["H17", "Amount of discharged energy", "0.01 kWh", "float"],
            ["H18", "Amount of charged energy", "0.01 kWh", "float"],
            ["H19", "Yield total (user resettable counter)", "0.01 kWh", "float"],
            ["H20", "Yield today", "0.01 kWh", "float"],
            ["H21", "Maximum power today", "W", "float"],
            ["H22", "Yield yesterday", "0.01 kWh", "float"],
            ["H23", "Maximum power yesterday", "W", "float"],
            ["ERR", "Error code", "", ""],
            ["CS", "State of operation", "", ""],
            ["BMV", "Model description (deprecated)", "", ""],
            ["FW", "Firmware version (16 bit)", "", ""],
            ["FWE", "Firmware version (24 bit)", "", ""],
            ["PID", "Product ID", "", ""],
            ["SER#", "Serial number", "", ""],
            ["HSDS", "Day sequence number (0..364)", "", ""],
            ["MODE", "Device mode", "", ""],
            ["AC_OUT_V", "AC output voltage", "0.01 V", "float"],
            ["AC_OUT_I", "AC output current", "0.1 A", "float"],
            ["AC_OUT_S", "AC output apparent power", "VA", "float"],
            ["WARN", "Warning reason", "", ""],
            ["MPPT", "Tracker operation mode", "", ""],
            ["Checksum", "Checksum", "", "exclude"],
        ],
        "test_responses": [
            b"H1\t-32914\r\nH2\t0\r\nH3\t0\r\nH4\t0\r\nH5\t0\r\nH6\t-35652\r\nH7\t12041\r\nH8\t14282\r\nH9\t0\r\nH10\t0\r\nH11\t0\r\nH12\t0\r\nH15\t-22\r\nH16\t0\r\nH17\t46\r\nH18\t48\r\nChecksum\t\x1a\r\nPID\t0xA389\r\nV\t12865\r\nVS\t-14\r\nI\t0\r\nP\t0\r\nCE\t0\r\nSOC\t1000\r\nTTG\t-1\r\nAlarm\tOFF\r\nAR\t0\r\nBMV\tSmartShunt 500A/50mV\r\nFW\t0405\r\nChecksum\tL\r\n",
            b"\x00L\r\nH1\t-32914\r\nH2\t0\r\nH3\t0\r\nH4\t0\r\nH5\t0\r\nH6\t-35652\r\nH7\t12041\r\nH8\t14282\r\nH9\t0\r\nH10\t0\r\nH11\t0\r\nH12\t0\r\nH15\t-22\r\nH16\t0\r\nH17\t46\r\nH18\t48\r\nChecksum\t\x1a\r\nPID\t0xA389\r\nV\t12868\r\nVS\t-12\r\nI\t0\r\nP\t0\r\nCE\t0\r\nSOC\t1000\r\nTTG\t-1\r\nAlarm\tOFF\r\nAR\t0\r\nBMV\tSmartShunt 500A/50mV\r\nFW\t0405\r\nChecksum\tK\r",
            b"\nH1\t-32914\r\nH2\t0\r\nH3\t0\r\nH4\t0\r\nH5\t0\r\nH6\t-35652\r\nH7\t12041\r\nH8\t14282\r\nH9\t0\r\nH10\t0\r\nH11\t0\r\nH12\t0\r\nH15\t-22\r\nH16\t0\r\nH17\t46\r\nH18\t48\r\nChecksum\t\x1a\r\nPID\t0xA389\r\nV\t12868\r\nVS\t-13\r\nI\t0\r\nP\t0\r\nCE\t0\r\nSOC\t1000\r\nTTG\t-1\r\nAlarm\tOFF\r\nAR\t0\r\nBMV\tSmartShunt 500A/50mV\r\nFW\t0405\r\nChecksum\tJ\r",
        ],
        "regex": "",
    },
}


class vedirect(AbstractProtocol):
    """
    VEDirect - VEDirect protocol handler
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"VEDirect"
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = [
            "default",
        ]
        self.SETTINGS_COMMANDS = [
            "",
        ]
        self.DEFAULT_COMMAND = "default"

    def get_full_command(self, command) -> bytes:
        """
        Override the default get_full_command as its different for VEDirect
        """
        log.info(f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands")
        # These need to be set to allow other functions to work`
        self._command = command
        # self._command_defn = self.get_command_defn(command)
        # End of required variables setting
        # print("")
        cmd = bytes(self._command, "utf-8")
        # combine byte_cmd, return
        full_command = cmd  # + bytes([13])
        log.debug(f"full command: {full_command}")
        return full_command

    def get_responses(self, response):
        """
        Override the default get_responses as its different for PI00
        """
        response = response.replace(b"\n", b"")
        responses = []
        _responses = response.split(b"\r")
        for resp in _responses:
            _resp = resp.split(b"\t")
            responses.append(_resp)
        # Trim leading '(' of first response
        # 3responses[0] = responses[0][1:]
        # Remove CRC and \r of last response
        # responses[-1] = responses[-1][:-3]
        return responses

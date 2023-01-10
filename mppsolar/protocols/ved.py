import logging
from typing import Tuple

from .abstractprotocol import AbstractProtocol
from .protocol_helpers import vedHexChecksum

# from .pi30 import COMMANDS

log = logging.getLogger("ved")

# (AAA BBB CCC DDD EEE
# (000 001 002 003 004

COMMANDS = {
    "vedtext": {
        "name": "vedtext",
        "description": "VE Direct Text",
        "help": " -- the output of the VE Direct text protocol",
        "type": "VEDTEXT",
        "response_type": "KEYED",
        "response": [
            ["V", "Main or channel 1 battery voltage", "V", "float:r/1000"],
            ["V2", "Channel 2 battery voltage", "V", "float:r/1000"],
            ["V3", "Channel 3 battery voltage", "V", "float:r/1000"],
            ["VS", "Auxiliary starter voltage", "V", "float:r/1000"],
            ["VM", "Mid-point voltage of the battery bank", "V", "float:r/1000"],
            ["DM", "Mid-point deviation of the battery bank", "‰", "float"],
            ["VPV", "Panel voltage", "V", "float:r/1000"],
            ["PPV", "Panel power", "W", "float"],
            ["I", "Main or channel 1 battery current", "A", "float:r/1000"],
            ["I2", "Channel 2 battery current", "A", "float:r/1000"],
            ["I3", "Channel 3 battery current", "A", "float:r/1000"],
            ["IL", "Load current", "A", "float:r/1000"],
            ["LOAD", "Load output state ON/OFF", "", "bytes:r.decode()"],
            ["T", "Battery temperature", "°C", "float"],
            ["P", "Instantaneous power", "W", "float"],
            ["CE", "Consumed Amp Hours", "Ah", "float:r/1000"],
            ["SOC", "State-of-charge", "%", "float:r/10"],
            ["TTG", "Time-to-go", "Minutes", "float"],
            ["Alarm", "Alarm condition active", "", "bytes:r.decode()"],
            ["Relay", "Relay state", "", "bytes:r.decode()"],
            ["AR", "Alarm reason", "", "bytes:r.decode()"],
            ["OR", "Off reason", "", "bytes:r.decode()"],
            ["H1", "Depth of the deepest discharge", "Ah", "float:r/1000"],
            ["H2", "Depth of the last discharge", "Ah", "float:r/1000"],
            ["H3", "Depth of the average discharge", "Ah", "float:r/1000"],
            ["H4", "Number of charge cycles", "", "bytes:r.decode()"],
            ["H5", "Number of full discharges", "", "bytes:r.decode()"],
            ["H6", "Cumulative Amp Hours drawn", "Ah", "float:r/1000"],
            ["H7", "Minimum main battery voltage", "V", "float:r/1000"],
            ["H8", "Maximum main battery voltage", "V", "float:r/1000"],
            ["H9", "Number of seconds since last full charge", "Seconds", "float"],
            ["H10", "Number of automatic synchronizations", "", "bytes:r.decode()"],
            ["H11", "Number of low main voltage alarms", "", "bytes:r.decode()"],
            ["H12", "Number of high main voltage alarms", "", "bytes:r.decode()"],
            ["H13", "Number of low auxiliary voltage alarms", "", "bytes:r.decode()"],
            ["H14", "Number of high auxiliary voltage alarms", "", "bytes:r.decode()"],
            ["H15", "Minimum auxiliary battery voltage", "V", "float:r/1000"],
            ["H16", "Maximum auxiliary battery voltage", "V", "float:r/1000"],
            ["H17", "Amount of discharged energy", "kWh", "float:r/100"],
            ["H18", "Amount of charged energy", "kWh", "float:r/100"],
            ["H19", "Yield total - user resettable counter", "kWh", "float:r/100"],
            ["H20", "Yield today", "kWh", "float:r/100"],
            ["H21", "Maximum power today", "W", "float"],
            ["H22", "Yield yesterday", "kWh", "float:r/100"],
            ["H23", "Maximum power yesterday", "W", "float"],
            ["ERR", "Error code", "", "bytes:r.decode()"],
            ["CS", "State of operation", "", "bytes:r.decode()"],
            ["BMV", "Model description", "", "bytes:r.decode()"],
            ["FW", "Firmware version 16 bit", "", "bytes:r.decode()"],
            ["FWE", "Firmware version 24 bit", "", "bytes:r.decode()"],
            ["PID", "Product ID", "", "bytes:r.decode()"],
            ["SER#", "Serial number", "", "bytes:r.decode()"],
            ["HSDS", "Day sequence number 0..364", "", "bytes:r.decode()"],
            ["MODE", "Device mode", "", "bytes:r.decode()"],
            ["AC_OUT_V", "AC output voltage", "V", "float:r*100"],
            ["AC_OUT_I", "AC output current", "0.1 A", "float"],
            ["AC_OUT_S", "AC output apparent power", "VA", "float"],
            ["WARN", "Warning reason", "", "bytes:r.decode()"],
            ["MPPT", "Tracker operation mode", "", "bytes:r.decode()"],
            ["Checksum", "Checksum", "", "exclude"],
        ],
        "test_responses": [
            b"H1\t-32914\r\nH2\t0\r\nH3\t0\r\nH4\t0\r\nH5\t0\r\nH6\t-35652\r\nH7\t12041\r\nH8\t14282\r\nH9\t0\r\nH10\t0\r\nH11\t0\r\nH12\t0\r\nH15\t-22\r\nH16\t0\r\nH17\t46\r\nH18\t48\r\nChecksum\t\x1a\r\nPID\t0xA389\r\nV\t12865\r\nVS\t-14\r\nI\t0\r\nP\t0\r\nCE\t0\r\nSOC\t1000\r\nTTG\t-1\r\nAlarm\tOFF\r\nAR\t0\r\nBMV\tSmartShunt 500A/50mV\r\nFW\t0405\r\nChecksum\tL\r\n",
            b"\x00L\r\nH1\t-32914\r\nH2\t0\r\nH3\t0\r\nH4\t0\r\nH5\t0\r\nH6\t-35652\r\nH7\t12041\r\nH8\t14282\r\nH9\t0\r\nH10\t0\r\nH11\t0\r\nH12\t0\r\nH15\t-22\r\nH16\t0\r\nH17\t46\r\nH18\t48\r\nChecksum\t\x1a\r\nPID\t0xA389\r\nV\t12868\r\nVS\t-12\r\nI\t0\r\nP\t0\r\nCE\t0\r\nSOC\t1000\r\nTTG\t-1\r\nAlarm\tOFF\r\nAR\t0\r\nBMV\tSmartShunt 500A/50mV\r\nFW\t0405\r\nChecksum\tK\r",
            b"\nH1\t-32914\r\nH2\t0\r\nH3\t0\r\nH4\t0\r\nH5\t0\r\nH6\t-35652\r\nH7\t12041\r\nH8\t14282\r\nH9\t0\r\nH10\t0\r\nH11\t0\r\nH12\t0\r\nH15\t-22\r\nH16\t0\r\nH17\t46\r\nH18\t48\r\nChecksum\t\x1a\r\nPID\t0xA389\r\nV\t12868\r\nVS\t-13\r\nI\t0\r\nP\t0\r\nCE\t0\r\nSOC\t1000\r\nTTG\t-1\r\nAlarm\tOFF\r\nAR\t0\r\nBMV\tSmartShunt 500A/50mV\r\nFW\t0405\r\nChecksum\tJ\r",
        ],
    },
    "batteryCapacity": {
        "name": "batteryCapacity",
        "description": "battery capacity",
        "help": " -- display the battery capacity setting value",
        "type": "VEDGET",
        "command_code": "0010",  # or should be the more accurate 1000
        "response_type": "POSITIONAL",
        "response": [
            ["discard", 1, "Command type", ""],
            ["discard", 2, "Command", ""],
            [
                "keyed",
                1,
                "Command response flag",
                {
                    "00": "OK",
                    "01": "Unknown ID",
                    "02": "Not supported",
                    "04": "Parameter Error",
                },
            ],
            ["LittleHex2Short", 2, "Battery Capacity", "Ah"],
            ["discard", 1, "checksum", ""],
        ],
        "test_responses": [
            b":70010007800C6\n",
            b"\x00\x1a:70010007800C6\n",
        ],
    },
}


class ved(AbstractProtocol):
    """
    VED - VEDirect protocol handler
    """

    def __str__(self):
        return "VED protocol handler for Victron direct SmartShunts"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"VED"
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = [
            "vedtext",
        ]
        self.SETTINGS_COMMANDS = [
            "",
        ]
        self.DEFAULT_COMMAND = "vedtext"

    def get_full_command(self, command) -> bytes:
        """
        Override the default get_full_command as its different for VEDirect
        """
        log.info(
            f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands"
        )
        # These need to be set to allow other functions to work`
        self._command = command
        self._command_defn = self.get_command_defn(command)
        # End of required variables setting
        if self._command_defn is None:
            return None

        # VEDHEX
        # : start of command
        # 7 Get
        # 0000 id of the value to get
        # 00 flags
        # 00 cs
        # \n
        # eg b':70010003E\n' = get battery capacity id = 0x1000 = 0010 little endian
        cmd_type = self._command_defn["type"]
        if cmd_type == "VEDTEXT":
            # Just listen - dont need to send a command
            log.debug(f"command is VEDTEXT type so returning {cmd_type}")
            return cmd_type
        elif cmd_type == "VEDGET":
            ID = self._command_defn["command_code"]
            cmd = f"7{ID}00"
            # pad cmd and convert to bytes for checksum
            _r = f"0{cmd}"
            _r = bytes.fromhex(_r)
            checksum = vedHexChecksum(_r)
            cmd = f":{cmd}{checksum:02X}\n"
            log.debug(f"full command: {cmd}")
            return cmd
        log.warn("unable to generate full command - is the definition wrong?")
        return None

    def check_response_valid(self, response) -> Tuple[bool, dict]:
        """
        VED HEX protocol - sum of bytes should be 0x55
        VED Text protocol - no validity check
        """
        if not response:
            return False, {"validity check": ["Error: Response was empty", ""]}
        if b":" in response:
            # HEX protocol response
            log.debug(f"checking validity of {response}")
            _r = response.split(b":")[1][:-1].decode()
            # print(f"trimmed response {_r}")
            _r = f"0{_r}"
            # print(f"padded response {_r}")
            _r = bytes.fromhex(_r)
            # print(f"bytes response {_r}")
            data = _r[:-1]
            checksum = _r[-1:][0]
            if vedHexChecksum(data) == checksum:
                log.debug(
                    f"VED Hex Checksum matches in response '{response}' checksum:{checksum}"
                )
                return True, {}
            else:
                # print("VED Hex Checksum does not match")
                return False, {
                    "validity check": [
                        f"Error: VED HEX checksum did not match for response {response}",
                        "",
                    ]
                }
        else:
            return True, {}

    def get_responses(self, response):
        """
        Override the default get_responses as its different for PI00
        """
        # remove \n
        response = response.replace(b"\n", b"")
        responses = []
        # for hex protocol responses - these contain a :
        if b":" in response:
            # trim anything before ':'
            _r = response.split(b":")[1].decode()
            # pad command (which is single char)
            _r = f"0{_r}"
            _r = bytes.fromhex(_r)
            if (
                self._command_defn is not None
                and self._command_defn["response_type"] == "POSITIONAL"
            ):
                # Have a POSITIONAL type response, so need to break it up...
                for defn in self._command_defn["response"]:
                    size = defn[1]
                    item = _r[:size]
                    responses.append(item)
                    _r = _r[size:]
                return responses
            else:
                return bytearray(response)
                # convert string hex to bytes
                _r = bytes.fromhex(_r)
                return bytearray(_r)
        else:
            # for text protocol responses
            _responses = response.split(b"\r")
            for resp in _responses:
                _resp = resp.split(b"\t")
                responses.append(_resp)
        # Trim leading '(' of first response
        # 3responses[0] = responses[0][1:]
        # Remove CRC and \r of last response
        # responses[-1] = responses[-1][:-3]
        return responses

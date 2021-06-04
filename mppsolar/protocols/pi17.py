import logging

from .abstractprotocol import AbstractProtocol
from .protocol_helpers import crcPI as crc

# from .pi30 import COMMANDS

log = logging.getLogger("pi17")

COMMANDS = {
    "PI": {
        "name": "PI",
        "prefix": "^P003",
        "description": "Device Protocol Version inquiry",
        "help": " -- queries the device protocol version",
        "type": "QUERY",
        "response": [["string", "Protocol Version", ""]],
        "test_responses": [
            b"",
        ],
    },
    "ID": {
        "name": "ID",
        "prefix": "^P003",
        "description": "Device Serial Number inquiry",
        "help": " -- queries the device serial number",
        "type": "QUERY",
        "response": [["string", "Serial Number", ""]],
        "test_responses": [
            b"",
        ],
    },
    "VFW": {
        "name": "VFW",
        "prefix": "^P004",
        "description": "Device CPU version inquiry",
        "help": " -- queries the CPU version",
        "type": "QUERY",
        "response": [["float", "CPU Version", ""]],
        "test_responses": [
            b"",
        ],
    },
    "VFW2": {
        "name": "VFW2",
        "prefix": "^P005",
        "description": "Device CPU 2 version inquiry",
        "help": " -- queries the CPU 2 version",
        "type": "QUERY",
        "response": [["float", "CPU 2 Version", ""]],
        "test_responses": [
            b"",
        ],
    },
    "MD": {
        "name": "MD",
        "prefix": "^P003",
        "description": "Device Model inquiry",
        "help": " -- queries the device model",
        "type": "QUERY",
        "response": [
            [
                "keyed",
                "Machine number",
                {
                    "000": "Infini-Solar 10KW/3P",
                },
            ],
            ["int", "Output rated VA", "kW"],
            ["int", "Output power factor", "pf"],
            ["int", "AC input phase number", "number"],
            ["int", "AC output phase number", "number"],
            ["int", "Norminal AC output voltage", "0.1V"],
            ["int", "Norminal AC input voltage", "0.1V"],
            ["string", "Battery piece number", "ea"],
            ["int", "Battery standard voltage per unit", "0.1V"],
        ],
        "test_responses": [
            b"",
        ],
    },
    "PIRI": {
        "name": "PIRI",
        "prefix": "^P005",
        "description": "Device rated information",
        "help": " -- queries rated information",
        "type": "QUERY",
        "response": [
            ["int", "AC input rated voltage", "0.1V"],
            ["string", "AC input rated frequency", "Hz"],
            ["string", "AC input rated current", "0.1A"],
            ["string", "AC output rated voltage", "0.1V"],
            ["string", "AC output rated current", "0.1A"],
            ["string", "MPPT rated current per string", "0.1A"],
            ["string", "Battery rated voltage", "0.1V"],
            ["string", "MPPT track number", "ea"],
            [
                "keyed",
                "Machine type",
                {
                    "00": "Grid type",
                    "01": "Off-grid type",
                    "10": "Hybrid type",
                },
            ],
            ["option", "Topology", ["transformerless", "transformer"]],
            ["option", "Parallel for output", ["disabled", "enabled"]],
        ],
        "test_responses": [
            b"",
        ],
    },
    "GS": {
        "name": "GS",
        "prefix": "^P003",
        "description": "Device rated information",
        "help": " -- queries rated information",
        "type": "QUERY",
        "response": [
            ["int", "Solar input voltage 1", "0.1V"],
            ["int", "Solar input voltage 2", "0.1V"],
            ["int", "Solar input current 1", "0.1A"],
            ["int", "Solar input current 2", "0.1A"],
            ["int", "Battery voltage", "0.1V"],
            ["int", "Battery capacity", "%"],
            ["int", "Battery current", "0.1A"],
            ["int", "AC input voltage R", "0.1V"],
            ["int", "AC input voltage S", "0.1V"],
            ["int", "AC input voltage T", "0.1V"],
            ["int", "AC input frequency", "0.01Hz"],
            ["int", "AC input current R", "0.1A"],
            ["int", "AC input current S", "0.1A"],
            ["int", "AC input current T", "0.1A"],
            ["int", "AC output voltage R", "0.1V"],
            ["int", "AC output voltage S", "0.1V"],
            ["int", "AC output voltage T", "0.1V"],
            ["int", "AC output frequency", "0.01Hz"],
            ["int", "AC output current R", "0.1A"],
            ["int", "AC output current S", "0.1A"],
            ["int", "AC output current T", "0.1A"],
            ["int", "Inner temperature", "°C"],
            ["int", "Component max temperature", "°C"],
            ["int", "External Battery temperature", "°C"],
            [
                "option",
                "Setting change bit",
                ["No setting change", "Settings changed - please refresh"],
            ],
        ],
        "test_responses": [
            b"",
        ],
    },
    "PS": {
        "name": "PS",
        "prefix": "^P003",
        "description": "Device Power Status",
        "help": " -- queries power status",
        "type": "QUERY",
        "response": [
            ["int", "Solar input power 1", "W"],
            ["int", "Solar input power 2", "W"],
            ["int", "Battery power", "W"],
            ["int", "AC input active power R", "W"],
            ["int", "AC input active power S", "W"],
            ["int", "AC input active power T", "W"],
            ["int", "AC input total active power", "W"],
            ["int", "AC output active power R", "W"],
            ["int", "AC output active power S", "W"],
            ["int", "AC output active power T", "W"],
            ["int", "AC output total active power", "W"],
            ["int", "AC output apparent power R", "VA"],
            ["int", "AC output apparent power S", "VA"],
            ["int", "AC output apparent power T", "VA"],
            ["int", "AC output total apparent power", "VA"],
            ["int", "AC output power percentage", "%"],
            ["option", "AC output connect status", ["Disconnected", "Connected"]],
            ["option", "Solar input 1 work status", ["Idle", "Working"]],
            ["option", "Solar input 2 work status", ["Idle", "Working"]],
            ["option", "Battery power direction", ["Idle", "Charging", "Discharging"]],
            ["option", "DC/AC power direction", ["Idle", "AC to DC", "DC to AC"]],
            ["option", "Line power direction", ["Idle", "Input", "Output"]],
        ],
        "test_responses": [
            b"",
        ],
    },
    "MOD": {
        "name": "MOD",
        "prefix": "^P004",
        "description": "Device working mode inquiry",
        "help": " -- queries the device working mode",
        "type": "QUERY",
        "response": [
            [
                "keyed",
                "Working mode",
                {
                    "00": "Power on mode",
                    "01": "Standby mode",
                    "02": "Bypass mode",
                    "03": "Battery mode",
                    "04": "Fault mode",
                    "05": "Hybrid mode (Line mode, Grid mode)",
                    "06": "Charge mode",
                },
            ],
        ],
        "test_responses": [
            b"",
        ],
    },
    "WS": {
        "name": "WS",
        "description": "Warning status inquiry",
        "help": " -- queries any active warnings flags from the Inverter",
        "type": "QUERY",
        "response": [
            [
                "stat_flags",
                "Warning status",
                [
                    "Solar input 1 loss",
                    "Solar input 2 loss",
                    "Solar input 1 voltage too high",
                    "Solar input 2 voltage too high",
                    "Battery under voltage",
                    "Battery low voltage",
                    "Battery disconnected",
                    "Battery over voltage",
                    "Battery low in hybrid mode",
                    "Grid voltage high loss",
                    "Grid voltage low loss",
                    "Grid frequency high loss",
                    "Grid frequency low loss",
                    "AC input long-time average voltage over",
                    "AC input voltage loss",
                    "AC input frequency loss",
                    "AC input island",
                    "AC input phase dislocation",
                    "Over temperature",
                    "Over load",
                    "Emergency Power Off active",
                    "AC input wave loss",
                    "Reserved",
                    "Reserved",
                    "Reserved",
                    "Reserved",
                ],
            ],
        ],
        "test_responses": [
            b"",
        ],
    },
    "PE": {
        "name": "PE",
        "description": "Set the enabled state of an Inverter setting",
        "help": " -- examples: PEA - enable A (Mute buzzer beep) [A - Mute buzzer beep, B - Mute buzzer beep in standby mode, C - Mute buzzer beep only on battery discharged status, D - Generator as AC input, E - Wide AC input range, F - N/G relay function]",
        "type": "SETTER",
        "response": [["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "PE([ABCEDF])$",
    },
}


class pi17(AbstractProtocol):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI17"
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = []
        self.SETTINGS_COMMANDS = ["PI", "ID", "VFW", "VFW2", "MD", "PIRI", "GS", "PS", "MOD", "WS"]
        self.DEFAULT_COMMAND = "PI"

    def get_full_command(self, command) -> bytes:
        """
        Override the default get_full_command as its different
        """
        log.info(f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands")
        # These need to be set to allow other functions to work`
        self._command = command
        self._command_defn = self.get_command_defn(command)
        # End of required variables setting
        if self._command_defn is None:
            return None

        _cmd = bytes(self._command, "utf-8")
        _type = self._command_defn["type"]

        # No CRC in PI17 commands?
        data_length = len(_cmd) + 1
        if _type == "QUERY":
            _prefix = f"^P{data_length:03}"
        else:
            _prefix = f"^S{data_length:03}"
        _pre_cmd = bytes(_prefix, "utf-8") + _cmd
        log.debug(f"_pre_cmd: {_pre_cmd}")
        # calculate the CRC
        crc_high, crc_low = crc(_pre_cmd)
        # combine byte_cmd, CRC , return
        # PI18 full command "^P005GS\x..\x..\r"
        # _crc = bytes([crc_high, crc_low, 13])
        full_command = _pre_cmd + bytes([13])  # + _crc
        log.debug(f"full command: {full_command}")
        return full_command

    def get_responses(self, response):
        """
        Override the default get_responses as its different
        """
        responses = response.split(b",")
        if responses[0] == b"^0\x1b\xe3\r":
            # is a reject response
            return ["NAK"]
        if responses[0] == b"^1\x0b\xc2\r": 
            # is a successful acknowledgement response
            return ["ACK"]
        

        # Drop ^Dxxx from first response
        responses[0] = responses[0][5:]
        # Remove CRC of last response
        responses[-1] = responses[-1][:-3]
        return responses

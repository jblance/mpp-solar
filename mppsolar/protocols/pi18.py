import logging

from .abstractprotocol import AbstractProtocol
from .protocol_helpers import crcPI as crc

# from .pi30 import COMMANDS

log = logging.getLogger("pi18")

COMMANDS = {
    ### QUERY ###
    "ET": {
        "name": "ET",
        "prefix": "^P005",
        "description": "Total Generated Energy query",
        "help": " -- Query total generated energy",
        "type": "QUERY",
        "response": [
            ["int", "Total generated energy", "Wh"]
        ],
        "test_responses": [
            b"",
        ],
    },
    "EY": {
        "name": "EY",
        "prefix": "^P009",
        "description": "Query generated energy of year",
        "help": " -- queries generated energy for the year YYYY from the Inverter",
        "type": "QUERY",
        "response": [
            ["int", "Year generated energy", "Wh"]
        ],
        "test_responses": [
            b"",
        ],
        "regex": "EY(\\d\\d\\d\\d)$",
    },
    "ID": {
        "name": "ID",
        "prefix": "^P005",
        "description": "Device Serial Number inquiry",
        "help": " -- queries the device serial number",
        "type": "QUERY",
        "response": [["string",	"Serial Number", ""]],
        "test_responses": [
            b"^D02514012345678901234567\r",
        ],
    },
    "VFW": {
        "name": "VFW",
        "prefix": "^P006",
        "description": "Device CPU version inquiry",
        "help": " -- queries the CPU version",
        "type": "QUERY",
        "response": [
            ["int", 	"Main CPU Version", 			""],
            ["int", 	"Slave 1 CPU Version", 			""],
            ["int", 	"Slave 2 CPU Version", 			""],
        ],
        "test_responses": [
            b"^^D02005220,00000,00000\r",
        ],
    },

    "PIRI": {
        "name": "PIRI",
        "prefix": "^P007",
        "description": "Device rated information",
        "help": " -- queries rated information",
        "type": "QUERY",
        "response": [
            ["10int",	"AC input rated voltage", 		"V"],
            ["10int", 	"AC input rated current", 		"A"],
            ["10int", 	"AC output rated voltage", 		"V"],
            ["10int", 	"AC output rated frequency", 		"Hz"],
            ["10int", 	"AC output rated current", 		"A"],
            ["int", 	"AC output rating apparent power", 	"VA"],
            ["int", 	"AC output rating active power", 	"W"],
            ["10int", 	"Battery rated voltage", 		"V"],
            ["10int", 	"Battery re-charge voltage", 		"V"],
            ["10int", 	"Battery re-discharge voltage", 	"V"],
            ["10int", 	"Battery under voltage", 		"V"],
            ["10int", 	"Battery bulk voltage", 		"V"],
            ["10int", 	"Battery float voltage", 		"V"],
            ["option",	"Battery type",				[ "AGM", "Flooded", "User" ]],
            ["int", 	"Max AC charging current",		"A"],
            ["int", 	"Max charging current",			"A"],
            ["option",	"Input voltage rang",			[ "Appliance", "UPS" ]],
            ["option",	"Output source priority",		[ "Solar-Utility-Battery", "Solar-Battery-Utility" ]],
            ["option",	"Charger source priority",		[ "Solar First", "Solar and Utility", "Only Solar" ]],
            ["int", 	"Parallel max num",			""],
            ["option",	"Machine type",				[ "Off-Grid", "Grid-Tie" ]],
            ["option",	"Topology",				[ "transformerless", "transformer" ]],
            ["option",	"Output model setting",			[ "Single module", "parallel output", "Phase 1 of three phase output", "Phase 2 of three phase output", "Phase 3 of three phase output" ]],
            ["option",	"Solar power priority",			[ "Battery-Load-Utiliy + AC Charger", "Load-Battery-Utiliy" ]],
            ["int", 	"MPPT strings",				""],
        ],
        "test_responses": [
            b"^D0882300,217,2300,500,217,5000,5000,480,500,540,450,552,545,2,10,060,1,1,1,9,1,0,0,0,1,00\r",
        ],
    },
    "GS": {
        "name": "GS",
        "prefix": "^P005",
        "description": "General status query",
        "help": " -- Query general status information",
        "type": "QUERY",
        "response": [
            ["10int",	"Grid voltage",				"V"],
            ["10int",	"Grid frequency",			"Hz"],
            ["10int",	"AC output voltage",			"V"],
            ["10int",	"AC output frequency",			"Hz"],
            ["int",	"AC output apparent power",		"VA"],
            ["int",	"AC output active power",		"W"],
            ["int",	"Output load percent",			"%"],
            ["10int",	"Battery voltage",			"V"],
            ["10int",	"Battery voltage from SCC",		"V"],
            ["10int",	"Battery voltage from SCC2",		"V"],
            ["int",	"Battery discharge current",		"A"],
            ["int",	"Battery charging current",		"A"],
            ["int",	"Battery capacity",			"%"],
            ["int",	"Inverter heat sink temperature",	"°C"],
            ["int",	"MPPT1 charger temperature",		"°C"],
            ["int",	"MPPT2 charger temperature",		"°C"],
            ["int",	"PV1 Input power",			"W"],
            ["int",	"PV2 Input power",			"W"],
            ["10int",	"PV1 Input voltage",			"V"],
            ["10int",	"PV2 Input voltage",			"V"],
            ["option",	"Setting value configuration state",	[ "Nothing changed", "Something changed" ]],
            ["option",	"MPPT1 charger status",			[ "abnormal", "normal but not charged", "charging" ]],
            ["option",	"MPPT2 charger status",			[ "abnormal", "normal but not charged", "charging" ]],
            ["option",	"Load connection",			[ "disconnect", "connect" ]],
            ["option",	"Battery power direction",		[ "donothing", "charge", "discharge" ]],
            ["option",	"DC/AC power direction",		[ "donothing", "AC-DC", "DC-AC" ]],
            ["option",	"Line power direction",			[ "donothing", "input", "output" ]],
            ["int", 	"Local parallel ID",			""],
        ],
        "test_responses": [
            b"D1062232,499,2232,499,0971,0710,019,008,000,000,000,000,000,044,000,000,0520,0000,1941,0000,0,2,0,1,0,2,1,0\x09\x7b\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "MOD": {
        "name": "MOD",
        "prefix": "^P006",
        "description": "Working mode query",
        "help": " -- Query the working mode",
        "type": "QUERY",
        "response": [
            ["option",	"Working mode",				[ "Power on mode", "Standby mode", "Bypass mode", "Battery mode", "Fault mode", "Hybrid mode(Line mode, Grid mode)" ]],
        ],
        "test_responses": [
            b"",
        ],
    },

#    "FWS": {
#        "name": "FWS",
#        "prefix": "^P005",
#        "description": "fault and warning status",
#        "help": " -- Query fault and warning status",
#        "type": "QUERY",
#        "response": [
#            [
#            ]
#        ],
#        "test_responses": [
#            b"",
#        ],
#    },

    "FLAG": {
        "name": "FLAG",
        "prefix": "^P007",
        "description": "Query enable/disable flag status",
        "help": " -- queries enable/disable flag status from the Inverter",
        "type": "QUERY",
        "response": [
            ["option",	"Buzzer beep",				[ "Disabled", "Enabled" ]],
            ["option",	"Overload bypass function",		[ "Disabled", "Enabled" ]],
            ["option",	"display back to default page",		[ "Disabled", "Enabled" ]],
            ["option",	"Overload restart",			[ "Disabled", "Enabled" ]],
            ["option",	"Over temperature restart",		[ "Disabled", "Enabled" ]],
            ["option",	"Backlight on",				[ "Disabled", "Enabled" ]],
            ["option",	"Alarm primary source interrupt",	[ "Disabled", "Enabled" ]],
            ["option",	"Fault code record",			[ "Disabled", "Enabled" ]],
            ["int",	"Reserved",				""],
        ],
        "test_responses": [
            b"",
        ],
    },

#    "DI": {
#        "name": "DI",
#        "prefix": "^P005",
#        "description": "Query default value of changeable paramer",
#        "help": " -- Query default value of changeable paramer",
#        "type": "QUERY",
#        "response": [
#        ],
#        "test_responses": [
#            b"",
#        ],
#    },

    "MCHGCR": {
        "name": "MCHGCR",
        "prefix": "^P009",
        "description": "Query Max. charging current selectable value",
        "help": " -- Query Max. charging current selectable value",
        "type": "QUERY",
        "response": [
            ["int", 	"Max. charging current value 1", 	"A"],
            ["int", 	"Max. charging current value 2", 	"A"],
            ["int", 	"Max. charging current value 3",	"A"],
            ["int", 	"Max. charging current value 4",	"A"],
            ["int", 	"Max. charging current value 5",	"A"],
            ["int", 	"Max. charging current value 6",	"A"],
            ["int", 	"Max. charging current value 7",	"A"],
            ["int", 	"Max. charging current value 8",	"A"],
        ],
        "test_responses": [
            b"^D034010,020,030,040,050,060,070,080\x161\r",
        ],
    },
    "MUCHGCR": {
        "name": "MUCHGCR",
        "prefix": "^P010",
        "description": "Query Max. AC charging current selectable value",
        "help": " -- Query Max. AC charging current selectable value",
        "type": "QUERY",
        "response": [
            ["int",	"Max. AC charging current value 1",	"A"],
            ["int",	"Max. AC charging current value 2",	"A"],
            ["int",	"Max. AC charging current value 3",	"A"],
            ["int",	"Max. AC charging current value 4",	"A"],
            ["int",	"Max. AC charging current value 5",	"A"],
            ["int",	"Max. AC charging current value 6",	"A"],
            ["int",	"Max. AC charging current value 7",	"A"],
            ["int",	"Max. AC charging current value 8",	"A"],
            ["int",	"Max. AC charging current value 9",	"A"],
        ],
        "test_responses": [
            b"",
        ],
    },
    "PI": {
        "name": "PI",
        "prefix": "^P005",
        "description": "Device Protocol Version inquiry",
        "help": " -- queries the device protocol version",
        "type": "QUERY",
        "response":[
            ["string",	"Protocol Version",			""]
        ],
        "test_responses": [
            b"",
        ],
    },

    ### SETTER ###
#    "LON": {
#        "name": "LON",
#        "prefix": "^S007",
#        "description": "Set enable/disable machine supply power to the loads",
#        "help": " -- examples: LON1 (0: disable, 1: enable)",
#        "type": "SETTER",
#        "response": [
#            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
#        ],
#        "test_responses": [
#            b"^1\x0b\xc2\r",
#            b"^0\x1b\xe3\r",
#        ],
#        "regex": "LON([01])$",
#    },

    "POP": {
        "name": "POP",
        "prefix": "^S007",
        "description": "Set output souce priority",
        "help": " -- examples: POP (0: Solar-Utility-Battery, 1: Solar-Battery-Utility)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "POP([01])$",
    },

    "PEI": {
        "name": "PEI",
        "prefix": "^S006",
        "description": "Machine type, enable: Grid-Tie (Maunal Option 9)",
        "help": " -- examples: PEI (enable Grid-Tie)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },

    "PDI": {
        "name": "PDI",
        "prefix": "^S006",
        "description": "Machine type, disable: Grid-Tie do Off-Grid Tie (Maunal Option 9)",
        "help": " -- examples: PDI (disable Grid-Tie)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },


# Not working "Command PCP01 was rejected"
#    "PCP": {
#        "name": "PCP",
#        "prefix": "^S009",
#        "description": "Set charging source priority",
#        "help": " -- examples: PCP01 (Parallel machine ID (0-9) + 0: Solar first, 1: Solar and Utility, 2: Only solar)",
#        "type": "SETTER",
#        "response": [
#            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
#        ],
#        "test_responses": [
#            b"^1\x0b\xc2\r",
#            b"^0\x1b\xe3\r",
#        ],
#        "regex": "PCP([0-9][012])$",
#    },

    "PSP": {
        "name": "PSP",
        "prefix": "^S007",
        "description": "Set solar power priority",
        "help": " -- examples: PSP0 (0: Battery-Load-Utiliy (+AC Charge), 1: Load-Battery-Utiliy)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "PSP([01])$",
    },

    "MCHGV": {
        "name": "MCHGV",
        "prefix": "^S015",
        "description": "Set battery charge voltages",
        "help": " -- examples: MCHGV552,540 (CV voltage in 0.1V xxx, Float voltage xxx in 0.1V)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
#        "regex": "MCHGV([4-5]\\d\\d,[4-5]\\d\\d)$",
        # Regex 480 - 584 Volt 
        "regex": "MCHGV(4[8-9][0-9]|5[0-7][0-9]|58[0-5]),(4[8-9][0-9]|5[0-7][0-9]|58[0-4])$",
    },

}


class pi18(AbstractProtocol):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI18"
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = [
            "ET",
            "EY",
            "ID",
            "VFW",
            "PIRI",
            "GS",
            "MOD",
            #"FWS",
            "FLAG",
            #"DI",
            "MCHGCR",
            "MUCHGCR",
            "PI",
        ]
        self.SETTINGS_COMMANDS = [
            "PEI"
            "PDI"
            "POP"
            #"PCP",
            "PSP",
            "MCHGV",
        ]
        self.DEFAULT_COMMAND = "PI"

    def get_full_command(self, command) -> bytes:
        """
        Override the default get_full_command as its different for PI18
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

        #data_length = len(_cmd) + 2 + 1
        if _type == "QUERY":
              _prefix = self._command_defn["prefix"]
        elif _type== "SETTER":
              _prefix = self._command_defn["prefix"]
              #data_length = len(_cmd) + 2 + 1
              #_prefix = f"^S{data_length:03}"

        else:
            _prefix = f"^P{data_length:03}"

        _pre_cmd = bytes(_prefix, "utf-8") + _cmd

        log.debug(f"_pre_cmd: {_pre_cmd}")
        # calculate the CRC
        crc_high, crc_low = crc(_pre_cmd)
        # combine byte_cmd, CRC , return
        # PI18 full command "^P005GS\x..\x..\r"
        _crc = bytes([crc_high, crc_low, 13])
        full_command = _pre_cmd + _crc

        log.debug(f"full command: {full_command}")
        return full_command

    def get_responses(self, response):
        """
        Override the default get_responses as its different for PI18
        """
        responses = response.split(b",")
        if responses[0] == b"^0\x1b\xe3\r":
            # is a reject response
            return ["NAK"]

        # Drop ^Dxxx from first response
        responses[0] = responses[0][5:]
        # Remove CRC of last response
        responses[-1] = responses[-1][:-3]
        return responses

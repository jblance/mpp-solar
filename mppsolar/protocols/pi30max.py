import logging

from .abstractprotocol import AbstractProtocol
from .protocol_helpers import crcPI as crc

log = logging.getLogger("pi30max")

QUERY_COMMANDS = {
    "QPI": {
        "name": "QPI",
        "description": "Protocol ID inquiry",
        "help": " -- queries the device protocol ID. e.g. PI30 for HS series",
        "type": "QUERY",
        "response": [
            ["string", "Protocol ID", ""],
        ],
        "test_responses": [
            b"(PI30\x9a\x0b\r",
        ],
    },
    "QID": {
        "name": "QID",
        "description": "Device Serial Number inquiry",
        "help": " -- queries the device serial number",
        "type": "QUERY",
        "response": [["string", "Serial Number", ""]],
        "test_responses": [
            b"(9293333010501\xBB\x07\r",
        ],
    },
    "QSID": {
        "name": "QSID",
        "description": "Device Serial Number inquiry",
        "help": " -- queries the device serial number (length greater than 14)",
        "type": "QUERY",
        "response": [["string", "Serial Number", ""]],
        "test_responses": [
        ],
    },	
    "QVFW": {
        "name": "QVFW",
        "description": "Main CPU firmware version inquiry",
        "help": " -- queries the main CPU firmware version",
        "type": "QUERY",
        "response": [["string", "Main CPU firmware version", ""]],
        "test_responses": [
            b"(VERFW:00072.70\x53\xA7\r",
        ],
    },
    "QVFW3": {
        "name": "QVFW3",
        "description": "Remote CPU firmware version inquiry",
        "help": " -- queries the CPU firmware version of the remote panel",
        "type": "QUERY",
        "response": [["string", "Remote CPU firmware version", ""]],
        "test_responses": [
        ],
    },	
    "VERFW": {
        "name": "VERFW",
        "description": "Bluetooth version inquiry",
        "help": " -- queries the bluetooth version",
        "type": "QUERY",
        "response": [["string", "Bluetooth version", ""]],
        "test_responses": [
        ],
    },	
    "QPIRI": {
        "name": "QPIRI",
        "description": "Current Settings inquiry",
        "help": " -- queries the current settings from the Inverter",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "response": [
            ["float", "AC Input Voltage", "V"],
            ["float", "AC Input Current", "A"],
            ["float", "AC Output Voltage", "V"],
            ["float", "AC Output Frequency", "Hz"],
            ["float", "AC Output Current", "A"],
            ["int", "AC Output Apparent Power", "VA"],
            ["int", "AC Output Active Power", "W"],
            ["float", "Battery Voltage", "V"],
            ["float", "Battery Recharge Voltage", "V"],
            ["float", "Battery Under Voltage", "V"],
            ["float", "Battery Bulk Charge Voltage", "V"],
            ["float", "Battery Float Charge Voltage", "V"],
            [
                "option",
                "Battery Type",
                [
                    "AGM",
                    "Flooded",
                    "User",
                    "TBD",
                    "Pylontech",
                    "WECO",
                    "Soltaro",
                    "LIb-protocol compatible",
                    "3rd party Lithium",
                ],
            ],
            ["int", "Max AC Charging Current", "A"],
            ["int", "Max Charging Current", "A"],
            ["option", "Input Voltage Range", ["Appliance", "UPS"]],
            [
                "option",
                "Output Source Priority",
                ["Utility Solar Battery", "Solar Utility Battery", "Solar Battery Utility"],
            ],
            [
                "option",
                "Charger Source Priority",
                [
                    "Utility first",
                    "Solar first",
                    "Solar + Utility",
                    "Only solar charging permitted",
                ],
            ],
            ["int", "Max Parallel Units", "units"],
            [
                "str_keyed",
                "Machine Type",
                {"00": "Grid tie", "01": "Off Grid", "10": "Hybrid"},
            ],
            ["option", "Topology", ["transformerless", "transformer"]],
            [
                "option",
                "Output Mode",
                [
                    "single machine output",
                    "parallel output",
                    "Phase 1 of 3 Phase output",
                    "Phase 2 of 3 Phase output",
                    "Phase 3 of 3 Phase output",
                    "Phase 1 of 2 phase output",
                    "Phase 2 of 2 phase output (120°)",
					"Phase 2 of 2 phase output (180°)",
                    "unknown output",
                ],
            ],
            ["float", "Battery Redischarge Voltage", "V"],
            [
                "option",
                "PV OK Condition",
                [
                    "As long as one unit of inverters has connect PV, parallel system will consider PV OK",
                    "Only All of inverters have connect PV, parallel system will consider PV OK",
                ],
            ],
            [
                "option",
                "PV Power Balance",
                [
                    "PV input max current will be the max charged current",
                    "PV input max power will be the sum of the max charged power and loads power",
                ],
            ],
			["int", "Max charging time for CV stage","min"],
			["option", "Operation Logic", ["Automatic mode", "On-line mode", "ECO mode"]],
			["int", "Max discharging current","A"],
        ],
        "test_responses": [
        ],
    },
    "QFLAG": {
        "name": "QFLAG",
        "description": "Flag Status inquiry",
        "help": " -- queries the enabled / disabled state of various Inverter settings (e.g. buzzer, overload, interrupt alarm)",
        "type": "QUERY",
        "response": [
            [
                "enflags",
                "Device Status",
                {
                    "a": {"name": "Buzzer", "state": "disabled"},
                    "b": {"name": "Overload Bypass", "state": "disabled"},
                    "d": {"name": "Solar Feed to Grid", "state": "disabled"},
                    "k": {"name": "LCD Reset to Default", "state": "disabled"},
                    "u": {"name": "Overload Restart", "state": "disabled"},
                    "v": {"name": "Over Temperature Restart", "state": "disabled"},
                    "x": {"name": "LCD Backlight", "state": "disabled"},
                    "y": {
                        "name": "Primary Source Interrupt Alarm",
                        "state": "disabled",
                    },
                    "z": {"name": "Record Fault Code", "state": "disabled"},
                },
            ]
        ],
        "test_responses": [
        ],	
	},
    "QPIGS": {
        "name": "QPIGS",
        "description": "General Status Parameters inquiry",
        "help": " -- queries the value of various metrics from the Inverter",
        "type": "QUERY",
        "response": [
            ["float", "AC Input Voltage", "V"],
            ["float", "AC Input Frequency", "Hz"],
            ["float", "AC Output Voltage", "V"],
            ["float", "AC Output Frequency", "Hz"],
            ["int", "AC Output Apparent Power", "VA"],
            ["int", "AC Output Active Power", "W"],
            ["int", "AC Output Load", "%"],
            ["int", "BUS Voltage", "V"],
            ["float", "Battery Voltage", "V"],
            ["int", "Battery Charging Current", "A"],
            ["int", "Battery Capacity", "%"],
            ["int", "Inverter Heat Sink Temperature", "°C"],
            ["float", "PV1 Input Current", "A"],
            ["float", "PV1 Input Voltage", "V"],
            ["float", "Battery Voltage from SCC", "V"],
            ["int", "Battery Discharge Current", "A"],
            [
                "flags",
                "Device Status",
                [
                    "Is SBU Priority Version Added",
                    "Is Configuration Changed",
                    "Is SCC Firmware Updated",
                    "Is Load On",
                    "Is Battery Voltage to Steady While Charging",
                    "Is Charging On",
                    "Is SCC Charging On",
                    "Is AC Charging On",
                ],
            ],
            ["int", "Battery Voltage Offset for Fans On", "10mV"],
            ["int", "EEPROM Version", ""],
            ["int", "PV1 Charging Power", "W"],
            [
                "flags",
                "Device Status2",
                ["Is Charging to Float", "Is Switched On", "Is Dustproof Installed"],
            ],
			["option", "Solar Feed to Grid", ["Disabled", "Enabled"]],
			[
                "keyed",
                "Country",
                {
                    "00": "India",
                    "01": "Germany",
                    "02": "South America",
				}
			],
			["int", "Solar Feed to Grid Power", "W"],
        ],
        "test_responses": [
        ],
    },
	"QPIGS2": {
        "name": "QPIGS2",
        "description": "General Status Parameters inquiry 2",
        "help": " -- queries the value of various metrics from the Inverter 2",
        "type": "QUERY",
        "response": [
            ["float", "PV2 Input Current", "A"],
			["float", "PV2 Input Voltage", "V"],
			["int", "PV2 Charging Power", "W"],
		],
		"test_responses": [
        ],
	},
	"QPGS": {
        "name": "QPGS",
        "description": "Parallel Information inquiry",
        "help": " -- example: QPGS1 queries the values of various metrics from instance 1 of parallel setup Inverters (numbers from 0)",
        "type": "QUERY",
        "response": [
            ["option", "Parallel instance number", ["Not valid", "valid"]],
            ["string", "Serial number", ""],
            [
                "keyed",
                "Work mode",
                {
                    "P": "Power On Mode",
                    "S": "Standby Mode",
                    "L": "Line Mode",
                    "B": "Battery Mode",
                    "F": "Fault Mode",
                    "H": "Power Saving Mode",
					"D": "Shutdown Mode",
                },
            ],
            [
                "keyed",
                "Fault code",
                {
                    "00": "No fault",
                    "01": "Fan is locked",
                    "02": "Over temperature",
                    "03": "Battery voltage is too high",
                    "04": "Battery voltage is too low",
                    "05": "Output short circuited or Over temperature",
                    "06": "Output voltage is too high",
                    "07": "Over load time out",
                    "08": "Bus voltage is too high",
                    "09": "Bus soft start failed",
					"10": "PV over current",
                    "11": "PV over voltage",
					"12": "DC over current",
					"13": "Battery discharge over current",
                    "51": "Over current inverter",
                    "52": "Bus voltage too low",
                    "53": "Inverter soft start failed",
                    "54": "Self-test failed",
                    "55": "Over DC voltage on output of inverter",
                    "56": "Battery connection is open",
                    "57": "Current sensor failed",
                    "58": "Output voltage is too low",
                    "60": "Power feedback protection",
                    "71": "Firmware version different",
                    "72": "Current sharing fault",
                    "80": "CAN communication failed",
                    "81": "Parallel host line lost",
                    "82": "Parallel synchronized signal lost",
                    "83": "Parallel battery voltage detect different",
                    "84": "AC input voltage or frequency detected different",
                    "85": "AC output current unbalanced",
                    "86": "AC output mode setting different",
                },
            ],
            ["float", "Grid voltage", "V"],
            ["float", "Grid frequency", "Hz"],
            ["float", "AC output voltage", "V"],
            ["float", "AC output frequency", "Hz"],
            ["int", "AC output apparent power", "VA"],
            ["int", "AC output active power", "W"],
            ["int", "Load percentage", "%"],
            ["float", "Battery voltage", "V"],
            ["int", "Battery charging current", "A"],
            ["int", "Battery capacity", "%"],
            ["float", "PV1 Input Voltage", "V"],
            ["int", "Total charging current", "A"],
            ["int", "Total AC output apparent power", "VA"],
            ["int", "Total output active power", "W"],
            ["int", "Total AC output percentage", "%"],
            [
                "flags",
                "Inverter Status",
                [
                    "Is SCC OK",
                    "Is AC Charging",
                    "Is SCC Charging",
                    "Is Battery Over Voltage",
                    "Is Battery Under Voltage",
                    "Is Line Lost",
                    "Is Load On",
                    "Is Configuration Changed",
                ],
            ],
            [
                "option",
                "Output mode",
                [
                    "single machine",
                    "parallel output",
                    "Phase 1 of 3 phase output",
                    "Phase 2 of 3 phase output",
                    "Phase 3 of 3 phase output",
                    "Phase 1 of 2 phase output",
                    "Phase 2 of 2 phase output",
                    "Unknown Output Mode",
                ],
            ],
            [
                "option",
                "Charger source priority",
                ["Utility first", "Solar first", "Solar + Utility", "Solar only"],
            ],
            ["int", "Max charger current", "A"],
            ["int", "Max charger range", "A"],
            ["int", "Max AC charger current", "A"],
            ["int", "PV input current", "A"],
            ["int", "Battery discharge current", "A"],
            ["float", "Unknown float", ""],
            ["string", "Unknown flags?", ""],
        ],
        "test_responses": [
        ],
        "regex": "QPGS(\\d+)$",
    },
}

SETTER_COMMANDS = {
}

class pi30max(AbstractProtocol):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI30MAX"
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = ["QPIGS", "QPIGS2"]
        self.SETTINGS_COMMANDS = ["QPIRI", "QFLAG"]
        self.DEFAULT_COMMAND = "QPI"
        # log.info(f'Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands')

    def check_response_valid(self, response):
        if response is None:
            return False, {"ERROR": ["No response", ""]}
        if len(response) <= 3:
            return False, {"ERROR": ["Response to short", ""]}

        if type(response) is str:
            if "(NAK" in response:
                return False, {"ERROR": ["NAK", ""]}
            crc_high, crc_low = crc(response[:-3])
            if [ord(response[-3]), ord(response[-2])] != [crc_high, crc_low]:
                return False, {"ERROR": ["Invalid response CRCs", ""]}
        elif type(response) is bytes:
            if b"(NAK" in response:
                return False, {"ERROR": ["NAK", ""]}

            crc_high, crc_low = crc(response[:-3])
            if response[-3:-1] != bytes([crc_high, crc_low]):
                return False, {"ERROR": ["Invalid response CRC", ""]}
        log.debug("CRCs match")
        return True, {}

import logging

from .pi30max import pi30max

log = logging.getLogger("pi30m045")

QUERY_COMMANDS = {
    "QPIRI": {
        "name": "QPIRI",
        "description": "Current Settings inquiry",
        "type": "QUERY",
        "response_type": "INDEXED",
        "response": [
            [
                1,
                "AC Input Voltage",
                "float",
                "V",
                {"icon": "mdi:transmission-tower-import", "device-class": "voltage"},
            ],
            [2, "AC Input Current", "float", "A", {"icon": "mdi:current-ac", "device-class": "current"}],
            [
                3,
                "AC Output Voltage",
                "float",
                "V",
                {"icon": "mdi:transmission-tower-export", "device-class": "voltage"},
            ],
            [4, "AC Output Frequency", "float", "Hz", {"icon": "mdi:current-ac", "device-class": "frequency"}],
            [5, "AC Output Current", "float", "A", {"icon": "mdi:current-ac", "device-class": "current"}],
            [6, "AC Output Apparent Power", "int", "VA", {"icon": "mdi:power-plug", "device-class": "apparent_power"}],
            [
                7,
                "AC Output Active Power",
                "int",
                "W",
                {"icon": "mdi:power-plug", "device-class": "power", "state_class": "measurement"},
            ],
            [8, "Battery Voltage", "float", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            [9, "Battery Recharge Voltage", "float", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            [10, "Battery Under Voltage", "float", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            [
                11,
                "Battery Bulk Charge Voltage",
                "float",
                "V",
                {"icon": "mdi:battery-outline", "device-class": "voltage"},
            ],
            [
                12,
                "Battery Float Charge Voltage",
                "float",
                "V",
                {"icon": "mdi:battery-outline", "device-class": "voltage"},
            ],
            [
                13,
                "Battery Type",
                "option",
                [
                    "AGM",
                    "Flooded",
                    "User",
                    "Pylontech",
                    "Shinheung",
                    "WECO",
                    "Soltaro",
                    "LIb-protocol compatible",
                    "3rd party Lithium",
                ],
            ],
            [14, "Max AC Charging Current", "int", "A", {"icon": "mdi:current-ac", "device-class": "current"}],
            [15, "Max Charging Current", "int", "A", {"icon": "mdi:current-ac", "device-class": "current"}],
            [16, "Input Voltage Range", "option", ["Appliance", "UPS"]],
            [
                17,
                "Output Source Priority",
                "option",
                [
                    "Utility Solar Battery",
                    "Solar Utility Battery",
                    "Solar Battery Utility",
                ],
            ],
            [
                18,
                "Charger Source Priority",
                "option",
                [
                    "Solar first",
                    "Solar + Utility",
                    "Only solar charging permitted",
                ],
            ],
            [19, "Max Parallel Units", "int", "units"],
            [
                20,
                "Machine Type",
                "str_keyed",
                {"00": "Grid tie", "01": "Off Grid", "10": "Hybrid"},
            ],
            [21, "Topology", "option", ["transformerless", "transformer"]],
            [
                22,
                "Output Mode",
                "option",
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
            [23, "Battery Redischarge Voltage", "float", "V"],
            [
                24,
                "PV OK Condition",
                "option",
                [
                    "As long as one unit of inverters has connect PV, parallel system will consider PV OK",
                    "Only All of inverters have connect PV, parallel system will consider PV OK",
                ],
            ],
            [
                25,
                "PV Power Balance",
                "option",
                [
                    "PV input max current will be the max charged current",
                    "PV input max power will be the sum of the max charged power and loads power",
                ],
            ],
            [26, "Max charging time for CV stage", "int", "min"],
            [
                27,
                "Operation Logic",
                "option",
                ["Automatic mode", "On-line mode", "ECO mode"],
            ],
            [28, "Max discharging current", "int", "A", {"icon": "mdi:current-ac", "device-class": "current"}],
        ],
        "test_responses": [
            b"(230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10 010 1 0 0 6 01 0 0 54.0 0 1\x6F\x7E\r",
        ],
    },
    "QDI": {
        "name": "QDI",
        "description": "Default Settings inquiry",
        "type": "QUERY",
        "response": [
            ["float", "AC Output Voltage", "V"],
            ["float", "AC Output Frequency", "Hz"],
            ["int", "Max AC Charging Current", "A"],
            ["float", "Battery Under Voltage", "V"],
            ["float", "Battery Float Charge Voltage", "V"],
            ["float", "Battery Bulk Charge Voltage", "V"],
            ["float", "Battery Recharge Voltage", "V"],
            ["int", "Max Charging Current", "A"],
            ["option", "Input Voltage Range", ["Appliance", "UPS"]],
            [
                "option",
                "Output Source Priority",
                ["Utility first", "Solar first", "SBU first"],
            ],
            [
                "option",
                "Charger Source Priority",
                [
                    "Solar first",
                    "Solar + Utility",
                    "Only solar charging permitted",
                ],
            ],
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
            ["option", "Buzzer", ["enabled", "disabled"]],
            ["option", "Power saving", ["disabled", "enabled"]],
            ["option", "Overload restart", ["disabled", "enabled"]],
            ["option", "Over temperature restart", ["disabled", "enabled"]],
            ["option", "LCD Backlight", ["disabled", "enabled"]],
            ["option", "Primary source interrupt alarm", ["disabled", "enabled"]],
            ["option", "Record fault code", ["disabled", "enabled"]],
            ["option", "Overload bypass", ["disabled", "enabled"]],
            ["option", "LCD reset to default", ["disabled", "enabled"]],
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
                    "Phase 2 of 2 phase output (120°)",
                    "Phase 2 of 2 phase output (180°)",
                    "Unknown Output Mode",
                ],
            ],
            ["float", "Battery Redischarge Voltage", "V"],
            [
                "option",
                "PV OK condition",
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
            ["int", "Max Charging Time at CV", "min"],
            ["int", "Max Discharging current", "A"],
        ],
        "test_responses": [
            b"(230.0 50.0 0030 44.0 54.0 56.4 46.0 60 0 0 2 0 0 0 0 0 1 1 1 0 1 0 54.0 0 1 224\xeb\xbc\r",
        ],
    },
    "QPGS": {
        "name": "QPGS",
        "description": "Parallel Information inquiry",
        "help": " -- example: QPGS0 queries the values of various metrics from instance 0 of parallel setup Inverters",
        "type": "QUERY",
        "response_type": "INDEXED",
        "response": [
            [1, "Parallel instance number", "option", ["Not valid", "valid"]],
            [2, "Serial number", "bytes:r.decode()", "", {"icon": "mdi:identifier"}],
            [
                3,
                "Work mode",
                "str_keyed",
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
                4,
                "Fault code",
                "str_keyed",
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
            [5, "Grid Voltage", "float", "V", {"icon": "mdi:power-plug", "device-class": "voltage"}],
            [6, "Grid Frequency", "float", "Hz", {"icon": "mdi:current-ac", "device-class": "frequency"}],
            [7, "AC Output Voltage", "float", "V", {"icon": "mdi:power-plug", "device-class": "voltage"}],
            [8, "AC Output Frequency", "float", "Hz", {"icon": "mdi:current-ac", "device-class": "frequency"}],
            [9, "AC Output Apparent Power", "int", "VA", {"icon": "mdi:power-plug", "device-class": "apparent_power"}],
            [
                10,
                "AC Output Active Power",
                "int",
                "W",
                {"icon": "mdi:power-plug", "device-class": "power", "state_class": "measurement"},
            ],
            [11, "Load Percentage", "int", "%", {"icon": "mdi:brightness-percent"}],
            [12, "Battery Voltage", "float", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            [13, "Battery Charging Current", "int", "A", {"icon": "mdi:current-dc", "device-class": "current"}],
            [14, "Battery Capacity", "int", "%", {"device-class": "battery"}],
            [15, "PV1 Input Voltage", "float", "V", {"icon": "mdi:solar-power", "device-class": "voltage"}],
            [
                16,
                "Total Charging Current",
                "int",
                "A",
                {"icon": "mdi:brightness-percent", "device-class": "current"},
            ],
            [
                17,
                "Total AC Output Apparent Power",
                "int",
                "VA",
                {"icon": "mdi:power-plug", "device-class": "apparent_power"},
            ],
            [
                18,
                "Total Output Active Power",
                "int",
                "W",
                {"icon": "mdi:power-plug", "device-class": "power", "state_class": "measurement"},
            ],
            [
                19,
                "Total AC Output Percentage",
                "int",
                "%",
                {"icon": "mdi:brightness-percent"},
            ],
            [
                20,
                "Inverter Status",
                "flags",
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
                21,
                "Output mode",
                "option",
                [
                    "single machine",
                    "parallel output",
                    "Phase 1 of 3 phase output",
                    "Phase 2 of 3 phase output",
                    "Phase 3 of 3 phase output",
                    "Phase 1 of 2 phase output",
                    "Phase 2 of 2 phase output (120°)",
                    "Phase 2 of 2 phase output (180°)",
                    "Unknown Output Mode",
                ],
            ],
            [
                22,
                "Charger source priority",
                "option",
                ["Solar first", "Solar + Utility", "Solar only"],
            ],
            [23, "Max Charger Current", "int", "A", {"device-class": "current"}],
            [24, "Max Charger Range", "int", "A", {"device-class": "current"}],
            [25, "Max AC Charger Current", "int", "A", {"device-class": "current"}],
            [26, "PV1 Input Current", "int", "A", {"icon": "mdi:solar-power", "device-class": "power"}],
            [
                27,
                "Battery Discharge Current",
                "int",
                "A",
                {"icon": "mdi:battery-negative", "device-class": "current"},
            ],
            [28, "PV2 Input Voltage", "float", "V", {"icon": "mdi:solar-power", "device-class": "voltage"}],
            [29, "PV2 Input Current", "int", "A", {"icon": "mdi:solar-power", "device-class": "current"}],
        ],
        "test_responses": [
            b"(0 92932105105315 B 00 000.0 00.00 230.0 50.00 0989 0907 012 53.2 009 090 349.8 009 00989 00907 011 10100110 0 1 100 120 030 02 000 275.3 02i]\r",
        ],
        "regex": "QPGS(\\d+)$",
    },
}
SETTER_COMMANDS = {
    "DAT": {
        "name": "DAT",
        "description": "Set Date Time",
        "help": " -- examples: DATYYMMDDHHMMSS (12 digits after DAT)",
        "type": "SETTER",
        "response": [["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "DAT(\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d)$",
    },
    "PCP": {
        "name": "PCP",
        "description": "Set Device Charger Priority",
        "help": " -- examples: PCP00 (set solar first), PCP01 (set solar and utility), PCP02 (set solar only charging)",
        "type": "SETTER",
        "response": [["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PCP(0[0123])$",
    },
    "PPCP": {
        "name": "PPCP",
        "description": "Set Parallel Device Charger Priority",
        "help": " -- examples: PPCP000 (set unit 1 to 00 - solar first), PPCP101 (set unit 1 to 01 - solar and utility), PPCP202 (set unit 2 to 02 - solar only charging)",
        "type": "SETTER",
        "response": [["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PPCP(\\d0[0123])$",
    },
}

class pi30m045(pi30max):
    def __str__(self):
        return "PI30 protocol handler for LV6548 and similar inverters"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI30M045"
        # Add pi30m045 specific commands to pi30max commands
        self.COMMANDS.update(QUERY_COMMANDS)
        # Add pi30m045 specific setter commands
        self.COMMANDS.update(SETTER_COMMANDS)
        log.info(f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands")
import logging

from .pi30max import pi30max

log = logging.getLogger("pi30m045")

QUERY_COMMANDS = {
    "QPIRI": {
        "name": "QPIRI",
        "description": "Current Settings inquiry",
        "type": "QUERY",
        "response_type": "INDEXED",
        "response": [
            [
                1,
                "AC Input Voltage",
                "float",
                "V",
                {"icon": "mdi:transmission-tower-import", "device-class": "voltage"},
            ],
            [2, "AC Input Current", "float", "A", {"icon": "mdi:current-ac", "device-class": "current"}],
            [
                3,
                "AC Output Voltage",
                "float",
                "V",
                {"icon": "mdi:transmission-tower-export", "device-class": "voltage"},
            ],
            [4, "AC Output Frequency", "float", "Hz", {"icon": "mdi:current-ac", "device-class": "frequency"}],
            [5, "AC Output Current", "float", "A", {"icon": "mdi:current-ac", "device-class": "current"}],
            [6, "AC Output Apparent Power", "int", "VA", {"icon": "mdi:power-plug", "device-class": "apparent_power"}],
            [
                7,
                "AC Output Active Power",
                "int",
                "W",
                {"icon": "mdi:power-plug", "device-class": "power", "state_class": "measurement"},
            ],
            [8, "Battery Voltage", "float", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            [9, "Battery Recharge Voltage", "float", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            [10, "Battery Under Voltage", "float", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            [
                11,
                "Battery Bulk Charge Voltage",
                "float",
                "V",
                {"icon": "mdi:battery-outline", "device-class": "voltage"},
            ],
            [
                12,
                "Battery Float Charge Voltage",
                "float",
                "V",
                {"icon": "mdi:battery-outline", "device-class": "voltage"},
            ],
            [
                13,
                "Battery Type",
                "option",
                [
                    "AGM",
                    "Flooded",
                    "User",
                    "Pylontech",
                    "Shinheung",
                    "WECO",
                    "Soltaro",
                    "LIb-protocol compatible",
                    "3rd party Lithium",
                ],
            ],
            [14, "Max AC Charging Current", "int", "A", {"icon": "mdi:current-ac", "device-class": "current"}],
            [15, "Max Charging Current", "int", "A", {"icon": "mdi:current-ac", "device-class": "current"}],
            [16, "Input Voltage Range", "option", ["Appliance", "UPS"]],
            [
                17,
                "Output Source Priority",
                "option",
                [
                    "Utility Solar Battery",
                    "Solar Utility Battery",
                    "Solar Battery Utility",
                ],
            ],
            [
                18,
                "Charger Source Priority",
                "option",
                [
                    "Solar first",
                    "Solar + Utility",
                    "Only solar charging permitted",
                ],
            ],
            [19, "Max Parallel Units", "int", "units"],
            [
                20,
                "Machine Type",
                "str_keyed",
                {"00": "Grid tie", "01": "Off Grid", "10": "Hybrid"},
            ],
            [21, "Topology", "option", ["transformerless", "transformer"]],
            [
                22,
                "Output Mode",
                "option",
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
            [23, "Battery Redischarge Voltage", "float", "V"],
            [
                24,
                "PV OK Condition",
                "option",
                [
                    "As long as one unit of inverters has connect PV, parallel system will consider PV OK",
                    "Only All of inverters have connect PV, parallel system will consider PV OK",
                ],
            ],
            [
                25,
                "PV Power Balance",
                "option",
                [
                    "PV input max current will be the max charged current",
                    "PV input max power will be the sum of the max charged power and loads power",
                ],
            ],
            [26, "Max charging time for CV stage", "int", "min"],
            [
                27,
                "Operation Logic",
                "option",
                ["Automatic mode", "On-line mode", "ECO mode"],
            ],
            [28, "Max discharging current", "int", "A", {"icon": "mdi:current-ac", "device-class": "current"}],
        ],
        "test_responses": [
            b"(230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10 010 1 0 0 6 01 0 0 54.0 0 1\x6F\x7E\r",
        ],
    },
    "QDI": {
        "name": "QDI",
        "description": "Default Settings inquiry",
        "type": "QUERY",
        "response": [
            ["float", "AC Output Voltage", "V"],
            ["float", "AC Output Frequency", "Hz"],
            ["int", "Max AC Charging Current", "A"],
            ["float", "Battery Under Voltage", "V"],
            ["float", "Battery Float Charge Voltage", "V"],
            ["float", "Battery Bulk Charge Voltage", "V"],
            ["float", "Battery Recharge Voltage", "V"],
            ["int", "Max Charging Current", "A"],
            ["option", "Input Voltage Range", ["Appliance", "UPS"]],
            [
                "option",
                "Output Source Priority",
                ["Utility first", "Solar first", "SBU first"],
            ],
            [
                "option",
                "Charger Source Priority",
                [
                    "Solar first",
                    "Solar + Utility",
                    "Only solar charging permitted",
                ],
            ],
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
            ["option", "Buzzer", ["enabled", "disabled"]],
            ["option", "Power saving", ["disabled", "enabled"]],
            ["option", "Overload restart", ["disabled", "enabled"]],
            ["option", "Over temperature restart", ["disabled", "enabled"]],
            ["option", "LCD Backlight", ["disabled", "enabled"]],
            ["option", "Primary source interrupt alarm", ["disabled", "enabled"]],
            ["option", "Record fault code", ["disabled", "enabled"]],
            ["option", "Overload bypass", ["disabled", "enabled"]],
            ["option", "LCD reset to default", ["disabled", "enabled"]],
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
                    "Phase 2 of 2 phase output (120°)",
                    "Phase 2 of 2 phase output (180°)",
                    "Unknown Output Mode",
                ],
            ],
            ["float", "Battery Redischarge Voltage", "V"],
            [
                "option",
                "PV OK condition",
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
            ["int", "Max Charging Time at CV", "min"],
            ["int", "Max Discharging current", "A"],
        ],
        "test_responses": [
            b"(230.0 50.0 0030 44.0 54.0 56.4 46.0 60 0 0 2 0 0 0 0 0 1 1 1 0 1 0 54.0 0 1 224\xeb\xbc\r",
        ],
    },
    "QPGS": {
        "name": "QPGS",
        "description": "Parallel Information inquiry",
        "help": " -- example: QPGS0 queries the values of various metrics from instance 0 of parallel setup Inverters",
        "type": "QUERY",
        "response_type": "INDEXED",
        "response": [
            [1, "Parallel instance number", "option", ["Not valid", "valid"]],
            [2, "Serial number", "bytes:r.decode()", "", {"icon": "mdi:identifier"}],
            [
                3,
                "Work mode",
                "str_keyed",
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
                4,
                "Fault code",
                "str_keyed",
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
            [5, "Grid Voltage", "float", "V", {"icon": "mdi:power-plug", "device-class": "voltage"}],
            [6, "Grid Frequency", "float", "Hz", {"icon": "mdi:current-ac", "device-class": "frequency"}],
            [7, "AC Output Voltage", "float", "V", {"icon": "mdi:power-plug", "device-class": "voltage"}],
            [8, "AC Output Frequency", "float", "Hz", {"icon": "mdi:current-ac", "device-class": "frequency"}],
            [9, "AC Output Apparent Power", "int", "VA", {"icon": "mdi:power-plug", "device-class": "apparent_power"}],
            [
                10,
                "AC Output Active Power",
                "int",
                "W",
                {"icon": "mdi:power-plug", "device-class": "power", "state_class": "measurement"},
            ],
            [11, "Load Percentage", "int", "%", {"icon": "mdi:brightness-percent"}],
            [12, "Battery Voltage", "float", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            [13, "Battery Charging Current", "int", "A", {"icon": "mdi:current-dc", "device-class": "current"}],
            [14, "Battery Capacity", "int", "%", {"device-class": "battery"}],
            [15, "PV1 Input Voltage", "float", "V", {"icon": "mdi:solar-power", "device-class": "voltage"}],
            [
                16,
                "Total Charging Current",
                "int",
                "A",
                {"icon": "mdi:brightness-percent", "device-class": "current"},
            ],
            [
                17,
                "Total AC Output Apparent Power",
                "int",
                "VA",
                {"icon": "mdi:power-plug", "device-class": "apparent_power"},
            ],
            [
                18,
                "Total Output Active Power",
                "int",
                "W",
                {"icon": "mdi:power-plug", "device-class": "power", "state_class": "measurement"},
            ],
            [
                19,
                "Total AC Output Percentage",
                "int",
                "%",
                {"icon": "mdi:brightness-percent"},
            ],
            [
                20,
                "Inverter Status",
                "flags",
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
                21,
                "Output mode",
                "option",
                [
                    "single machine",
                    "parallel output",
                    "Phase 1 of 3 phase output",
                    "Phase 2 of 3 phase output",
                    "Phase 3 of 3 phase output",
                    "Phase 1 of 2 phase output",
                    "Phase 2 of 2 phase output (120°)",
                    "Phase 2 of 2 phase output (180°)",
                    "Unknown Output Mode",
                ],
            ],
            [
                22,
                "Charger source priority",
                "option",
                ["Solar first", "Solar + Utility", "Solar only"],
            ],
            [23, "Max Charger Current", "int", "A", {"device-class": "current"}],
            [24, "Max Charger Range", "int", "A", {"device-class": "current"}],
            [25, "Max AC Charger Current", "int", "A", {"device-class": "current"}],
            [26, "PV1 Input Current", "int", "A", {"icon": "mdi:solar-power", "device-class": "power"}],
            [
                27,
                "Battery Discharge Current",
                "int",
                "A",
                {"icon": "mdi:battery-negative", "device-class": "current"},
            ],
            [28, "PV2 Input Voltage", "float", "V", {"icon": "mdi:solar-power", "device-class": "voltage"}],
            [29, "PV2 Input Current", "int", "A", {"icon": "mdi:solar-power", "device-class": "current"}],
        ],
        "test_responses": [
            b"(0 92932105105315 B 00 000.0 00.00 230.0 50.00 0989 0907 012 53.2 009 090 349.8 009 00989 00907 011 10100110 0 1 100 120 030 02 000 275.3 02i]\r",
        ],
        "regex": "QPGS(\\d+)$",
    },
}
SETTER_COMMANDS = {
    "DAT": {
        "name": "DAT",
        "description": "Set Date Time",
        "help": " -- examples: DATYYMMDDHHMMSS (12 digits after DAT)",
        "type": "SETTER",
        "response": [["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "DAT(\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d)$",
    },
    "PCP": {
        "name": "PCP",
        "description": "Set Device Charger Priority",
        "help": " -- examples: PCP00 (set solar first), PCP01 (set solar and utility), PCP02 (set solar only charging)",
        "type": "SETTER",
        "response": [["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PCP(0[0123])$",
    },
    "PPCP": {
        "name": "PPCP",
        "description": "Set Parallel Device Charger Priority",
        "help": " -- examples: PPCP000 (set unit 1 to 00 - solar first), PPCP101 (set unit 1 to 01 - solar and utility), PPCP202 (set unit 2 to 02 - solar only charging)",
        "type": "SETTER",
        "response": [["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PPCP(\\d0[0123])$",
    },
}

class pi30m045(pi30max):
    def __str__(self):
        return "PI30 protocol handler for LV6548 and similar inverters"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI30M045"
        # Add pi30m045 specific commands to pi30max commands
        self.COMMANDS.update(QUERY_COMMANDS)
        # Add pi30m045 specific setter commands
        self.COMMANDS.update(SETTER_COMMANDS)
        log.info(f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands")

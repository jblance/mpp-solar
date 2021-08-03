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
            b"(1492932105105335005535\x94\x0e\r",
        ],
    },
    "QVFW": {
        "name": "QVFW",
        "description": "Main CPU firmware version inquiry",
        "type": "QUERY",
        "response": [["string", "Main CPU firmware version", ""]],
        "test_responses": [
            b"(VERFW:00072.70\x53\xA7\r",
            b"(VERFW:00046.05\xbe\xb6\r",
        ],
    },
    "QVFW3": {
        "name": "QVFW3",
        "description": "Remote CPU firmware version inquiry",
        "type": "QUERY",
        "response": [["string", "Remote CPU firmware version", ""]],
        "test_responses": [],
    },
    "VERFW": {
        "name": "VERFW",
        "description": "Bluetooth version inquiry",
        "type": "QUERY",
        "response": [["string", "Bluetooth version", ""]],
        "test_responses": [],
    },
    "QPIRI": {
        "name": "QPIRI",
        "description": "Current Settings inquiry",
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
            ["int", "Max charging time for CV stage", "min"],
            ["option", "Operation Logic", ["Automatic mode", "On-line mode", "ECO mode"]],
            ["int", "Max discharging current", "A"],
        ],
        "test_responses": [],
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
        "test_responses": [],
    },
    "QPIGS": {
        "name": "QPIGS",
        "description": "General Status Parameters inquiry",
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
                },
            ],
            ["int", "Solar Feed to Grid Power", "W"],
        ],
        "test_responses": [
            b"(227.2 50.0 230.3 50.0 0829 0751 010 447 54.50 020 083 0054 02.7 323.6 00.00 00000 00010110 00 00 00879 010\xf1\x8c\r",
        ],
    },
    "QPIGS2": {
        "name": "QPIGS2",
        "description": "General Status Parameters inquiry 2",
        "type": "QUERY",
        "response": [
            ["float", "PV2 Input Current", "A"],
            ["float", "PV2 Input Voltage", "V"],
            ["int", "PV2 Charging Power", "W"],
        ],
        "test_responses": [
            b"(03.1 327.3 01026 \xc9\x8b\r",
        ],
    },
    "QPGS": {
        "name": "QPGS",
        "description": "Parallel Information inquiry",
        "help": " -- example: QPGS0 queries the values of various metrics from instance 0 of parallel setup Inverters",
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
            ["float", "Grid Voltage", "V"],
            ["float", "Grid Frequency", "Hz"],
            ["float", "AC Output Voltage", "V"],
            ["float", "AC Output Frequency", "Hz"],
            ["int", "AC Output Apparent Power", "VA"],
            ["int", "AC Output Active Power", "W"],
            ["int", "Load Percentage", "%"],
            ["float", "Battery Voltage", "V"],
            ["int", "Battery Charging Current", "A"],
            ["int", "Battery Capacity", "%"],
            ["float", "PV1 Input Voltage", "V"],
            ["int", "Total Charging Current", "A"],
            ["int", "Total AC Output Apparent Power", "VA"],
            ["int", "Total Output Active Power", "W"],
            ["int", "Total AC Output Percentage", "%"],
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
                    "Phase 2 of 2 phase output (120°)",
                    "Phase 2 of 2 phase output (180°)",
                    "Unknown Output Mode",
                ],
            ],
            [
                "option",
                "Charger source priority",
                ["Utility first", "Solar first", "Solar + Utility", "Solar only"],
            ],
            ["int", "Max Charger Current", "A"],
            ["int", "Max Charger Range", "A"],
            ["int", "Max AC Charger Current", "A"],
            ["int", "PV1 Input Current", "A"],
            ["int", "Battery Discharge Current", "A"],
            ["float", "PV2 Input Voltage", "V"],
            ["int", "PV2 Input Current", "A"],
        ],
        "test_responses": [],
        "regex": "QPGS(\\d+)$",
    },
    "QMOD": {
        "name": "QMOD",
        "description": "Mode inquiry",
        "type": "QUERY",
        "response": [
            [
                "keyed",
                "Device Mode",
                {
                    "P": "Power on",
                    "S": "Standby",
                    "L": "Line",
                    "B": "Battery",
                    "F": "Fault",
                    "H": "Power Saving",
                    "D": "Shutdown",
                },
            ]
        ],
        "test_responses": [
            b"(S\x64\x39\r",
            b"(B\xe7\xc9\r",
        ],
    },
    "QPIWS": {
        "name": "QPIWS",
        "description": "Warning status inquiry",
        "type": "QUERY",
        "response": [
            [
                "stat_flags",
                "Warning",
                [
                    "PV loss warning",
                    "Inverter fault",
                    "Bus over fault",
                    "Bus under fault",
                    "Bus soft fail fault",
                    "Line fail warning",
                    "OPV short warning",
                    "Inverter voltage too low fault",
                    "Inverter voltage too high fault",
                    "Over temperature fault",
                    "Fan locked fault",
                    "Battery voltage to high fault",
                    "Battery low alarm warning",
                    "Reserved",
                    "Battery under shutdown warning",
                    "Battery derating warning",
                    "Overload fault",
                    "EEPROM fault",
                    "Inverter over current fault",
                    "Inverter soft fail fault",
                    "Self test fail fault",
                    "OP DC voltage over fault",
                    "Bat open fault",
                    "Current sensor fail fault",
                    "Battery short fault",
                    "Power limit warning",
                    "PV voltage high warning",
                    "MPPT overload fault",
                    "MPPT overload warning",
                    "Battery too low to charge warning",
                    "",
                    "Battery weak",
                    "Battery weak",
                    "Battery weak",
                    "",
                    "Battery equalisation warning",
                ],
            ]
        ],
        "test_responses": [
            b"(00000100000000001000000000000000\x56\xA6\r",
            b"(000000000000000000000000000000000000<\x8e\r",
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
                    "Utility first",
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
    "QMCHGCR": {
        "name": "QMCHGCR",
        "description": "Max Charging Current Options inquiry",
        "type": "QUERY",
        "response": [["string", "Max Charging Current", "A"]],
        "test_responses": [
            b"(010 020 030 040 050 060 070 080 090 100 110 120\x0c\xcb\r",
        ],
    },
    "QMUCHGCR": {
        "name": "QMUCHGCR",
        "description": "Max Utility Charging Current Options inquiry",
        "type": "QUERY",
        "response": [["string", "Max Utility Charging Current", "A"]],
        "test_responses": [
            b"(002 010 020 030 040 050 060 070 080 090 100 110 120\xca#\r",
        ],
    },
    "QOPPT": {
        "name": "QOPPT",
        "description": "Device Output Source Priority Time Order Inquiry",
        "type": "QUERY",
        "response": [["bytes.decode", "Device Output Source Priority Time Order", ""]],
        "test_responses": [
            b"(2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 2 1>>\r",
        ],
    },
    "QCHPT": {
        "name": "QCHPT",
        "description": "Device Charger Source Priority Time Order Inquiry",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "response": [
            [
                "option",
                "Charger Source Priority 00 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 01 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 02 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 03 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 04 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 05 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 06 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 07 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 08 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 09 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 10 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 11 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 12 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 13 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 14 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 15 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 16 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 17 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 18 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 19 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 20 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 21 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 22 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Charger Source Priority 23 hours",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Device Charger Source Priority",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Selection of Charger Source Priority Order 1",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Selection of Charger Source Priority Order 2",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
            [
                "option",
                "Selection of Charger Source Priority Order 3",
                ["undefined", "Solar first", "Solar + Utility", "Only Solar"],
            ],
        ],
        "test_responses": [
            b"(3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0\xd0\x8b\r",
        ],
    },
    "QT": {
        "name": "QT",
        "description": "Device Time Inquiry",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "response": [["bytes.decode", "Device Time", ""]],
        "test_responses": [
            b"(20210726122606JF\r",
        ],
    },
    "QBEQI": {
        "name": "QBEQI",
        "description": "Battery Equalization Status Parameters Inquiry",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "response": [
            ["option", "Equalization Enabled", ["Disabled", "Enabled"]],
            ["int", "Equalization Time", "min"],
            ["int", "Equalization Period", "day"],
            ["int", "Equalization Max Current", "A"],
            ["bytes.decode", "Reserved1", ""],
            ["float", "Equalization Voltage", "V"],
            ["bytes.decode", "Reserved2", ""],
            ["int", "Equalization Over Time", "min"],
            ["option", "Equalization Active", ["Inactive", "Active"]],
            ["int", "Equalization Elasped Time", "hour"],
        ],
        "test_responses": [
            b"(1 030 030 080 021 55.40 224 030 0 0234y?\r",
        ],
    },
    "QMN": {
        "name": "QMN",
        "description": "Model Name Inquiry",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "response": [["bytes.decode", "Model Name", ""]],
        "test_responses": [
            b"(MKS2-8000\xb2\x8d\r",
        ],
    },
    "QET": {
        "name": "QET",
        "description": "Total PV Generated Energy Inquiry",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "response": [["int", "Total PV Generated Energy", "Wh"]],
        "test_responses": [
            b"(00238800!J\r",
        ],
    },
    "QEY": {
        "name": "QEY",
        "description": "Yearly PV Generated Energy Inquiry",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "response": [
            ["int", "PV Generated Energy for Year", "Wh"],
            ["info:cv", "Year", ""],
        ],
        "test_responses": [
            b"(00238800!J\r",
        ],
        "regex": "QEY(\\d\\d\\d\\d)$",
    },
    "QEM": {
        "name": "QEM",
        "description": "Monthly PV Generated Energy Inquiry",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "response": [
            ["int", "PV Generated Energy for Month", "Wh"],
            ["info:cv[:4]", "Year", ""],
            ["info:calendar.month_name[int(cv[4:])]", "Month", ""],
        ],
        "test_responses": [
            b"(00238800!J\r",
        ],
        "regex": "QEM(\\d\\d\\d\\d\\d\\d)$",
    },
    "QED": {
        "name": "QED",
        "description": "Daily PV Generated Energy Inquiry",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "response": [
            ["int", "PV Generated Energy for Day", "Wh"],
            ["info:cv[:4]", "Year", ""],
            ["info:calendar.month_name[int(cv[4:6])]", "Month", ""],
            ["info:cv[6:]", "Day", ""],
        ],
        "test_responses": [
            b"(00238800!J\r",
        ],
        "regex": "QED(\\d\\d\\d\\d\\d\\d\\d\\d)$",
    },
    "QLT": {
        "name": "QLT",
        "description": "Total Output Load Energy Inquiry",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "response": [["int", "Total Output Load Energy", "Wh"]],
        "test_responses": [
            b"(00238800!J\r",
        ],
    },
    "QLY": {
        "name": "QLY",
        "description": "Yearly Output Load Energy Inquiry",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "response": [
            ["int", "Output Load Energy for Year", "Wh"],
            ["info:cv", "Year", ""],
        ],
        "test_responses": [
            b"(00238800!J\r",
        ],
        "regex": "QLY(\\d\\d\\d\\d)$",
    },
    "QLM": {
        "name": "QLM",
        "description": "Monthly Output Load Energy Inquiry",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "response": [
            ["int", "Output Load Energy for Month", "Wh"],
            ["info:cv[:4]", "Year", ""],
            ["info:calendar.month_name[int(cv[4:])]", "Month", ""],
        ],
        "test_responses": [
            b"(00238800!J\r",
        ],
        "regex": "QLM(\\d\\d\\d\\d\\d\\d)$",
    },
    "QLD": {
        "name": "QLD",
        "description": "Daily Output Load Energy Inquiry",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "response": [
            ["int", "Output Load Energy for Day", "Wh"],
            ["info:cv[:4]", "Year", ""],
            ["info:calendar.month_name[int(cv[4:6])]", "Month", ""],
            ["info:cv[6:]", "Day", ""],
        ],
        "test_responses": [
            b"(00238800!J\r",
        ],
        "regex": "QLD(\\d\\d\\d\\d\\d\\d\\d\\d)$",
    },
    "QLED": {
        "name": "QLED",
        "description": "LED Status Parameters Inquiry",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "response": [
            ["option", "LED Enabled", ["Disabled", "Enabled"]],
            ["option", "LED Speed", ["Low", "Medium", "Fast"]],
            ["option", "LED Effect", ["Breathing", "Unknown", "Solid", "Right Scrolling"]],
            ["int", "LED Brightness", ""],
            ["int", "LED Number of Colors", ""],
            ["bytes.decode", "RGB", ""],
        ],
        "test_responses": [
            b"(1 1 2 5 3 148000211255255255000255255\xdaj\r",
        ],
    },
}

SETTER_COMMANDS = {}
COMMANDS = QUERY_COMMANDS
COMMANDS.update(SETTER_COMMANDS)


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

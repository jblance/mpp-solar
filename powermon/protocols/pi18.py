import logging

from powermon.commands.result import ResultType
from powermon.protocols.abstractprotocol import AbstractProtocol
from mppsolar.protocols.protocol_helpers import crcPI as crc
from powermon.commands.result import Result
from powermon.commands.response_definition import ResponseType

log = logging.getLogger("pi18")

SETTER_COMMANDS = {
    "MCHGC": {
        "name": "MCHGC",
        "prefix": "^S013",
        "description": "Set Battery Max Charging Current Solar + AC             (Manual Option 11)",
        "help": " -- example: MCHGC0,030        (set unit 0 [0-9] to max charging current of  30A [    010 020 030 040 050 060 070 080])",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "MCHGC([0-9],0[1-8]0)$",
    },
    "MUCHGC": {
        "name": "MUCHGC",
        "prefix": "^S014",
        "description": "Set Battery Max AC Charging Current                     (Manual Option 13)",
        "help": " -- example: MUCHGC0,030       (set unit 0 [0-9] utility charging current to 30A [002 010 020 030 040 050 060 070 080])",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"",],
        "regex": "MUCHGC([0-9]),(002|0[1-8]0)$",
    },
    "PBT": {
        "name": "PBT",
        "prefix": "^S007",
        "description": "Set Battery Type                                        (Manual Option 14)",
        "help": " -- example: PBT0              (set battery as PBT0 [0: AGM], PBT1 [1: FLOODED], PBT2 [2: USER])",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "PBT([012])$",
    },
    "PCP": {
        "name": "PCP",
        "prefix": "^S009",
        "description": "Set charging source priority                            (Manual Option 10)",
        "help": " -- example: PCP0,1            (set unit 0 [0-9] to 0: Solar first, 1: Solar and Utility, 2: Only solar)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"^1\x0b\xc2\r", b"^0\x1b\xe3\r",],
        "regex": "PCP([0-9],[012])$",
    },
#    "PE": {
#        "name": "PE",
#        "description": "Set the enabled state of an Inverter setting",
#        "help": " -- examples: PEa - enable a (buzzer) [a=buzzer, b=overload bypass, j=power saving, K=LCD go to default after 1min, u=overload restart, v=overtemp restart, x=backlight, y=alarm on primary source interrupt, z=fault code record]",
#        "response_type": ResultType.ACK,
#        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
#        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
#        "regex": "PE(.+)$",
#    },
#   "PD": {
#       "name": "PD",
#       "description": "Set the disabled state of an Inverter setting",
#       "help": " -- examples: PDa - disable a (buzzer) [a=buzzer, b=overload bypass, j=power saving, K=LCD go to default after 1min, u=overload restart, v=overtemp restart, x=backlight, y=alarm on primary source interrupt, z=fault code record]",
#       "response_type": ResultType.ACK,
#       "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
#       "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
#       "regex": "PD(.+)$",
#   },
#    "PF": {
#        "name": "PF",
#        "description": "Set Control Parameters to Default Values",
#        "help": " -- example PF (reset control parameters to defaults)",
#        "response_type": ResultType.ACK,
#        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
#        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
#    },
    "PGR": {
        "name": "PGR",
        "description": "Set Grid Working Range",
        "help": " -- examples: PCR00 (set device working range to appliance), PCR01 (set device working range to UPS)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "PGR(0[01])$",
    },
    "POP": {
        "name": "POP",
        "description": "Set Device Output Source Priority",
        "help": " -- examples: POP00 (set utility first), POP01 (set solar first), POP02 (set SBU priority)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "POP(0[012])$",
    },
    "POPLG": {
        "name": "POPLG",
        "description": "Set Device Operation Logic",
        "help": " -- examples: POPLG00 (set Auto mode), POPLG01 (set Online mode), POPLG02 (set ECO mode)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "POPLG(0[012])$",
    },
    "POPM": {
        "name": "POPM",
        "description": "Set Device Output Mode (for 4000/5000)",
        "help": " -- examples: POPM01 (set unit 0 to 1 - parallel output), POPM10 (set unit 1 to 0 - single machine output), POPM02 (set unit 0 to 2 - phase 1 of 3), POPM13 (set unit 1 to 3 - phase 2 of 3), POPM24 (set unit 2 to 4 - phase 3 of 3)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "POPM(\\d[01234])$",
    },
    "PPCP": {
        "name": "PPCP",
        "description": "Set Parallel Device Charger Priority (for 4000/5000)",
        "help": " -- examples: PPCP000 (set unit 1 to 00 - utility first), PPCP101 (set unit 1 to 01 - solar first), PPCP202 (set unit 2 to 02 - solar and utility), PPCP003 (set unit 0 to 03 - solar only charging)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "PPCP(\\d0[0123])$",
    },
    "PPVOKC": {
        "name": "PPVOKC",
        "description": "Set PV OK Condition",
        "help": " -- examples: PPVOKC0 (as long as one unit has connected PV, parallel system will consider PV OK), PPVOKC1 (only if all inverters have connected PV, parallel system will consider PV OK)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "PPVOKC([01])$",
    },
    "PSDV": {
        "name": "PSDV",
        "description": "Set Battery Cut-off Voltage",
        "help": " -- example PSDV40.0 - set battery cut-off voltage to 40V (40.0 - 48.0V for 48V unit)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "PSDV(\\d\\d\\.\\d)$",
    },
    "PSPB": {
        "name": "PSPB",
        "description": "Set Solar Power Balance",
        "help": " -- examples: PSPB0 (PV input max current will be the max charged current), PSPB1 (PV input max power will be the sum of the max charge power and loads power)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "PSPB([01])$",
    },
    "PBATCD": {
        "name": "PBATCD",
        "description": "Battery charge/discharge controlling command",
        "help": " -- examples: PBATCDxxx (please read description, use carefully)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "PBATCD([01][01][01])$",
    },
    "DAT": {
        "name": "DAT",
        "description": "Set Date Time",
        "help": " -- examples: DATYYYYMMDDHHMMSS (14 digits after DAT)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "DAT(\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d)$",
    },
    "PBATMAXDISC": {
        "name": "PBATMAXDISC",
        "description": "Battery max discharge current",
        "help": " -- examples: PBATMAXDISCxxx (000- disable or 030-150A)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "PBATMAXDISC([01]\\d\\d)$",
    },
    "BTA": {
        "name": "BTA",
        "description": "Calibrate inverter battery voltage",
        "help": " -- examples: BTA-01 (reduce inverter reading by 0.05V), BTA+09 (increase inverter reading by 0.45V)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "BTA([-+]0\\d)$",
    },
    "PSAVE": {
        "name": "PSAVE",
        "description": "Save EEPROM changes",
        "help": " -- examples: PSAVE (save changes to eeprom)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r"],
    },
}

QUERY_COMMANDS = {
    "Q1": {
        "name": "Q1",
        "description": "Q1 query",
        "response_type": ResultType.INDEXED,
        "response": [
            [0, "Time until the end of absorb charging", ResponseType.INT, "sec"],
            [1, "Time until the end of float charging", ResponseType.INT, "sec"],
            [2, "SCC Flag", ResponseType.OPTION, ["SCC not communicating?", "SCC is powered and communicating"]],
            [3, "AllowSccOnFlag", ResponseType.BYTES, ""],
            [4, "ChargeAverageCurrent", ResponseType.BYTES, ""],
            [5, "SCC PWM temperature", ResponseType.INT, "\u00b0C", {"device-class": "temperature"}],
            [6, "Inverter temperature", ResponseType.INT, "\u00b0C", {"device-class": "temperature"}],
            [7, "Battery temperature", ResponseType.INT, "\u00b0C", {"device-class": "temperature"}],
            [8, "Transformer temperature", ResponseType.INT, "\u00b0C", {"device-class": "temperature"}],
            [9, "GPIO13", ResponseType.INT, ""],
            [10, "Fan lock status", ResponseType.OPTION, ["Not locked", "Locked"]],
            [11, "Not used", ResponseType.BYTES, ""],
            [12, "Fan PWM speed", ResponseType.INT, "%"],
            [13, "SCC charge power", ResponseType.INT, "W", {"icon": "mdi:solar-power", "device-class": "power"}],
            [14, "Parallel Warning", ResponseType.BYTES, ""],
            [15, "Sync frequency", ResponseType.FLOAT, ""],
            [
                16,
                "Inverter charge status",
                ResponseType.STR_KEYED,
                {"10": "nocharging", "11": "bulk stage", "12": "absorb", "13": "float"},
                {"icon": "mdi:book-open"},
            ],
        ],
        "test_responses": [b"(00000 00000 01 01 00 059 045 053 068 00 00 000 0040 0580 0000 50.00 139\xb9\r"],
    },
    "QBOOT": {
        "name": "QBOOT",
        "description": "DSP Has Bootstrap inquiry",
        "response_type": ResultType.INDEXED,
        "response": [[0, "DSP Has Bootstrap", ResponseType.OPTION, ["No", "Yes"]]],
        "test_responses": [b"(0\xb9\x1c\r"],
    },
    "QDI": {
        "name": "QDI",
        "description": "Default Settings inquiry",
        "help": " -- queries the default settings from the Inverter",
        "response_type": ResultType.INDEXED,
        "response": [
            [0, "AC Output Voltage", ResponseType.FLOAT, "V"],
            [1, "AC Output Frequency", ResponseType.FLOAT, "Hz"],
            [2, "Max AC Charging Current", ResponseType.INT, "A"],
            [3, "Battery Under Voltage", ResponseType.FLOAT, "V"],
            [4, "Battery Float Charge Voltage", ResponseType.FLOAT, "V"],
            [5, "Battery Bulk Charge Voltage", ResponseType.FLOAT, "V"],
            [6, "Battery Recharge Voltage", ResponseType.FLOAT, "V"],
            [7, "Max Charging Current", ResponseType.INT, "A"],
            [8, "Input Voltage Range", ResponseType.OPTION, ["Appliance", "UPS"]],
            [9, "Output Source Priority", ResponseType.OPTION, ["Utility first", "Solar first", "SBU first"]],
            [
                10,
                "Charger Source Priority",
                ResponseType.OPTION,
                ["Utility first", "Solar first", "Solar + Utility", "Only solar charging permitted"],
            ],
            [11, "Battery Type", ResponseType.OPTION, ["AGM", "Flooded", "User"]],
            [12, "Buzzer", ResponseType.OPTION, ["enabled", "disabled"]],
            [13, "Power saving", ResponseType.OPTION, ["disabled", "enabled"]],
            [14, "Overload restart", ResponseType.OPTION, ["disabled", "enabled"]],
            [15, "Over temperature restart", ResponseType.OPTION, ["disabled", "enabled"]],
            [16, "LCD Backlight", ResponseType.OPTION, ["disabled", "enabled"]],
            [17, "Primary source interrupt alarm", ResponseType.OPTION, ["disabled", "enabled"]],
            [18, "Record fault code", ResponseType.OPTION, ["disabled", "enabled"]],
            [19, "Overload bypass", ResponseType.OPTION, ["disabled", "enabled"]],
            [20, "LCD reset to default", ResponseType.OPTION, ["disabled", "enabled"]],
            [
                21,
                "Output mode",
                ResponseType.OPTION,
                [
                    "single machine output",
                    "parallel output",
                    "Phase 1 of 3 Phase output",
                    "Phase 2 of 3 Phase output",
                    "Phase 3 of 3 Phase output",
                    "Phase 1 of 2 phase output",
                    "Phase 2 of 2 phase output",
                    "unknown output phase",
                ],
            ],
            [22, "Battery Redischarge Voltage", ResponseType.FLOAT, "V"],
            [
                23,
                "PV OK condition",
                ResponseType.OPTION,
                [
                    "As long as one unit of inverters has connect PV, parallel system will consider PV OK",
                    "Only All of inverters have connect PV, parallel system will consider PV OK",
                ],
            ],
            [
                24,
                "PV Power Balance",
                ResponseType.OPTION,
                [
                    "PV input max current will be the max charged current",
                    "PV input max power will be the sum of the max charged power and loads power",
                ],
            ],
            [25, "Unknown Value", ResponseType.INT, ""],
        ],
        "test_responses": [
            b"(230.0 50.0 0030 42.0 54.0 56.4 46.0 60 0 0 2 0 0 0 0 0 1 1 0 0 1 0 54.0 0 1 000\x9E\x60\r"
        ],
    },
    "QFLAG": {
        "name": "QFLAG",
        "description": "Flag Status inquiry",
        "help": " -- queries the enabled / disabled state of various Inverter settings (e.g. buzzer, overload, interrupt alarm)",
        "response_type": ResultType.INDEXED,
        "response": [
            [
                0,
                "Device Status",
                ResponseType.ENFLAGS,
                {
                    "a": {"name": "Buzzer", "state": "disabled"},
                    "b": {"name": "Overload Bypass", "state": "disabled"},
                    "j": {"name": "Power Saving", "state": "disabled"},
                    "k": {"name": "LCD Reset to Default", "state": "disabled"},
                    "u": {"name": "Overload Restart", "state": "disabled"},
                    "v": {"name": "Over Temperature Restart", "state": "disabled"},
                    "x": {"name": "LCD Backlight", "state": "disabled"},
                    "y": {"name": "Primary Source Interrupt Alarm", "state": "disabled"},
                    "z": {"name": "Record Fault Code", "state": "disabled"},
                },
            ]
        ],
        "test_responses": [b"(EakxyDbjuvz\x2F\x29\r"],
    },
    "QID": {
        "name": "QID",
        "description": "Device Serial Number inquiry",
        "help": " -- queries the device serial number",
        "response_type": ResultType.INDEXED,
        "response": [[0, "Serial Number", ResponseType.BYTES, ""]],
        "test_responses": [b"(9293333010501\xbb\x07\r"],
    },
    "QMCHGCR": {
        "name": "QMCHGCR",
        "description": "Max Charging Current Options inquiry",
        "help": " -- queries the maximum charging current setting of the Inverter",
        "response_type": ResultType.MULTIVALUED,
        "response": [[0, "Max Charging Current Options", ResponseType.STRING, "A"]],
        "test_responses": [b"(010 020 030 040 050 060 070 080 090 100 110 120\x0c\xcb\r"],
    },
    "QMOD": {
        "name": "QMOD",
        "description": "Mode inquiry",
        "help": " -- queries the Inverter mode",
        "response_type": ResultType.INDEXED,
        "response": [
            [
                0,
                "Device Mode",
                ResponseType.STR_KEYED,
                {"P": "Power on", "S": "Standby", "L": "Line", "B": "Battery", "F": "Fault", "H": "Power saving"},
            ]
        ],
        "test_responses": [b"(S\xe5\xd9\r"],
    },
    "QMN": {
        "name": "QMN",
        "description": "Model Name Inquiry",
        "response_type": ResultType.INDEXED,
        "response": [[0, "Model Name", ResponseType.BYTES, ""]],
        "test_responses": [b"(MKS2-8000\xb2\x8d\r",],
    },
    "QGMN": {
        "name": "QGMN",
        "description": "General Model Name Inquiry",
        "response_type": ResultType.INDEXED,
        "response": [[0, "General Model Number", ResponseType.BYTES, ""]],
        "test_responses": [b"(044\xc8\xae\r",],
    },
    "QMUCHGCR": {
        "name": "QMUCHGCR",
        "description": "Max Utility Charging Current Options inquiry",
        "help": " -- queries the maximum utility charging current setting of the Inverter",
        "response_type": ResultType.MULTIVALUED,
        "response": [[0, "Max Utility Charging Current", ResponseType.STRING, "A"]],
        "test_responses": [b"(002 010 020 030 040 050 060 070 080 090 100 110 120\xca#\r"],
    },
    "QOPM": {
        "name": "QOPM",
        "description": "Output Mode inquiry",
        "help": " -- queries the output mode of the Inverter (e.g. single, parallel, phase 1 of 3 etc)",
        "response_type": ResultType.INDEXED,
        "response": [
            [
                0,
                "Output mode",
                ResponseType.OPTION,
                [
                    "single machine output",
                    "parallel output",
                    "Phase 1 of 3 Phase output",
                    "Phase 2 of 3 Phase output",
                    "Phase 3 of 3 Phase output",
                    "Phase 1 of 2 phase output",
                    "Phase 2 of 2 phase output",
                    "unknown output phase",
                ],
            ]
        ],
        "test_responses": [b"(0\xb9\x1c\r"],
    },
    "QPGS": {
        "name": "QPGS",
        "description": "Parallel Information inquiry",
        "help": " -- example: QPGS1 queries the values of various metrics from instance 1 of parallel setup Inverters (numbers from 0)",
        "response_type": ResultType.INDEXED,
        "response": [
            [0, "Parallel instance number", ResponseType.OPTION, ["Not valid", "valid"]],
            [1, "Serial number", ResponseType.BYTES, ""],
            [
                2,
                "Work mode",
                ResponseType.STR_KEYED,
                {
                    "P": "Power On Mode",
                    "S": "Standby Mode",
                    "L": "Line Mode",
                    "B": "Battery Mode",
                    "F": "Fault Mode",
                    "H": "Power Saving Mode",
                },
            ],
            [
                3,
                "Fault code",
                ResponseType.STR_KEYED,
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
                    "11": "Main relay failed",
                    "51": "Over current inverter",
                    "52": "Bus soft start failed",
                    "53": "Inverter soft start failed",
                    "54": "Self-test failed",
                    "55": "Over DC voltage on output of inverter",
                    "56": "Battery connection is open",
                    "57": "Current sensor failed",
                    "58": "Output voltage is too low",
                    "60": "Inverter negative power",
                    "71": "Parallel version different",
                    "72": "Output circuit failed",
                    "80": "CAN communication failed",
                    "81": "Parallel host line lost",
                    "82": "Parallel synchronized signal lost",
                    "83": "Parallel battery voltage detect different",
                    "84": "Parallel Line voltage or frequency detect different",
                    "85": "Parallel Line input current unbalanced",
                    "86": "Parallel output setting different",
                },
            ],
            [4, "Grid voltage", ResponseType.FLOAT, "V"],
            [5, "Grid frequency", ResponseType.FLOAT, "Hz"],
            [6, "AC output voltage", ResponseType.FLOAT, "V"],
            [7, "AC output frequency", ResponseType.FLOAT, "Hz"],
            [8, "AC output apparent power", ResponseType.INT, "VA"],
            [9, "AC output active power", ResponseType.INT, "W"],
            [10, "Load percentage", ResponseType.INT, "%"],
            [11, "Battery voltage", ResponseType.FLOAT, "V"],
            [12, "Battery charging current", ResponseType.INT, "A"],
            [13, "Battery capacity", ResponseType.INT, "%"],
            [14, "PV Input Voltage", ResponseType.FLOAT, "V"],
            [15, "Total charging current", ResponseType.INT, "A"],
            [16, "Total AC output apparent power", ResponseType.INT, "VA"],
            [17, "Total output active power", ResponseType.INT, "W"],
            [18, "Total AC output percentage", ResponseType.INT, "%"],
            [
                19,
                "Inverter Status",
                ResponseType.FLAGS,
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
                20,
                "Output mode",
                ResponseType.OPTION,
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
                21,
                "Charger source priority",
                ResponseType.OPTION,
                ["Utility first", "Solar first", "Solar + Utility", "Solar only"],
            ],
            [22, "Max charger current", ResponseType.INT, "A"],
            [23, "Max charger range", ResponseType.INT, "A"],
            [24, "Max AC charger current", ResponseType.INT, "A"],
            [25, "PV input current", ResponseType.INT, "A"],
            [26, "Battery discharge current", ResponseType.INT, "A"],
            [27, "Unknown float", ResponseType.FLOAT, ""],
            [28, "Unknown flags?", ResponseType.STRING, ""],
        ],
        "test_responses": [
            b"(1 92931701100510 B 00 000.0 00.00 230.6 50.00 0275 0141 005 51.4 001 100 083.3 002 00574 00312 003 10100110 1 2 060 120 10 04 000\xcc#\r",
            b"(1 92912102100033 B 00 000.0 00.00 120.1 59.99 0048 0000 000 53.1 000 059 000.0 000 00154 00016 000 00000110 7 1 060 120 030 00 000 000.0 00\xe7c\r",
            b"QPGS0?\xda\r",
        ],
        "regex": "QPGS(\\d+)$",
    },
    "QPI": {
        "name": "QPI",
        "description": "Protocol ID inquiry",
        "help": " -- queries the device protocol ID. e.g. PI30 for HS series",
        "response_type": ResultType.INDEXED,
        "response": [[0, "Protocol Id", ResponseType.BYTES, ""]],
        "test_responses": [b"(PI30\x9a\x0b\r"],
    },
    "QPIz": { # Question: is this a typo? Duplicate of QPI?
        "name": "QPIz",
        "description": "Protocol ID inquiry",
        "help": " -- queries the device protocol ID. e.g. PI30 for HS series",
        "response_type": ResultType.INDEXED,
        "response": [[0, "Protocol ID", ResponseType.BYTES, ""]],
        "test_responses": [b"(PI30\x9a\x0b\r"],
    },
    "QPIGS": {
        "name": "QPIGS",
        "description": "General Status Parameters inquiry",
        "help": " -- queries the value of various metrics from the Inverter",
        "response_type": ResultType.INDEXED,
        "response": [
            [
                0,
                "AC Input Voltage",
                ResponseType.FLOAT,
                "V",
                {"icon": "mdi:transmission-tower-export", "device-class": "voltage"},
            ],
            [1, "AC Input Frequency", ResponseType.FLOAT, "Hz", {"icon": "mdi:current-ac", "device-class": "frequency"}],
            [2, "AC Output Voltage", ResponseType.FLOAT, "V", {"icon": "mdi:power-plug", "device-class": "voltage"}],
            [3, "AC Output Frequency", ResponseType.FLOAT, "Hz", {"icon": "mdi:current-ac", "device-class": "frequency"}],
            [4, "AC Output Apparent Power", ResponseType.INT, "VA", {"icon": "mdi:power-plug", "device-class": "apparent_power"}],
            [
                5,
                "AC Output Active Power",
                ResponseType.INT,
                "W",
                {"icon": "mdi:power-plug", "device-class": "power", "state_class": "measurement"},
            ],
            [6, "AC Output Load", ResponseType.INT, "%", {"icon": "mdi:brightness-percent"}],
            [7, "BUS Voltage", ResponseType.INT, "V", {"icon": "mdi:details", "device-class": "voltage"}],
            [8, "Battery Voltage", ResponseType.FLOAT, "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            [9, "Battery Charging Current", ResponseType.INT, "A", {"icon": "mdi:current-dc", "device-class": "current"}],
            [10, "Battery Capacity", ResponseType.INT, "%", {"device-class": "battery"}],
            [
                11,
                "Inverter Heat Sink Temperature",
                ResponseType.INT,
                "\u00b0C",
                {"icon": "mdi:details", "device-class": "temperature"},
            ],
            [12, "PV Input Current", ResponseType.FLOAT, "A", {"icon": "mdi:solar-power", "device-class": "current"}],
            [13, "PV Input Voltage", ResponseType.FLOAT, "V", {"icon": "mdi:solar-power", "device-class": "voltage"}],
            [14, "Battery Voltage from SCC", ResponseType.FLOAT, "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            [15, "Battery Discharge Current", ResponseType.INT, "A", {"icon": "mdi:battery-negative", "device-class": "current"}],
            [
                16,
                "Device Status",
                ResponseType.FLAGS,
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
            [17, "RSV1", ResponseType.INT, "A"],
            [18, "RSV2", ResponseType.INT, "A"],
            [
                19,
                "PV Input Power",
                ResponseType.INT,
                "W",
                {"icon": "mdi:solar-power", "device-class": "power", "state_class": "measurement"},
            ],
            [20, "Device Status2", ResponseType.FLAGS, ["Is Charging to Float", "Is Switched On", "Is Reserved"]],
        ],
        "test_responses": [
            b"(000.0 00.0 230.0 49.9 0161 0119 003 460 57.50 012 100 0069 0014 103.8 57.45 00000 00110110 00 00 00856 010\x24\x8c\r",
        ],
    },
    "^P007PIRI": {
        "name": "^P007PIRI",
        "prefix": "^P007",
        "description": "Current Settings inquiry",
        "help": " -- queries the current settings from the Inverter",
        "response_type": ResultType.INDEXED,
        "response": [
            [0, "AC Input Voltage", ResponseType.TEN_INT, "V"],
            [1, "AC Input Current", ResponseType.TEN_INT, "A"],
            [2, "AC Output Voltage", ResponseType.TEN_INT, "V"],
            [3, "AC Output Frequency", ResponseType.TEN_INT, "Hz"],
            [4, "AC Output Current", ResponseType.TEN_INT, "A"],
            [5, "AC Output Apparent Power", ResponseType.INT, "VA"],
            [6, "AC Output Active Power", ResponseType.INT, "W"],
            [7, "Battery Voltage", ResponseType.TEN_INT, "V"],
            [8, "Battery re-charge Voltage", ResponseType.TEN_INT, "V"],
            [9, "Battery re-discharge Voltage", ResponseType.TEN_INT, "V"],
            [10, "Battery Under Voltage", ResponseType.TEN_INT, "V"],
            [11, "Battery Bulk Charge Voltage", ResponseType.TEN_INT, "V"],
            [12, "Battery Float Charge Voltage", ResponseType.TEN_INT, "V"],
            [13, "Battery Type", ResponseType.STR_KEYED,
                {
                   "0":"AGM",
                   "1":"Flooded",
                   "2":"User",
                },
            ],
            [14, "Max AC Charging Current", ResponseType.INT, "A"],
            [15, "Max Charging Current", ResponseType.INT, "A"],
            [16, "Input Voltage Range", ResponseType.OPTION,
                [
                   "Appliance",
                   "UPS",
                ]
            ],
            [17, "Output Source Priority", ResponseType.OPTION,
                [
                   "Solar - Utility - Battery",
                   "Solar - Battery - Utility",
                ]
            ],
            [18, "Charger Source Priority",  ResponseType.OPTION,
                [
                   "Solar First",
                   "Solar + Utility",
                   "Only solar charging permitted",
                 ],
            ],
            [19, "Max Parallel Units", ResponseType.INT, "units"],
            [20, "Machine Type", ResponseType.STR_KEYED,
                {
                   "0": "Off Grid",
                   "1": "Grid Tie",
                },
            ],
            [21, "Topology", ResponseType.OPTION,
                [
                   "transformerless",
                   "transformer",
                ]
            ],
            [22, "Output Mode", ResponseType.OPTION,
                [
                   "single machine output",
                   "parallel output",
                   "Phase 1 of 3 Phase output",
                   "Phase 2 of 3 Phase output",
                   "Phase 3 of 3 Phase output",
                ],
            ],
            [23, "Solar power priority", ResponseType.OPTION,
                [
                   "Battery-Load-Utiliy + AC Charger"
                   "Load-Battery-Utiliy",
                ],
            ],
            [24, "MPPT strings", ResponseType.INT, ""],
            [25, "Unknown flags?", ResponseType.STRING, ""],

        ],
        "test_responses": [
            b"^D0882300,217,2300,500,217,5000,5000,480,480,530,440,570,570,2,10,070,1,1,1,9,0,0,0,0,1,00\xe1k\r",
            # ac_input_voltage=Invalid response for AC Input Voltage: b'D0882300,217,2300,500,217,5000,5000,480,480,530,440,570,570,2,10,070,1,1,1,9,0,0,0,0,1,00'

        ],
    },
    "QPIWS": {
        "name": "QPIWS",
        "description": "Warning status inquiry",
        "help": " -- queries any active warnings flags from the Inverter",
        "response_type": ResultType.INDEXED,
        "response": [
            [
                0,
                "Warning",
                ResponseType.FLAGS,
                [
                    "",
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
                    "Reserved",
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
                    "",
                ],
            ]
        ],
        "test_responses": [b"(00000100000000001000000000000000\x56\xA6\r"],
    },
    "QVFW": {
        "name": "QVFW",
        "description": "Main CPU firmware version inquiry",
        "help": " -- queries the main CPU firmware version",
        "response_type": ResultType.INDEXED,
        "response": [[0, "Main CPU firmware version", ResponseType.BYTES, ""]],
        "test_responses": [b"(VERFW:00072.70\x53\xA7\r"],
    },
    "QVFW2": {
        "name": "QVFW2",
        "description": "Secondary CPU firmware version inquiry",
        "help": " -- queries the secondary CPU firmware version",
        "response_type": ResultType.INDEXED,
        "response": [[0, "Secondary CPU firmware version", ResponseType.BYTES, ""]],
        "test_responses": [b"(VERFW:00072.70\x53\xA7\r"],
    },
}


class pi18(AbstractProtocol):
    def __str__(self):
        return "PI18 protocol handler"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI18"
        self.add_command_definitions(QUERY_COMMANDS, "QUERY")
        self.add_command_definitions(SETTER_COMMANDS, "SETTER")
        self.STATUS_COMMANDS = ["PIGS"]
        self.SETTINGS_COMMANDS = ["PIRI", "QFLAG"]
        self.DEFAULT_COMMAND = "PI"
        self.ID_COMMANDS = ["PI", "GMN", "MN"]
        # log.info(f'Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands')

    def check_response_valid(self, result: Result):
        # fail if no response
        if result.raw_response is None:
            result.is_valid = False
            result.error = True
            result.error_messages.append("failed validity check: response was empty")
            return
        # fail if dict??? not sure what this is for
        if type(result.raw_response) is dict:
            result.is_valid = False
            result.error = True
            result.error_messages.append("failed validity check: incorrect raw_response format (found dict)")
            return
        # fail on short responses
        if len(result.raw_response) <= 3:
            result.is_valid = False
            result.error = True
            result.error_messages.append(
                f"failed validity check: response to short len was {len(result.raw_response)}"
            )
            return
        # check crc matches the calculated one
        calc_crc_high, calc_crc_low = crc(result.raw_response[:-3])
        if type(result.raw_response) is str:
            crc_high, crc_low = ord(result.raw_response[-3]), ord(result.raw_response[-2])
        else:
            crc_high, crc_low = result.raw_response[-3], result.raw_response[-2]
        if [calc_crc_high, calc_crc_low] != [crc_high, crc_low]:
            result.is_valid = False
            result.error = True
            result.error_messages.append(
                f"failed validity check: response has invalid CRC - got '\\x{crc_high:02x}\\x{crc_low:02x}', calculated '\\x{calc_crc_high:02x}\\x{calc_crc_low:02x}'"
            )
            return
            # if result.raw_response[-3:-1] != bytes([calc_crc_high, calc_crc_low]):
        log.debug("CRCs match")
        return

    def get_responses(self, response) -> list:
        """
        Override the default get_responses as its different for PI18
        """
        if not response:
            return ["No response"]
        responses = response.split(b",")
        if responses[0] == b"^0\x1b\xe3\r":
            # is a reject response
            return ["NAK"]
        elif responses[0] == b"^1\x0b\xc2\r":
            # is a successful acknowledgement response
            return ["ACK"]

        # Drop ^Dxxx from first response
        responses[0] = responses[0][5:]
        # Remove CRC of last response
        responses[-1] = responses[-1][:-3]
        return responses

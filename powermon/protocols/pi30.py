import logging

from powermon.protocols import ResponseType
from powermon.protocols.abstractprotocol import AbstractProtocol
from mppsolar.protocols.protocol_helpers import crcPI as crc

log = logging.getLogger("pi30")

SETTER_COMMANDS = {
    "F": {
        "name": "F",
        "description": "Set Device Output Frequency",
        "help": " -- examples: F50 (set output frequency to 50Hz) or F60 (set output frequency to 60Hz)",
        "response_type": ResponseType.ACK,
        "response": [
            [1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "F([56]0)$",
    },
    "MCHGC": {
        "name": "MCHGC",
        "description": "Set Max Charging Current (for parallel units)",
        "help": " -- examples: MCHGC040 (set unit 0 to max charging current of 40A), MCHGC160 (set unit 1 to max charging current of 60A)",
        "response_type": ResponseType.ACK,
        "response": [
            [1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "MCHGC(\\d\\d\\d)$",
    },
    "MNCHGC": {
        "name": "MNCHGC",
        "description": "Set Utility Max Charging Current (more than 100A) (for 4000/5000)",
        "help": " -- example: MNCHGC1120 (set unit 1 utility max charging current to 120A)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(ACK\x39\x20\r",
            b"(NAK\x73\x73\r",
        ],
        "regex": "MNCHGC(\\d\\d\\d\\d)$",
    },
    "MUCHGC": {
        "name": "MUCHGC",
        "description": "Set Utility Max Charging Current",
        "help": " -- example: MUCHGC130 (set unit 1 utility max charging current to 30A)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "MUCHGC(\\d\\d\\d)$",
    },
    "PBCV": {
        "name": "PBCV",
        "description": "Set Battery re-charge voltage",
        "help": " -- example PBCV44.0 - set re-charge voltage to 44V (12V unit: 11V/11.3V/11.5V/11.8V/12V/12.3V/12.5V/12.8V, 24V unit: 22V/22.5V/23V/23.5V/24V/24.5V/25V/25.5V, 48V unit: 44V/45V/46V/47V/48V/49V/50V/51V)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PBCV(\\d\\d\\.\\d)$",
    },
    "PBDV": {
        "name": "PBDV",
        "description": "Set Battery re-discharge voltage",
        "help": " -- example PBDV48.0 - set re-discharge voltage to 48V (12V unit: 00.0V/12V/12.3V/12.5V/12.8V/13V/13.3V/13.5V/13.8V/14V/14.3V/14.5, 24V unit: 00.0V/24V/24.5V/25V/25.5V/26V/26.5V/27V/27.5V/28V/28.5V/29V, 48V unit: 00.0V/48V/49V/50V/51V/52V/53V/54V/55V/56V/57V/58V, 00.0V means battery is full(charging in float mode).)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PBDV(\\d\\d\\.\\d)$",
    },
    "PBFT": {
        "name": "PBFT",
        "description": "Set Battery Float Charging Voltage",
        "help": " -- example PBFT58.0 - set battery float charging voltage to 58V (48.0 - 58.4V for 48V unit)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PBFT(\\d\\d\\.\\d)$",
    },
    "PBT": {
        "name": "PBT",
        "description": "Set Battery Type",
        "help": " -- examples: PBT00 (set battery as AGM), PBT01 (set battery as FLOODED), PBT02 (set battery as USER)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PBT(0[012])$",
    },
    "PCP": {
        "name": "PCP",
        "description": "Set Device Charger Priority",
        "help": " -- examples: PCP00 (set utility first), PCP01 (set solar first), PCP02 (HS only: set solar and utility), PCP03 (set solar only charging)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PCP(0[0123])$",
    },
    "PCVV": {
        "name": "PCVV",
        "description": "Set Battery C.V. (constant voltage) charging voltage",
        "help": " -- example PCVV48.0 - set charging voltage to 48V (48.0 - 58.4V for 48V unit)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PCVV(\\d\\d\\.\\d)$",
    },
    "PE": {
        "name": "PE",
        "description": "Set the enabled state of an Inverter setting",
        "help": " -- examples: PEa - enable a (buzzer) [a=buzzer, b=overload bypass, j=power saving, K=LCD go to default after 1min, u=overload restart, v=overtemp restart, x=backlight, y=alarm on primary source interrupt, z=fault code record]",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PE(.+)$",
    },
    "PD": {
        "name": "PD",
        "description": "Set the disabled state of an Inverter setting",
        "help": " -- examples: PDa - disable a (buzzer) [a=buzzer, b=overload bypass, j=power saving, K=LCD go to default after 1min, u=overload restart, v=overtemp restart, x=backlight, y=alarm on primary source interrupt, z=fault code record]",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PD(.+)$",
    },
    "PF": {
        "name": "PF",
        "description": "Set Control Parameters to Default Values",
        "help": " -- example PF (reset control parameters to defaults)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
    },
    "PGR": {
        "name": "PGR",
        "description": "Set Grid Working Range",
        "help": " -- examples: PCR00 (set device working range to appliance), PCR01 (set device working range to UPS)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PGR(0[01])$",
    },
    "POP": {
        "name": "POP",
        "description": "Set Device Output Source Priority",
        "help": " -- examples: POP00 (set utility first), POP01 (set solar first), POP02 (set SBU priority)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "POP(0[012])$",
    },
    "POPLG": {
        "name": "POPLG",
        "description": "Set Device Operation Logic",
        "help": " -- examples: POPLG00 (set Auto mode), POPLG01 (set Online mode), POPLG02 (set ECO mode)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "POPLG(0[012])$",
    },
    "POPM": {
        "name": "POPM",
        "description": "Set Device Output Mode (for 4000/5000)",
        "help": " -- examples: POPM01 (set unit 0 to 1 - parallel output), POPM10 (set unit 1 to 0 - single machine output), POPM02 (set unit 0 to 2 - phase 1 of 3), POPM13 (set unit 1 to 3 - phase 2 of 3), POPM24 (set unit 2 to 4 - phase 3 of 3)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "POPM(\\d[01234])$",
    },
    "PPCP": {
        "name": "PPCP",
        "description": "Set Parallel Device Charger Priority (for 4000/5000)",
        "help": " -- examples: PPCP000 (set unit 1 to 00 - utility first), PPCP101 (set unit 1 to 01 - solar first), PPCP202 (set unit 2 to 02 - solar and utility), PPCP003 (set unit 0 to 03 - solar only charging)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PPCP(\\d0[0123])$",
    },
    "PPVOKC": {
        "name": "PPVOKC",
        "description": "Set PV OK Condition",
        "help": " -- examples: PPVOKC0 (as long as one unit has connected PV, parallel system will consider PV OK), PPVOKC1 (only if all inverters have connected PV, parallel system will consider PV OK)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PPVOKC([01])$",
    },
    "PSDV": {
        "name": "PSDV",
        "description": "Set Battery Cut-off Voltage",
        "help": " -- example PSDV40.0 - set battery cut-off voltage to 40V (40.0 - 48.0V for 48V unit)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PSDV(\\d\\d\\.\\d)$",
    },
    "PSPB": {
        "name": "PSPB",
        "description": "Set Solar Power Balance",
        "help": " -- examples: PSPB0 (PV input max current will be the max charged current), PSPB1 (PV input max power will be the sum of the max charge power and loads power)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PSPB([01])$",
    },
    "PBATCD": {
        "name": "PBATCD",
        "description": "Battery charge/discharge controlling command",
        "help": " -- examples: PBATCDxxx (please read description, use carefully)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PBATCD([01][01][01])$",
    },
    "DAT": {
        "name": "DAT",
        "description": "Set Date Time",
        "help": " -- examples: DATYYYYMMDDHHMMSS (14 digits after DAT)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "DAT(\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d)$",
    },
    "PBATMAXDISC": {
        "name": "PBATMAXDISC",
        "description": "Battery max discharge current",
        "help": " -- examples: PBATMAXDISCxxx (000- disable or 030-150A)",
        "response_type": ResponseType.ACK,
        "response": [[1, "Command execution", "ack", {"NAK": "Failed", "ACK": "Successful"}],],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PBATMAXDISC([01]\\d\\d)$",
    },
}
QUERY_COMMANDS = {
    "Q1": {
        "name": "Q1",
        "description": "Q1 query",
        "response_type": ResponseType.INDEXED,
        "response": [
            [1, "Time until the end of absorb charging", "int", "sec"],
            [2, "Time until the end of float charging", "int", "sec"],
            [
                3,
                "SCC Flag",
                "option",
                ["SCC not communicating?", "SCC is powered and communicating"],
            ],
            [4, "AllowSccOnFlag", "bytes.decode", ""],
            [5, "ChargeAverageCurrent", "bytes.decode", ""],
            [6, "SCC PWM temperature", "int", "°C", {"device-class": "temperature"}],
            [7, "Inverter temperature", "int", "°C", {"device-class": "temperature"}],
            [8, "Battery temperature", "int", "°C", {"device-class": "temperature"}],
            [9, "Transformer temperature", "int", "°C", {"device-class": "temperature"}],
            [10, "GPIO13", "int", ""],
            [11, "Fan lock status", "option", ["Not locked", "Locked"]],
            [12, "Not used", "bytes.decode", ""],
            [13, "Fan PWM speed", "int", "%"],
            [14, "SCC charge power", "int", "W", {"icon": "mdi:solar-power", "device-class": "power"}],
            [15, "Parallel Warning", "bytes.decode", ""],
            [16, "Sync frequency", "float", ""],
            [
                17,
                "Inverter charge status",
                "str_keyed",
                {"10": "nocharging", "11": "bulk stage", "12": "absorb", "13": "float"},
                {"icon": "mdi:book-open"},
            ],
        ],
        "test_responses": [
            b"(00000 00000 01 01 00 059 045 053 068 00 00 000 0040 0580 0000 50.00 13\x39\xB9\r",
        ],
    },
    "QBOOT": {
        "name": "QBOOT",
        "description": "DSP Has Bootstrap inquiry",
        "response_type": ResponseType.INDEXED,
        "response": [[1, "DSP Has Bootstrap", "option", ["No", "Yes"]]],
        "test_responses": [
            b"(0\xb9\x1c\r",
        ],
    },
    "QDI": {
        "name": "QDI",
        "description": "Default Settings inquiry",
        "help": " -- queries the default settings from the Inverter",
        "response_type": ResponseType.INDEXED,
        "response": [
            [1, "AC Output Voltage", "float", "V"],
            [2, "AC Output Frequency", "float", "Hz"],
            [3, "Max AC Charging Current", "int", "A"],
            [4, "Battery Under Voltage", "float", "V"],
            [5, "Battery Float Charge Voltage", "float", "V"],
            [6, "Battery Bulk Charge Voltage", "float", "V"],
            [7, "Battery Recharge Voltage", "float", "V"],
            [8, "Max Charging Current", "int", "A"],
            [9, "Input Voltage Range", "option", ["Appliance", "UPS"]],
            [
                10,
                "Output Source Priority",
                "option",
                ["Utility first", "Solar first", "SBU first"],
            ],
            [
                11,
                "Charger Source Priority",
                "option",
                [
                    "Utility first",
                    "Solar first",
                    "Solar + Utility",
                    "Only solar charging permitted",
                ],
            ],
            [12, "Battery Type", "option", ["AGM", "Flooded", "User"]],
            [13, "Buzzer", "option", ["enabled", "disabled"]],
            [14, "Power saving", "option", ["disabled", "enabled"]],
            [15, "Overload restart", "option", ["disabled", "enabled"]],
            [16, "Over temperature restart", "option", ["disabled", "enabled"]],
            [17, "LCD Backlight", "option", ["disabled", "enabled"]],
            [18, "Primary source interrupt alarm", "option", ["disabled", "enabled"]],
            [19, "Record fault code", "option", ["disabled", "enabled"]],
            [20, "Overload bypass", "option", ["disabled", "enabled"]],
            [21, "LCD reset to default", "option", ["disabled", "enabled"]],
            [
                22,
                "Output mode",
                "option",
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
            [23, "Battery Redischarge Voltage", "float", "V"],
            [
                24,
                "PV OK condition",
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
            [26, "Unknown Value", "int", ""],
        ],
        "test_responses": [
            b"(230.0 50.0 0030 42.0 54.0 56.4 46.0 60 0 0 2 0 0 0 0 0 1 1 0 0 1 0 54.0 0 1 000\x9E\x60\r",
        ],
    },
    "QFLAG": {
        "name": "QFLAG",
        "description": "Flag Status inquiry",
        "help": " -- queries the enabled / disabled state of various Inverter settings (e.g. buzzer, overload, interrupt alarm)",
        "response_type": ResponseType.INDEXED,
        "response": [
            [
                1,
                "Device Status",
                "enflags",
                {
                    "a": {"name": "Buzzer", "state": "disabled"},
                    "b": {"name": "Overload Bypass", "state": "disabled"},
                    "j": {"name": "Power Saving", "state": "disabled"},
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
            b"(EakxyDbjuvz\x2F\x29\r",
        ],
    },
    "QID": {
        "name": "QID",
        "description": "Device Serial Number inquiry",
        "help": " -- queries the device serial number",
        "response_type": ResponseType.INDEXED,
        "response": [[1, "Serial Number", "bytes.decode", ""]],
        "test_responses": [
            b"(9293333010501\xBB\x07\r",
        ],
    },
    "QMCHGCR": {
        "name": "QMCHGCR",
        "description": "Max Charging Current Options inquiry",
        "help": " -- queries the maximum charging current setting of the Inverter",
        "response_type": ResponseType.MULTIVALUED,
        "response": [[1, "Max Charging Current Options", "string", "A"]],
        "test_responses": [
            b"(010 020 030 040 050 060 070 080 090 100 110 120\x0c\xcb\r",
        ],
    },
    "QMOD": {
        "name": "QMOD",
        "description": "Mode inquiry",
        "help": " -- queries the Inverter mode",
        "response_type": ResponseType.INDEXED,
        "response": [
            [
                1,
                "Device Mode",
                "str_keyed",
                {
                    "P": "Power on",
                    "S": "Standby",
                    "L": "Line",
                    "B": "Battery",
                    "F": "Fault",
                    "H": "Power saving",
                },
            ]
        ],
        "test_responses": [
            b"(S\xe5\xd9\r",
        ],
    },
    "QMN": {
        "name": "QMN",
        "description": "Model Name Inquiry",
        "response_type": ResponseType.INDEXED,
        "response": [[1, "Model Name", "bytes.decode", ""]],
        "test_responses": [
            b"(MKS2-8000\xb2\x8d\r",
        ],
    },
    "QGMN": {
        "name": "QGMN",
        "description": "General Model Name Inquiry",
        "response_type": ResponseType.INDEXED,
        "response": [[1, "General Model Number", "bytes.decode", ""]],
        "test_responses": [
            b"(044\xc8\xae\r",
        ],
    },
    "QMUCHGCR": {
        "name": "QMUCHGCR",
        "description": "Max Utility Charging Current Options inquiry",
        "help": " -- queries the maximum utility charging current setting of the Inverter",
        "response_type": ResponseType.MULTIVALUED,
        "response": [[1, "Max Utility Charging Current", "string", "A"]],
        "test_responses": [
            b"(002 010 020 030 040 050 060 070 080 090 100 110 120\xca#\r",
        ],
    },
    "QOPM": {
        "name": "QOPM",
        "description": "Output Mode inquiry",
        "help": " -- queries the output mode of the Inverter (e.g. single, parallel, phase 1 of 3 etc)",
        "response_type": ResponseType.INDEXED,
        "response": [
            [
                1,
                "Output mode",
                "option",
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
        "test_responses": [
            b"(0\xb9\x1c\r",
        ],
    },
    "QPGS": {
        "name": "QPGS",
        "description": "Parallel Information inquiry",
        "help": " -- example: QPGS1 queries the values of various metrics from instance 1 of parallel setup Inverters (numbers from 0)",
        "response_type": ResponseType.INDEXED,
        "response": [
            [1, "Parallel instance number", "option", ["Not valid", "valid"]],
            [2, "Serial number", "bytes.decode", ""],
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
            [5, "Grid voltage", "float", "V"],
            [6, "Grid frequency", "float", "Hz"],
            [7, "AC output voltage", "float", "V"],
            [8, "AC output frequency", "float", "Hz"],
            [9, "AC output apparent power", "int", "VA"],
            [10, "AC output active power", "int", "W"],
            [11, "Load percentage", "int", "%"],
            [12, "Battery voltage", "float", "V"],
            [13, "Battery charging current", "int", "A"],
            [14, "Battery capacity", "int", "%"],
            [15, "PV Input Voltage", "float", "V"],
            [16, "Total charging current", "int", "A"],
            [17, "Total AC output apparent power", "int", "VA"],
            [18, "Total output active power", "int", "W"],
            [19, "Total AC output percentage", "int", "%"],
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
                    "Phase 2 of 2 phase output",
                    "Unknown Output Mode",
                ],
            ],
            [
                22,
                "Charger source priority",
                "option",
                ["Utility first", "Solar first", "Solar + Utility", "Solar only"],
            ],
            [23, "Max charger current", "int", "A"],
            [24, "Max charger range", "int", "A"],
            [25, "Max AC charger current", "int", "A"],
            [26, "PV input current", "int", "A"],
            [27, "Battery discharge current", "int", "A"],
            [28, "Unknown float", ""],
            [29, "string", "Unknown flags?", ""],
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
        "response_type": ResponseType.INDEXED,
        "response": [
            [1, "Protocol ID", "bytes.decode", ""],
        ],
        "test_responses": [
            b"(PI30\x9a\x0b\r",
        ],
    },
    "QPIz": {
        "name": "QPIz",
        "description": "Protocol ID inquiry",
        "help": " -- queries the device protocol ID. e.g. PI30 for HS series",
        "response_type": ResponseType.INDEXED,
        "test_responses": [
            b"(PI30\x9a\x0b\r",
        ],
    },
    "QPIGS": {
        "name": "QPIGS",
        "description": "General Status Parameters inquiry",
        "help": " -- queries the value of various metrics from the Inverter",
        "response_type": ResponseType.INDEXED,
        "response": [
            [1, "AC Input Voltage", "float", "V", {"icon": "mdi:transmission-tower-export", "device-class": "voltage"}],
            [2, "AC Input Frequency", "float", "Hz", {"icon": "mdi:current-ac", "device-class": "frequency"}],
            [3, "AC Output Voltage", "float", "V", {"icon": "mdi:power-plug", "device-class": "voltage"}],
            [4, "AC Output Frequency", "float", "Hz", {"icon": "mdi:current-ac", "device-class": "frequency"}],
            [5, "AC Output Apparent Power", "int", "VA", {"icon": "mdi:power-plug", "device-class": "apparent_power"}],
            [6, "AC Output Active Power", "int", "W", {"icon": "mdi:power-plug", "device-class": "power", "state_class": "measurement"}],
            [7, "AC Output Load", "int", "%", {"icon": "mdi:brightness-percent"}],
            [8, "BUS Voltage", "int", "V", {"icon": "mdi:details", "device-class": "voltage"}],
            [9, "Battery Voltage", "float", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            [10, "Battery Charging Current", "int", "A", {"icon": "mdi:current-dc", "device-class": "current"}],
            [11, "Battery Capacity", "int", "%", {"device-class": "battery"}],
            [12, "Inverter Heat Sink Temperature", "int", "°C", {"icon": "mdi:details", "device-class": "temperature"}],
            [13, "PV Input Current", "float", "A", {"icon": "mdi:solar-power", "device-class": "current"}],
            [14, "PV Input Voltage", "float", "V", {"icon": "mdi:solar-power", "device-class": "voltage"}],
            [15, "Battery Voltage from SCC", "float", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            [16, "Battery Discharge Current", "int", "A", {"icon": "mdi:battery-negative", "device-class": "current"}],
            [
                17,
                "Device Status",
                "flags",
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
            [18, "RSV1", "int", "A"],
            [19, "RSV2", "int", "A"],
            [20, "PV Input Power", "int", "W", {"icon": "mdi:solar-power", "device-class": "power", "state_class": "measurement"}],
            [
                21,
                "Device Status2",
                "flags",
                ["Is Charging to Float", "Is Switched On", "Is Reserved"],
            ],
        ],
        "test_responses": [
            b"(000.0 00.0 230.0 49.9 0161 0119 003 460 57.50 012 100 0069 0014 103.8 57.45 00000 00110110 00 00 00856 010\x24\x8c\r",
        ],
    },
    "QPIRI": {
        "name": "QPIRI",
        "description": "Current Settings inquiry",
        "help": " -- queries the current settings from the Inverter",
        "response_type": ResponseType.INDEXED,
        "response": [
            [1, "AC Input Voltage", "float", "V"],
            [2, "AC Input Current", "float", "A"],
            [3, "AC Output Voltage", "float", "V"],
            [4, "AC Output Frequency", "float", "Hz"],
            [5, "AC Output Current", "float", "A"],
            [6, "AC Output Apparent Power", "int", "VA"],
            [7, "AC Output Active Power", "int", "W"],
            [8, "Battery Voltage", "float", "V"],
            [9, "Battery Recharge Voltage", "float", "V"],
            [10, "Battery Under Voltage", "float", "V"],
            [11, "Battery Bulk Charge Voltage", "float", "V"],
            [12, "Battery Float Charge Voltage", "float", "V"],
            [
                13,
                "Battery Type",
                "option",
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
            [14, "Max AC Charging Current", "int", "A"],
            [15, "Max Charging Current", "int", "A"],
            [16, "Input Voltage Range", "option", ["Appliance", "UPS"]],
            [
                17,
                "Output Source Priority",
                "option",
                ["Utility first", "Solar first", "SBU first"],
            ],
            [
                18,
                "Charger Source Priority",
                "option",
                [
                    "Utility first",
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
                    "Phase 2 of 2 phase output",
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
        ],
        "test_responses": [
            b"(230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10 010 1 0 0 6 01 0 0 54.0 0 1\x6F\x7E\r",
            b"(120.0 25.0 120.0 60.0 25.0 3000 3000 48.0 46.0 44.0 58.4 54.4 2 30 060 1 2 0 9 01 0 6 54.0 0 1 000 0\x8f\xed\r",
            b"(230.0 13.0 230.0 50.0 13.0 3000 2400 24.0 23.0 21.0 28.2 27.0 0 30 50 0 2 1 - 01 1 0 26.0 0 0\xb9\xbd\r",
            b"(230.0 21.7 230.0 50.0 21.7 5000 5000 48.0 47.0 46.5 57.6 57.6 5 30 080 0 1 2 1 01 0 0 52.0 0 1\x03$\r",
            b"(230.0 21.7 230.0 50.0 21.7 5000 5000 48.0 47.0 46.5 57.6 57.6 9 30 080 0 1 2 1 01 0 0 52.0 0 1\x9c\x6f\r",
            b"(230.0 34.7 230.0 50.0 34.7 8000 8000 48.0 48.0 42.0 54.0 52.5 2 010 030 1 2 2 9 01 0 0 50.0 0 1 480 0 070\xd9`\r",
        ],
    },
    "QPIWS": {
        "name": "QPIWS",
        "description": "Warning status inquiry",
        "help": " -- queries any active warnings flags from the Inverter",
        "response_type": ResponseType.INDEXED,
        "response": [
            [
                1,
                "Warning",
                "flags",
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
        "test_responses": [
            b"(00000100000000001000000000000000\x56\xA6\r",
        ],
    },
    "QVFW": {
        "name": "QVFW",
        "description": "Main CPU firmware version inquiry",
        "help": " -- queries the main CPU firmware version",
        "response_type": ResponseType.INDEXED,
        "response": [[1, "Main CPU firmware version", "bytes.decode", ""]],
        "test_responses": [
            b"(VERFW:00072.70\x53\xA7\r",
        ],
    },
    "QVFW2": {
        "name": "QVFW2",
        "description": "Secondary CPU firmware version inquiry",
        "help": " -- queries the secondary CPU firmware version",
        "response_type": ResponseType.INDEXED,
        "response": [[1, "Secondary CPU firmware version", "bytes.decode", ""]],
        "test_responses": [
            b"(VERFW:00072.70\x53\xA7\r",
        ],
    },
}


class pi30(AbstractProtocol):
    def __str__(self):
        return "PI30 protocol handler"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI30"
        self.COMMANDS = QUERY_COMMANDS
        self.COMMANDS.update(SETTER_COMMANDS)
        self.STATUS_COMMANDS = ["QPIGS", "Q1"]
        self.SETTINGS_COMMANDS = ["QPIRI", "QFLAG"]
        self.DEFAULT_COMMAND = "QPI"
        self.ID_COMMANDS = ["QPI", "QGMN", "QMN"]
        # log.info(f'Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands')

    def check_response_valid(self, result):
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
            result.error_messages.append(f"failed validity check: response to short len was {len(result.raw_response)}")
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
            result.error_messages.append(f"failed validity check: response has invalid CRC - got '\\x{crc_high:02x}\\x{crc_low:02x}', calculated '\\x{calc_crc_high:02x}\\x{calc_crc_low:02x}'")
            return
            # if result.raw_response[-3:-1] != bytes([calc_crc_high, calc_crc_low]):
        log.debug("CRCs match")
        return

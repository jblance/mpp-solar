""" pi30.py """
import logging

from mppsolar.protocols.protocol_helpers import crcPI as crc
from powermon.commands.reading_definition import ReadingType, ResponseType
# from powermon.commands.result import Result
from powermon.commands.result import ResultType
from powermon.protocols.abstractprotocol import AbstractProtocol

log = logging.getLogger("pi30")

SETTER_COMMANDS = {
    "F": {
        "name": "F",
        "description": "Set Device Output Frequency",
        "help": " -- examples: F50 (set output frequency to 50Hz) or F60 (set output frequency to 60Hz)",
        "result_type": ResultType.ACK,
        "reading_definitions": [{"description": "Command execution", "response_type": ResponseType.ACK, "options": {"NAK": "Failed", "ACK": "Successful"}, "reading_type": ReadingType.ACK}],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "F([56]0)$",
    },
    "MCHGC": {
        "name": "MCHGC",
        "description": "Set Max Charging Current (for parallel units)",
        "help": " -- examples: MCHGC040 (set unit 0 to max charging current of 40A), MCHGC160 (set unit 1 to max charging current of 60A)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "MCHGC(\\d\\d\\d)$",
    },
    "MNCHGC": {
        "name": "MNCHGC",
        "description": "Set Utility Max Charging Current (more than 100A) (for 4000/5000)",
        "help": " -- example: MNCHGC1120 (set unit 1 utility max charging current to 120A)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(ACK\x39\x20\r", b"(NAK\x73\x73\r"],
        "regex": "MNCHGC(\\d\\d\\d\\d)$",
    },
    "MUCHGC": {
        "name": "MUCHGC",
        "description": "Set Utility Max Charging Current",
        "help": " -- example: MUCHGC130 (set unit 1 utility max charging current to 30A)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "MUCHGC(\\d\\d\\d)$",
    },
    "PBCV": {
        "name": "PBCV",
        "description": "Set Battery re-charge voltage",
        "help": " -- example PBCV44.0 - set re-charge voltage to 44V (12V unit: 11V/11.3V/11.5V/11.8V/12V/12.3V/12.5V/12.8V, 24V unit: 22V/22.5V/23V/23.5V/24V/24.5V/25V/25.5V, 48V unit: 44V/45V/46V/47V/48V/49V/50V/51V)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "PBCV(\\d\\d\\.\\d)$",
    },
    "PBDV": {
        "name": "PBDV",
        "description": "Set Battery re-discharge voltage",
        "help": " -- example PBDV48.0 - set re-discharge voltage to 48V (12V unit: 00.0V/12V/12.3V/12.5V/12.8V/13V/13.3V/13.5V/13.8V/14V/14.3V/14.5, 24V unit: 00.0V/24V/24.5V/25V/25.5V/26V/26.5V/27V/27.5V/28V/28.5V/29V, 48V unit: 00.0V/48V/49V/50V/51V/52V/53V/54V/55V/56V/57V/58V, 00.0V means battery is full(charging in float mode).)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "PBDV(\\d\\d\\.\\d)$",
    },
    "PBFT": {
        "name": "PBFT",
        "description": "Set Battery Float Charging Voltage",
        "help": " -- example PBFT58.0 - set battery float charging voltage to 58V (48.0 - 58.4V for 48V unit)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "PBFT(\\d\\d\\.\\d)$",
    },
    "PBT": {
        "name": "PBT",
        "description": "Set Battery Type",
        "help": " -- examples: PBT00 (set battery as AGM), PBT01 (set battery as FLOODED), PBT02 (set battery as USER)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "PBT(0[012])$",
    },
    "PCP": {
        "name": "PCP",
        "description": "Set Device Charger Priority",
        "help": " -- examples: PCP00 (set utility first), PCP01 (set solar first), PCP02 (HS only: set solar and utility), PCP03 (set solar only charging)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "PCP(0[0123])$",
    },
    "PCVV": {
        "name": "PCVV",
        "description": "Set Battery C.V. (constant voltage) charging voltage",
        "help": " -- example PCVV48.0 - set charging voltage to 48V (48.0 - 58.4V for 48V unit)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "PCVV(\\d\\d\\.\\d)$",
    },
    "PE": {
        "name": "PE",
        "description": "Set the enabled state of an Inverter setting",
        "help": " -- examples: PEa - enable a (buzzer) [a=buzzer, b=overload bypass, j=power saving, K=LCD go to default after 1min, u=overload restart, v=overtemp restart, x=backlight, y=alarm on primary source interrupt, z=fault code record]",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "PE(.+)$",
    },
    "PD": {
        "name": "PD",
        "description": "Set the disabled state of an Inverter setting",
        "help": " -- examples: PDa - disable a (buzzer) [a=buzzer, b=overload bypass, j=power saving, K=LCD go to default after 1min, u=overload restart, v=overtemp restart, x=backlight, y=alarm on primary source interrupt, z=fault code record]",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
        "regex": "PD(.+)$",
    },
    "PF": {
        "name": "PF",
        "description": "Set Control Parameters to Default Values",
        "help": " -- example PF (reset control parameters to defaults)",
        "response_type": ResultType.ACK,
        "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
    },
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
    "QMCHGCR": {
        "name": "QMCHGCR",
        "description": "Max Charging Current Options inquiry",
        "help": " -- queries the maximum charging current setting of the Inverter",
        "response_type": ResultType.MULTIVALUED,
        "response": [{"index": 0, "description": "Max Charging Current Options", "reading_type": ReadingType.AMPS, "response_type": ResponseType.STRING}],
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
                ResponseType.OPTION,
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
                ResponseType.OPTION,
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
                ResponseType.OPTION,
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
    "QPIz": {  # Question: is this a typo? Duplicate of QPI?
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
    "QPIRI": {
        "name": "QPIRI",
        "description": "Current Settings inquiry",
        "help": " -- queries the current settings from the Inverter",
        "response_type": ResultType.INDEXED,
        "response": [
            [0, "AC Input Voltage", ResponseType.FLOAT, "V"],
            [1, "AC Input Current", ResponseType.FLOAT, "A"],
            [2, "AC Output Voltage", ResponseType.FLOAT, "V"],
            [3, "AC Output Frequency", ResponseType.FLOAT, "Hz"],
            [4, "AC Output Current", ResponseType.FLOAT, "A"],
            [5, "AC Output Apparent Power", ResponseType.INT, "VA"],
            [6, "AC Output Active Power", ResponseType.INT, "W"],
            [7, "Battery Voltage", ResponseType.FLOAT, "V"],
            [8, "Battery Recharge Voltage", ResponseType.FLOAT, "V"],
            [9, "Battery Under Voltage", ResponseType.FLOAT, "V"],
            [10, "Battery Bulk Charge Voltage", ResponseType.FLOAT, "V"],
            [11, "Battery Float Charge Voltage", ResponseType.FLOAT, "V"],
            [
                12,
                "Battery Type",
                ResponseType.OPTION,
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
            [13, "Max AC Charging Current", ResponseType.INT, "A"],
            [14, "Max Charging Current", ResponseType.INT, "A"],
            [15, "Input Voltage Range", ResponseType.OPTION, ["Appliance", "UPS"]],
            [16, "Output Source Priority", ResponseType.OPTION, ["Utility first", "Solar first", "SBU first"]],
            [
                17,
                "Charger Source Priority",
                ResponseType.OPTION,
                ["Utility first", "Solar first", "Solar + Utility", "Only solar charging permitted"],
            ],
            [18, "Max Parallel Units", ResponseType.INT, "units"],
            [19, "Machine Type", ResponseType.OPTION, {"00": "Grid tie", "01": "Off Grid", "10": "Hybrid"}],
            [20, "Topology", ResponseType.OPTION, ["transformerless", "transformer"]],
            [
                21,
                "Output Mode",
                ResponseType.OPTION,
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
            [22, "Battery Redischarge Voltage", ResponseType.FLOAT, "V"],
            [
                23,
                "PV OK Condition",
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
            [25, "Max charging time for CV stage", ResponseType.INT, "min"],
            [26, "Operation Logic", ResponseType.OPTION, ["Automatic mode", "On-line mode", "ECO mode"]],
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

NEW_FORMAT_COMMANDS = {
    "QID": {
        "name": "QID",
        "description": "Device Serial Number inquiry",
        "help": " -- queries the device serial number",
        "result_type": ResultType.SINGLE,
        "reading_definitions": [{"description": "Serial Number", "reading_type": ReadingType.MESSAGE, "response_type": ResponseType.STRING}],
        "test_responses": [b"(9293333010501\xbb\x07\r"],
    },
    "Q1": {
        "name": "Q1",
        "description": "Q1 query",
        "result_type": ResultType.INDEXED,
        "reading_definitions": [
            {"index": 0, "reading_type": ReadingType.TIME, "response_type": ResponseType.INT, "description": "Time until the end of absorb charging"},
            {"index": 1, "reading_type": ReadingType.TIME, "response_type": ResponseType.INT, "description": "Time until the end of float charging"},
            {"index": 2, "reading_type": ReadingType.MESSAGE, "response_type": ResponseType.OPTION, "description": "SCC Flag", "options": {"00": "SCC not communicating?", "01": "SCC is powered and communicating", "11": "I am probably decoding wrong, should this be a 3?"}},
            {"index": 3, "reading_type": ReadingType.MESSAGE, "response_type": ResponseType.OPTION, "description": "AllowSccOnFlag", "options": {"00": "SCC not allowed to charge", "01": "SCC allowed to charge"}},
            {"index": 4, "reading_type": ReadingType.AMPERAGE, "response_type": ResponseType.INT, "description": "ChargeAverageCurrent"},
            {"index": 5, "reading_type": ReadingType.TEMPERATURE, "response_type": ResponseType.INT, "description": "SCC PWM temperature", "device-class": "temperature"},
            {"index": 6, "reading_type": ReadingType.TEMPERATURE, "response_type": ResponseType.INT, "description": "Inverter temperature", "device-class": "temperature"},
            {"index": 7, "reading_type": ReadingType.TEMPERATURE, "response_type": ResponseType.INT, "description": "Battery temperature", "device-class": "temperature"},
            {"index": 8, "reading_type": ReadingType.TEMPERATURE, "response_type": ResponseType.INT, "description": "Transformer temperature", "device-class": "temperature"},
            {"index": 9, "reading_type": ReadingType.MESSAGE, "response_type": ResponseType.OPTION, "description": "Parallel Mode", "options": {"00": "New", "01": "Slave", "02": "Master"}},
            {"index": 10, "reading_type": ReadingType.MESSAGE, "response_type": ResponseType.OPTION, "description": "Fan lock status", "options": {"00": "Not locked", "01": "Locked"}},
            {"index": 11, "reading_type": ReadingType.MESSAGE, "response_type": ResponseType.BYTES, "description": "Not used"},
            {"index": 12, "reading_type": ReadingType.PERCENTAGE, "response_type": ResponseType.INT, "description": "Fan PWM speed"},
            {"index": 13, "reading_type": ReadingType.WATTS, "response_type": ResponseType.INT, "description": "SCC charge power", "icon": "mdi:solar-power", "device-class": "power"},
            {"index": 14, "reading_type": ReadingType.MESSAGE, "response_type": ResponseType.BYTES, "description": "Parallel Warning"},
            {"index": 15, "reading_type": ReadingType.FREQUENCY, "response_type": ResponseType.FLOAT, "description": "Sync frequency"},
            {"index": 16,
                "description": "Inverter charge status",
                "reading_type": ReadingType.MESSAGE,
                "response_type": ResponseType.OPTION,
                "options": {"10": "nocharging", "11": "bulk stage", "12": "absorb", "13": "float"},
                "icon": "mdi:book-open", },
        ],
        "test_responses": [b"(00000 00000 01 01 00 059 045 053 068 00 00 000 0040 0580 0000 50.00 139\xb9\r"],
    },
}


class PI30(AbstractProtocol):
    """ pi30 protocol handler """
    def __str__(self):
        return "PI30 protocol handler"

    def __init__(self) -> None:
        super().__init__()
        self._protocol_id = b"PI30"
        self.add_command_definitions(NEW_FORMAT_COMMANDS)
        self.STATUS_COMMANDS = ["QPIGS", "Q1"]
        self.SETTINGS_COMMANDS = ["QPIRI", "QFLAG"]
        self.DEFAULT_COMMAND = "QPI"
        self.ID_COMMANDS = ["QPI", "QGMN", "QMN"]
        self.check_definitions_count()

    def check_crc(self, response: str):
        """ crc check, needs override in protocol """
        log.debug("check crc for %s in pi30", response)
        # check crc matches the calculated one
        calc_crc_high, calc_crc_low = crc(response[:-3])
        crc_high, crc_low = response[-3], response[-2]
        if [calc_crc_high, calc_crc_low] != [crc_high, crc_low]:
            raise ValueError(f"response has invalid CRC - got '\\x{crc_high:02x}\\x{crc_low:02x}', \
                calculated '\\x{calc_crc_high:02x}\\x{calc_crc_low:02x}'")
        log.debug("CRCs match")

    # def check_response_and_trim(self, response: str):
    #     # fail if no response
    #     if response is None:
    #         result.is_valid = False
    #         result.error = True
    #         result.error_messages.append("failed validity check: response was empty")
    #         return
    #     # fail on short responses
    #     if len(result.raw_response) <= 3:
    #         result.is_valid = False
    #         result.error = True
    #         result.error_messages.append(
    #             f"failed validity check: response to short len was {len(result.raw_response)}"
    #         )
    #         return
    #     # check crc matches the calculated one
    #     calc_crc_high, calc_crc_low = crc(result.raw_response[:-3])
    #     if type(result.raw_response) is str:
    #         crc_high, crc_low = ord(result.raw_response[-3]), ord(result.raw_response[-2])
    #     else:
    #         crc_high, crc_low = result.raw_response[-3], result.raw_response[-2]
    #     if [calc_crc_high, calc_crc_low] != [crc_high, crc_low]:
    #         result.is_valid = False
    #         result.error = True
    #         result.error_messages.append(
    #             f"failed validity check: response has invalid CRC - \
    #                 got '\\x{crc_high:02x}\\x{crc_low:02x}', \
    #                 calculated '\\x{calc_crc_high:02x}\\x{calc_crc_low:02x}'"
    #         )
    #         return
    #         # if result.raw_response[-3:-1] != bytes([calc_crc_high, calc_crc_low]):
    #     log.debug("CRCs match")
    #     return

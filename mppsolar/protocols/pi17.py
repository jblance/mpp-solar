import logging

from .abstractprotocol import AbstractProtocol
from ..helpers import CRC_XModem

from typing import Tuple

log = logging.getLogger("pi17")

QUERY_COMMANDS = {
    "GPMP": {
        "name": "GPMP",
        "prefix": "^P005",
        "description": "Query the maximum output power for feeding grid",
        "help": " -- queries Query the maximum output power for feeding grid",
        "type": "QUERY",
        "response": [
            ["int", "Maximum Feeding Grid power", "W"],
        ],
        "test_responses": [
            b'^D00815000\xe1\xa1\r',
        ]
    },
    "PI": {
        "name": "PI",
        "prefix": "^P003",
        "description": "Device Protocol Version inquiry",
        "help": " -- queries the device protocol version",
        "type": "QUERY",
        "response": [["string", "Protocol Version", ""]],
        "test_responses": [
            b"^D00517\xca\xec\r",
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
            b"^D0251496161704100242000000le\r",
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
            b"^D017VERFW:00001.01VW\r",
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
            b"^D018VERFW2:00001.01\x99\xc3\r",
        ],
    },
    "MD": {
        "name": "MD",
        "prefix": "^P003",
        "description": "Device Model inquiry",
        "help": " -- queries the device model",
        "response_type" : "SEQUENTIAL",
        "type": "QUERY",
        "response": [
            [
                "str_keyed",
                "Machine number",
                {
                    "000": "Infini-Solar 10KW/3P",
                    "001": "Infini-Solar 15KW/3P",
                    "002": "Infini-Solar 15KW/3P-custom",
                    "003": "Infini-Solar WP (Infini WP 12K/15K)",
                    "004": "Infini-Solar WP 30KW/3P",
                    "005": "Infini-Solar WP LV 6KW/2P",
                    "006": "Infini-Solar WP TWIN",
                },
            ],
            ["int", "Output rated VA", "kW"],
            ["int", "Output power factor", "pf"],
            ["int", "AC input phase number", "number"],
            ["int", "AC output phase number", "number"],
            ["int:r/10", "Norminal AC output voltage", "V"],
            ["int:r/10", "Norminal AC input voltage", "V"],
            ["int", "Battery piece number", "ea"],
            ["int:r/10", "Battery standard voltage per unit", "V"],
        ],
        "test_responses": [
            b"^D037000,010000,99,3,3,2300,2300,04,120U\x82\r",
        ],
    },
    "DI": {
        "name": "DI",
        "prefix": "^P003",
        "description": "Query default value of changeable parameters",
        "help": "",
        "type": "QUERY",
        "response": [
            ["int:r/10", "AC input highest voltage for feed power", "V"],
            ["int:r/10", "AC input lowest voltage for feed power", "V"],
            ["int:r/100", "AC input highest frequency for feed power", "Hz"],
            ["int:r/100", "AC input lowest frequency for feed power", "Hz"],
            ["int:r/10", "Solar input highest MPPT voltage", "V"],
            ["int:r/10", "Solar input lowest MPPT voltage", "V"],
            ["int:r/10", "Solar input highest voltage", "V"],
            ["int:r/10", "Solar input lowest voltage", "V"],
            ["int:r/10", "Solar input highest average voltage", "V"],
            ["int:r*30", "LCD sleep wait time", "s", {"device-class":"duration"}],
            ["int:r/10", "Battery maximum charge current", "A"],
            ["int:r/10", "Battery constant charge voltage CV", "V"],
            ["int:r/10", "Battery float charge voltage", "V"],
            ["int", "The wait time for feed power", "s", {"device-class":"duration"}],
            ["string", "Start time for support loads", "HHMM"],
            ["string", "Ending time for support loads", "HHMM"],
            ["string", "Start time for AC charger", "HHMM"],
            ["string", "Ending time for AC charger", "HHMM"],
            ["int:r/10", "Battery under voltage", "V"],
            ["int:r/10", "Battery under back voltage", "V"],
            ["int:r/10", "Battery weak voltage in hybrid mode", "V"],
            ["int:r/10", "Battery weak back voltage in hybrid mode", "V"],
            ["int:r/10", "Battery stop charge current level in floating charging", "A"],
            ["int:r/10", "Keep charged time of battery catch stop charger current level", "A"],
            ["int:r/10", "Battery voltage of recover to charge when battery stop charger in floating charging", "V"],
        ],
        "test_responses": [],
    },
    "DM": {
        "name": "DM",
        "prefix": "^P003",
        "description": "Query machine model",
        "help": "For outputs interpretation see documentations",
        "type": "QUERY",
        "response": [["string", "model_code", ""]],
        "test_responses": [b"^D006050h\xdb\r"],
    },
    "INGS": {
        "name": "INGS",
        "prefix": "^P004",
        "description": "",
        "help": "",
        "response_type": "SEQUENTIAL",
        "type": "QUERY",
        "response": [
            ["int:r/10", "Input current R", "A"],
            ["int:r/10", "Input current S", "A"],
            ["int:r/10", "Input current T", "A"],
            ["int:r/10", "Output current R", "A"],
            ["int:r/10", "Output current S", "A"],
            ["int:r/10", "Output current T", "A"],
            ["int:r/10", "PBusVolt", "V"],
            ["int:r/10", "NBusVolt", "V"],
            ["int:r/10", "PBusAvgV", "V"],
            ["int:r/10", "NBusAvgV", "V"],
            ["int:r/10", "NLintCur", "A"],
        ],
        "test_responses": [b"^D0560020,0019,0021,0002,0004,0005,3809,3809,3810,3807,000\xf1\x1e\r"],
    },
    "EMINFO": {
        "name": "EMINFO",
        "prefix": "^P005",
        "description": "",
        "help": "",
        "type": "QUERY",
        "response": [
            ["int", "EMFirst", ""],
            ["int", "DefFeed-InPow", ""],
            ["int", "ActPvPow", ""],
            ["int", "ActFeedPow", ""],
            ["int", "ReservPow", ""],
            ["int", "EMLast", ""],
        ],
        "test_responses": [b"^D0301,10000,00005,00010,00000,1\xad\xc4\r"],
    },
    "PIRI": {
        "name": "PIRI",
        "prefix": "^P005",
        "description": "Device rated information",
        "help": " -- queries rated information",
        "response_type": "SEQUENTIAL",
        "type": "QUERY",
        "response": [
            ["int:r/10", "AC input rated voltage", "V"],
            ["int:r/10", "AC input rated frequency", "Hz"],
            ["int:r/10", "AC input rated current", "A"],
            ["int:r/10", "AC output rated voltage", "V"],
            ["int:r/10", "AC output rated current", "A"],
            ["int:r/10", "MPPT rated current per string", "A"],
            ["int:r/10", "Battery rated voltage", "V"],
            ["int", "MPPT track number", "ea"],
            [
                "str_keyed",
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
            b"^D0452400,500,0416,2400,0416,0187,0480,2,10,0,1\xbcs\r",
        ],
    },
    "GS": {
        "name": "GS",
        "prefix": "^P003",
        "description": "Query general status",
        "help": " -- queries general status",
        "response_type": "SEQUENTIAL",
        "type": "QUERY",
        "response": [
            ["int:r/10", "Solar input voltage 1", "V"], 
            ["int:r/10", "Solar input voltage 2", "V"],
            ["int:r/100", "Solar input current 1", "A"],
            ["int:r/100", "Solar input current 2", "A"],
            ["int:r/10", "Battery voltage", "V"],
            ["int", "Battery capacity", "%", {"device-class": "battery"}],
            ["int:r/10", "Battery current", "A"],
            ["int:r/10", "AC input voltage R", "V"],
            ["int:r/10", "AC input voltage S", "V"],
            ["int:r/10", "AC input voltage T", "V"],
            ["int:r/100", "AC input frequency", "Hz"],
            ["int:r/10", "AC input current R", "A"],
            ["int:r/10", "AC input current S", "A"],
            ["int:r/10", "AC input current T", "A"],
            ["int:r/10", "AC output voltage R", "V"],
            ["int:r/10", "AC output voltage S", "V"],
            ["int:r/10", "AC output voltage T", "V"],
            ["int:r/100", "AC output frequency", "Hz"],
            ["int:r/10", "AC output current R", "A"],
            ["int:r/10", "AC output current S", "A"],
            ["int:r/10", "AC output current T", "A"],
            ["int", "Inner temperature", "°C", {"device-class": "temperature"}],
            ["int", "Component max temperature", "°C", {"device-class": "temperature"}],
            ["int", "External Battery temperature", "°C", {"device-class": "temperature"}],
            [
                "option",
                "Setting change bit",
                ["No setting change", "Settings changed - please refresh"],
            ],
        ],
        "test_responses": [
            b"^D1100000,0000,0000,0000,0394,000,+00000,2389,2427,2459,5002,0000,0000,0000,2378,2434,2455,5001,,,,029,029,000,0\xf8n\r",
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
            ["int", "AC output apparent power R", "VA", {"device-class":"apparent_power"}],
            ["int", "AC output apparent power S", "VA", {"device-class":"apparent_power"}],
            ["int", "AC output apparent power T", "VA", {"device-class":"apparent_power"}],
            ["int", "AC output total apparent power", "VA", {"device-class":"apparent_power"}],
            ["int", "AC output power percentage", "%", {"device-class":"power_factor"}],
            ["option", "AC output connect status", ["Disconnected", "Connected"]],
            ["option", "Solar input 1 work status", ["Idle", "Working"]],
            ["option", "Solar input 2 work status", ["Idle", "Working"]],
            ["option", "Battery power direction", ["Idle", "Charging", "Discharging"]],
            ["option", "DC/AC power direction", ["Idle", "AC to DC", "DC to AC"]],
            ["option", "Line power direction", ["Idle", "Input", "Output"]],
        ],
        "test_responses": [
            b'^D10100263,00381,,-00855,-03141,-03156,-07152,0000,0000,0000,00000,0193,0147,0195,00535,003,1,1,1,2,2,12\x1c\r'
            b'^D10100271,00381,,-00756,-02491,-02401,-05648,0000,0000,0000,00000,0193,0147,0194,00534,003,1,1,1,2,2,1:\xe9\r'
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
            b"^D00505\xd9\x9f\r",
        ],
    },
    "WS": {
        "name": "WS",
        "prefix": "^P003",
        "description": "Warning status inquiry",
        "help": " -- queries any active warnings flags from the Inverter",
        "type": "QUERY",
        "response": [
            ["option", "Solar input 1 loss", ["disabled", "enabled"]],
            ["option", "Solar input 2 loss", ["disabled", "enabled"]],
            ["option", "Solar input 1 voltage too high", ["disabled", "enabled"]],
            ["option", "Solar input 2 voltage too high", ["disabled", "enabled"]],
            ["option", "Battery under voltage", ["disabled", "enabled"]],
            ["option", "Battery low voltage", ["disabled", "enabled"]],
            ["option", "Battery disconnected", ["disabled", "enabled"]],
            ["option", "Battery over voltage", ["disabled", "enabled"]],
            ["option", "Battery low in hybrid mode", ["disabled", "enabled"]],
            ["option", "Grid voltage high loss", ["disabled", "enabled"]],
            ["option", "Grid voltage low loss", ["disabled", "enabled"]],
            ["option", "Grid frequency high loss", ["disabled", "enabled"]],
            ["option", "Grid frequency low loss", ["disabled", "enabled"]],
            ["option", "AC input long-time average voltage over", ["disabled", "enabled"]],
            ["option", "AC input voltage loss", ["disabled", "enabled"]],
            ["option", "AC input frequency loss", ["disabled", "enabled"]],
            ["option", "AC input island", ["disabled", "enabled"]],
            ["option", "AC input phase dislocation", ["disabled", "enabled"]],
            ["option", "Over temperature", ["disabled", "enabled"]],
            ["option", "Over load", ["disabled", "enabled"]],
            ["option", "Emergency Power Off active", ["disabled", "enabled"]],
            ["option", "AC input wave loss", ["disabled", "enabled"]],
        ],
        "test_responses": [
            b"^D0471,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,\x14\x9c\r",
        ],
    },
    "FLAG": {
        "name": "FLAG",
        "prefix": "^P005",
        "description": "Query enable/disable flag status",
        "help": " -- queries enable/disable flag status from the Inverter",
        "type": "QUERY",
        "response": [
            ["option", "Mute buzzer beep", ["Disabled", "Enabled"]],
            ["option", "Mute buzzer beep in standby mode", ["Disabled", "Enabled"]],
            [
                "option",
                "Mute buzzer beep only on battery discharged status",
                ["Disabled", "Enabled"],
            ],
            ["option", "Generator as AC input", ["Disabled", "Enabled"]],
            ["option", "Wide AC input range", ["Disabled", "Enabled"]],
            ["option", "N/G relay function", ["Disabled", "Enabled"]],
        ],
        "test_responses": [
            b"^D0120,0,1,0,1\xd8\xf2\r",
        ],
    },
    "T": {
        "name": "T",
        "prefix": "^P002",
        "description": "Query current time",
        "help": " -- queries current time from the Inverter",
        "type": "QUERY",
        "response": [
            ["string", "DateTime", "YYYYMMDDHHMMSS"],
        ],
        "test_responses": [
            b"^D01720210521234743\x0dR\r",
        ],
    },
    "ET": {
        "name": "ET",
        "prefix": "^P003",
        "description": "Query total generated energy",
        "help": " -- queries total generated energy from the Inverter",
        "type": "QUERY",
        "response": [
            [
                "int",
                "Generated Energy Total",
                "kWh",
                {"icon": "mdi:counter", "device-class": "energy", "state_class": "total"},
            ],
        ],
        "test_responses": [
            b"^D01100006591\xba\x10\r",
        ],
    },
    "BATS": {
        "name": "BATS",
        "description": "Query battery setting",
        "help": " -- queries battery setting",
        "response_type": "SEQUENTIAL",
        "type": "QUERY",
        "response": [
            ["int:r/10", "Battery maximum charge current", "A"],
            ["int:r/10", "Battery constant charge voltage(C.V.)", "V"],
            ["int:r/10", "Battery floating charge voltage", "V"],
            ["int:r/10", "Battery stop charger current level in floating charging", "A"],
            [
                "int",
                "Keep charged time of battery catch stopped charging current level",
                "Minutes",
            ],
            [
                "int:r/10",
                "Battery voltage of recover to charge when battery stop charger in floating charging",
                "V"
            ],
            ["int:r/10", "Battery under voltage", "V"],
            ["int:r/10", "Battery under voltage release", "V"],
            ["int:r/10", "Battery weak voltage in hybrid mode", "V"],
            ["int:r/10", "Battery weak voltage release in hybrid mode", "V"],
            ["option", "Battery Type", ["Ordinary", "Li-Fe"]],
            ["string", "Reserved", ""],
            ["string", "Battery install date", "YYYYMMDDHHMMSS"],
            [
                "option",
                "AC charger keep battery voltage function enable/diable",
                ["Disabled", "Enabled"],
            ],
            ["int:r/10", "AC charger keep battery voltage", "V"],
            ["int:r/10", "Battery temperature sensor compensation", "mV"],
            ["int:r/10", "Max. AC charging current", "A"],
            ["int", "Battery discharge max current in hybrid mode", "A"],
            ["option", "Enable/Disable EPS function", ["Disabled", "Enabled"]],
            ["int:r/10", "Battery voltage of cut-off Main output in battery mode", "V"],
            ["int:r/10", "Battery voltage of re-connecting Main output in battery mode", "V" ],
        ],
        "test_responses": [
            b"^D0762000,0584,0576,0000,000,0576,0460,0510,0460,0510,1,,,1,0540,000,2000,0250\x85Y\r",
            b"^D0941750,0560,0540,0000,060,0530,0420,0480,0480,0540,0,,,0,0480,000,0100,0175,000,000,000,000,0\xc9\xd9\r",
            b"^D0941750,0560,0540,0000,060,0530,0420,0480,0480,0540,0,,,0,0480,000,0100,0175,010,020,020,080,0mr\r",
        ],
    },
    "HECS": {
        "name": "HECS",
        "prefix": "^P005",
        "description": "Query energy control status",
        "help": " -- queries the device energy distribution",
        "response_type": "SEQUENTIAL",
        "type": "QUERY",
        "response": [
            [
                "str_keyed",
                "Solar Energy Distribution Priority",
                {
                    "00": "Battery-Load-Grid",
                    "01": "Load-Battery-Grid",
                    "02": "Load-Grid-Battery",
                },
            ],
            ["option", "Solar charge battery", ["disabled", "enabled"]],
            ["option", "AC charge battery", ["disabled", "enabled"]],
            ["option", "Feed power to utility", ["disabled", "enabled"]],
            ["option", "Battery discharge to loads when solar input normal", ["disabled", "enabled"]],
            ["option", "Battery discharge to loads when solar input loss", ["disabled", "enabled"]],
            ["option", "Battery discharge to feed grid when solar input normal", ["disabled", "enabled"]],
            ["option", "Battery discharge to feed grid when solar input loss", ["disabled", "enabled"]],
            ["exclude", "Reserved", ["disabled", "enabled"]],
        ],
        "test_responses": [
            b"^D01900,0,0,0,0,0,0,0,0\x35\xfc\r",
        ],
    },
    "EY": {
        "name": "EY",
        "prefix": "^P010",
        "description": "Query generated energy of year",
        "help": " -- queries generated energy for the year YYYY from the Inverter",
        "type": "QUERYEN",
        "response": [
            ["int", "Generated Energy Year", "Wh"],
        ],
        "test_responses": [
            b"^D01100006591\xba\x10\r",
        ],
        "regex": "EY(\\d\\d\\d\\d)$",
    },
    "EM": {
        "name": "EM",
        "prefix": "^P012",
        "description": "Query generated energy of month",
        "help": " -- queries generated energy for the month YYYYMM from the Inverter",
        "type": "QUERYEN",
        "response": [
            ["int", "Generated Energy Month", "Wh"],
        ],
        "test_responses": [
            b"^D01000006591\x51\x33\r",
        ],
        "regex": "EM(\\d\\d\\d\\d\\d\\d)$",
    },
    "ED": {
        "name": "ED",
        "prefix": "^P014",
        "description": "Query generated energy of day",
        "help": " -- queries generated energy for the day YYYYMMDD from the Inverter",
        "type": "QUERYEN",
        "response": [
            ["int", "Generated Energy Day", "Wh"],
        ],
        "test_responses": [
            b"^D009000091\x0e\x73\r",
        ],
        "regex": "ED(\\d\\d\\d\\d\\d\\d\\d\\d)$",
    },
    "EH": {
        "name": "EH",
        "prefix": "^P016",
        "description": "Query generated energy of hour",
        "help": " -- queries generated energy for the hour YYYYMMDDHH from the Inverter",
        "type": "QUERYEN",
        "response": [
            ["int", "Generated Energy Hour", "Wh"],
        ],
        "test_responses": [
            b"^D008000001\x0c\x8a\r",
        ],
        "regex": "EH(\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d)$",
    },
}

SETTER_COMMANDS = {
    "GPMP0": {
        "name": "GPMP0",
        "description": "Set max power of feeding grid",
        "help": " -- examples: GPMP0nnnnn (n: 0~9, unit: W, 0-15000W for 15KW converter)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "GPMP(0[10]\d\d\d\d)$",
    },
    "LON": {
        "name": "LON",
        "description": "Set enable/disable machine supply power to the loads",
        "help": " -- examples: LON1 (0: disable, 1: enable)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "LON([01])$",
    },
    "PA": {
        "name": "PA",
        "description": "Mute buzzer beep",
        "help": " -- examples: PA1 (1: enable, 0: disable)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "PA([01])$",
    },
    "PB": {
        "name": "PB",
        "description": "Mute buzzer beep in standby mode",
        "help": " -- examples: PB1 (1: enable, 0: disable)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "PB([01])$",
    },
    "PC": {
        "name": "PC",
        "description": "Mute buzzer beep only on battery discharged status",
        "help": " -- examples: PC1 (1: enable, 0: disable)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "PC([01])$",
    },
    "PD": {
        "name": "PD",
        "description": "Generator as AC input",
        "help": " -- examples: PD1 (1: enable, 0: disable)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "PD([01])$",
    },
    "PE": {
        "name": "PE",
        "description": "Wide AC input range",
        "help": " -- examples: PE1 (1: enable, 0: disable)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "PE([01])$",
    },
    "PF": {
        "name": "PF",
        "description": "N/G relay function",
        "help": " -- examples: PF1 (1: enable, 0: disable)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "PF([01])$",
    },
    "DAT": {
        "name": "DAT",
        "description": "Set date time",
        "help": " -- examples: DAT190518224530(YYMMDDHHMMSS-12digits)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "DAT(\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d)$",
    },
    "LST": {
        "name": "LST",
        "description": "Set LCD sleep wait time",
        "help": " -- examples: LSTnn (nn: 00, 01, 02, 10, 20 for selection, unit : 30second.00 means LCD always light)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "LST((0[123])|([12]0))$",
    },
    "EDA": {
        "name": "EDA",
        "description": "Enable/disable solar charge battery",
        "help": " -- examples: EDA1 (1: enable, 0: disable)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "EDA([01])$",
    },
    "EDB": {
        "name": "EDB",
        "description": "Enable/disable AC charge battery",
        "help": " -- examples: EDB1 (1: enable, 0: disable)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "EDB([01])$",
    },
    "EDC": {
        "name": "EDC",
        "description": "Enable/disable feed power to utility",
        "help": " -- examples: EDC1 (1: enable, 0: disable)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "EDC([01])$",
    },
    "EDD": {
        "name": "EDD",
        "description": "Enable/disable battery discharge to loads when solar input normal",
        "help": " -- examples: EDD1 (1: enable, 0: disable)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "EDD([01])$",
    },
    "EDE": {
        "name": "EDE",
        "description": "Enable/disable battery discharge to loads when solar input loss",
        "help": " -- examples: EDE1 (1: enable, 0: disable)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "EDE([01])$",
    },
    "EDF": {
        "name": "EDF",
        "description": "Enable/disable battery discharge to feed power to utility when solar input normal",
        "help": " -- examples: EDF1 (1: enable, 0: disable)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "EDF([01])$",
    },
    "EDG": {
        "name": "EDG",
        "description": "Enable/disable battery discharge to feed power to utility whensolar input loss",
        "help": " -- examples: EDG1 (1: enable, 0: disable)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "EDG([01])$",
    },
    "BT": {
        "name": "BT",
        "description": "Set battery type",
        "help": " -- examples: EDG1 (1: Li-Fe, 0: Ordinary)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "BT([01])$",
    },
    "MCHGV": {
        "name": "MCHGV",
        "description": "Set battery charge voltages",
        "help": " -- examples: MCHGV0576,0566 (CV voltage in 0.1V xxxx, Float voltage xxxx in 0.1V)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "MCHGV(0[45]\\d\\d,0[45]\\d\\d)$",
    },
    "ACCT": {
        "name": "ACCT",
        "description": "Set AC charge time range",
        "help": " -- examples: ACCT2200-0259 (Sets time range from 22:00 to 02:59. End minute is inclusive)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "ACCT((2[0-3]|[01]?[0-9])([0-5]?[0-9])-(2[0-3]|[01]?[0-9])([0-5]?[0-9]))$",
    },
    "ACCB": {
        "name": "ACCB",
        "description": "AC Charger  keep  battery voltage",
        "help": " -- examples: ACCB1,0450 (1: enable, 0: disable),(400-600) 0.1V",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "ACCB([01],0[456]\\d\\d)$",
    },
    "MCHGC": {
        "name": "MCHGC",
        "description": "Set battery maximum charge current",
        "help": " -- examples: MCHGC1200 (Current in mA xxxx)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "MCHGC([012]\\d\\d\\d)$",
    },
    "MUCHGC": {
        "name": "MUCHGC",
        "description": "Set maximum charge current from AC",
        "help": " -- examples: MUCHGC0600 (Current in mA xxxx)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "MUCHGC([012]\\d\\d\\d)$",
    },
    "SEP": {
        "name": "SEP",
        "description": "Set solar energy distribution priority",
        "help": " -- examples: SEP(00-BLG; 01-LBG; 02-LGB)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "SEP(0[012])$",
    },
    "BDCM": {
        "name": "BDCM",
        "description": "Battery discharge max current in hybrid mode",
        "help": " -- examples: (BDCMxxxx, A)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "BDCM(0[012]\\d\\d)$",
    },
    "BATDV": {
        "name": "BATDV",
        "description": "Battery discharge voltage limits",
        "help": " -- examples: (BATDV0420,0440,0430,0450, 0.1V)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "BATDV(0[45]\\d\\d,0[45]\\d\\d,0[45]\\d\\d,0[45]\\d\\d)$",
    },
    "BCA":{
        "name":"BCA",
        "description":" Set battery charger application in floating charging",
        "help": "--examples: BCA0000,060,0530 - set stop charger current level at 0 Amps, wait at least 60 minutes before recharging, recover to charge when battery stop charger in floating charging below 530",
        "type":"SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "BCA(0\\d\\d\\d,0\\d\\d,0\\d\\d\\d)$",
    },
}


class pi17(AbstractProtocol):
    def __str__(self):
        return "PI17 protocol handler"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI17"
        self.COMMANDS = QUERY_COMMANDS
        self.COMMANDS.update(SETTER_COMMANDS)
        # TODO fix these lists
        self.STATUS_COMMANDS = []
        self.SETTINGS_COMMANDS = [
            "MD",
        ]
        self.DEFAULT_COMMAND = "PI"
        self.PID = "PI"
        self.ID_COMMANDS = ["PI", "DM"]
        self.POLYNOMIAL = 0x1021
        self.PRESET = 0
        self.crcXModem = CRC_XModem()

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
            _pre_cmd = bytes(_prefix, "utf-8") + _cmd
            log.debug(f"_pre_cmd: {_pre_cmd}")
            log.debug(f"_prefix: {_prefix}")
            # calculate the CRC
            # crc_high; crc_low = crc(_pre_cmd)
            # combine byte_cmd, CRC , return
            # PI18 full command "^P005GS\x..\x..\r"
            # _crc = bytes([crc_high, crc_low, 13])
            full_command = _pre_cmd + bytes([13])  # + _crc
            log.debug(f"full command: {full_command}")
            return full_command
        elif _type == "QUERYEN":
            data_length1 = len(_cmd) + 4
            _prefix = f"^P{data_length1:03}"
            log.debug(f"_prefix: {_prefix}")
            intermedstr = _prefix + self._command
            _numb0 = sum(bytearray(intermedstr, "utf-8")) & 255
            _numb = f"{_numb0:03d}"
            log.debug(f"_numb: {_numb}")
            _pre_cmd = intermedstr + str(_numb)
            log.debug(f"_pre_cmd: {_pre_cmd}")
            full_command = bytes(_pre_cmd, "utf-8") + bytes([13])
            log.debug(f"full command: {full_command}")
            return full_command
        else:
            _prefix = f"^S{data_length:03}"
            _pre_cmd = bytes(_prefix, "utf-8") + _cmd
            log.debug(f"_pre_cmd: {_pre_cmd}")
            # calculate the CRC
            # crc_high; crc_low = crc(_pre_cmd)
            # combine byte_cmd, CRC , return
            # PI18 full command "^P005GS\x..\x..\r"
            # _crc = bytes([crc_high, crc_low, 13])
            full_command = _pre_cmd + bytes([13])  # + _crc
            log.debug(f"full command: {full_command}")
            return full_command
    
    def check_response_valid(self, response) -> Tuple[bool, dict]:
        """
        Simplest validity check, CRC checks should be added to individual protocols
        """
        if response is None:
            return False, {"validity check": ["Error: Response was empty", ""]}
        crc = self.crcXModem.crc_hex(response[:-3])

        if response[-3:-1].hex().upper() != crc:
            # print(response[-3:-1].hex().upper(), crc)
            return False, {"validity check": ["Error: CRC error P17", ""]}
        return True, {}

    def get_responses(self, response):
        """
        Override the default get_responses as its different
        """
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

import logging

from .pi30max import pi30max

log = logging.getLogger("pi30m044")

QUERY_COMMANDS = {
    "QPIRI": {
        "name": "QPIRI",
        "description": "Current Settings inquiry",
        "type": "QUERY",
        "response_type": "INDEXED",
        "response": [
            [
                1,
                "Grid Rating Voltage",
                "float",
                "V",
                {"icon": "mdi:transmission-tower-import", "device-class": "voltage"},
            ],
            [2, "Grid Rating Current", "float", "A", {"icon": "mdi:current-ac", "device-class": "current"}],
            [
                3,
                "AC Output Rating Voltage",
                "float",
                "V",
                {"icon": "mdi:transmission-tower-export", "device-class": "voltage"},
            ],
            [4, "AC Output Rating Frequency", "float", "Hz", {"icon": "mdi:current-ac", "device-class": "frequency"}],
            [5, "AC Output Rating Current", "float", "A", {"icon": "mdi:current-ac", "device-class": "current"}],
            [6, "AC Output Rating Apparent Power", "int", "VA", {"icon": "mdi:power-plug", "device-class": "apparent_power"}],
            [
                7,
                "AC Output Rating Active Power",
                "int",
                "W",
                {"icon": "mdi:power-plug", "device-class": "power", "state_class": "measurement"},
            ],
            [8, "Battery Rating Voltage", "float", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
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
                    "TBD",
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
                    "Undefined",
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
            b"(EbuvyzDajkxn@\r",
        ],
    },
    "QMUCHGCR": {
        "name": "QMUCHGCR",
        "description": "Max Utility Charging Current Options inquiry",
        "help": " -- queries the maximum utility charging current setting of the Inverter",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "response": [
            ["int", "Max Utility Charging Current 1", "A"],
            ["int", "Max Utility Charging Current 2", "A"],
            ["int", "Max Utility Charging Current 3", "A"],
            ["int", "Max Utility Charging Current 4", "A"],
            ["int", "Max Utility Charging Current 5", "A"],
            ["int", "Max Utility Charging Current 6", "A"],
            ["int", "Max Utility Charging Current 7", "A"],
            ["int", "Max Utility Charging Current 8", "A"],
            ["int", "Max Utility Charging Current 9", "A"],
            ["int", "Max Utility Charging Current 10", "A"],
            ["int", "Max Utility Charging Current 11", "A"],
            ["int", "Max Utility Charging Current 12", "A"],
            ["int", "Max Utility Charging Current 13", "A"],
        ],
        "test_responses": [
            b"(002 010 020 030 040 050 060 070 080 090 100 110 120\xca#\r",
        ],
    },
    "QMCHGCR": {
        "name": "QMCHGCR",
        "description": "Max Charging Current Options inquiry",
        "help": " -- queries the maximum charging current setting of the Inverter",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "response": [
            ["int", "Max Charging Current 1", "A"],
            ["int", "Max Charging Current 2", "A"],
            ["int", "Max Charging Current 3", "A"],
            ["int", "Max Charging Current 4", "A"],
            ["int", "Max Charging Current 5", "A"],
            ["int", "Max Charging Current 6", "A"],
            ["int", "Max Charging Current 7", "A"],
            ["int", "Max Charging Current 8", "A"],
            ["int", "Max Charging Current 9", "A"],
            ["int", "Max Charging Current 10", "A"],
            ["int", "Max Charging Current 11", "A"],
            ["int", "Max Charging Current 12", "A"],
            ["int", "Max Charging Current 13", "A"],
        ],
        "test_responses": [
            b"(010 020 030 040 050 060 070 080 090 100 110 120\x0c\xcb\r",
        ],
    },
    "QOPPT": {
        "name": "QOPPT",
        "description": "Device Output Source Priority Time Order Inquiry",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "response": [
            [
                "option",
                "Output Source Priority 00 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 01 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 02 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 03 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 04 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 05 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 06 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 07 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 08 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 09 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 10 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 11 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 12 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 13 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 14 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 15 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 16 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 17 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 18 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 19 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 20 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 21 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 22 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Output Source Priority 23 hours",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Device Output Source Priority",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Selection of Output Source Priority Order 1",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Selection of Output Source Priority Order 2",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
            [
                "option",
                "Selection of Output Source Priority Order 3",
                ["Utility Solar Battery (USB)", "Solar Utility Battery (SUB)", "Solar Battery Utility (SBU)"],
            ],
        ],
        "test_responses": [
            b"(2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 2 1>>\r",
        ],
    },
    "QT": {
        "name": "QT",
        "description": "Device Time Inquiry",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "response": [["bytes.decode:datetime.strptime(r, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')", "Device Time", ""]],
        "test_responses": [
            b"(20210726122606JF\r",
        ],
    },
    "QBMS": {
        "name": "QBMS",
        "description": "Read lithium battery information",
        "help": " -- queries the value of various metrics from the battery",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "crctype": "chk",
        "response": [

            [
                "option",
                "Battery connect status",
                [
                    "Connected",
                    "Disconnected",
                ],
            ],
            ["int", "Battery capacity from BMS", "%"],
            [
                "option",
                "Battery force charging",
                [
                    "No",
                    "Yes",
                ],
            ],
            [
                "option",
                "Battery stop discharge flag",
                [
                    "Enable discharge",
                    "Disable discharge",
                ],
            ],
            [
                "option",
                "Battery stop charge flag",
                [
                    "Enable charge",
                    "Disable charge",
                ],
            ],
            ["float:r/10", "Battery bulk charging voltage from BMS", "V"],
            ["float:r/10", "Battery float charging voltage from BMS", "V"],
            ["float:r/10", "Battery cut-off voltage from BMS", "V"],
            ["float", "Battery max charging current", "A"],
            ["float", "Battery max discharge current", "A"]],
         "test_responses": [
            b"(0 100 0 0 1 532 532 450 0000 0030\x5E\n",
        ],
    },
}

SETTER_COMMANDS = {
    "PBT": {
        "name": "PBT",
        "description": "Set Battery Type",
        "help": " -- examples: PBT00 (set battery as AGM), Setting battery type, 00 for AGM, 01 for Flooded battery, 02 for user define, 03 for Pylontech, 04 for Shinheung, 05 for Weco, 06 for Soltaro, 07 for BAK, 08 for Lib, 09 for Lic",
        "type": "SETTER",
        "response": [["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PBT(0[0-9])$",
    },
}

class pi30m044(pi30max):
    def __str__(self):
        return "PI30 protocol handler for Voltronic Axpert Max 7.2k (general_model_name 044, model_name MKS2-7200)"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI30M044"
        # Add pi30m044 specific commands to pi30max commands
        self.COMMANDS.update(QUERY_COMMANDS)
        # Add pi30m044 specific setter commands
        self.COMMANDS.update(SETTER_COMMANDS)
        log.info(f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands")

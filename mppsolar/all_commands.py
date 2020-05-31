commands = {
    "ET": {
        "description": "Total Generated Energy query",
        "help": " -- Query total generated energy",
        "name": "ET",
        "prefix": "^P005",
        "regex": "",
        "response": [
            [
                "int",
                "Total generated energy",
                "KWh"
            ]
        ],
        "supports": [
            "PI18"
        ],
        "test_responses": [
            ""
        ],
        "type": "QUERY"
    },
    "F": {
        "description": "Set Device Output Frequency",
        "help": " -- examples: F50 (set output frequency to 50Hz) or F60 (set output frequency to 60Hz)",
        "name": "F",
        "regex": "F([56]0)$",
        "response": [
            [
                "ack",
                "Command execution",
                {
                    "ACK": "Successful",
                    "NAK": "Failed"
                }
            ]
        ],
        "test_responses": [
            [
                "(NAK",
                "7373"
            ],
            [
                "(ACK",
                "3920"
            ]
        ],
        "type": "SETTER"
    },
    "GS": {
        "description": "General status query",
        "help": " -- Query general status information",
        "name": "GS",
        "prefix": "^P005",
        "regex": "",
        "response": [
            [
                "10int",
                "Grid voltage",
                "V"
            ],
            [
                "10int",
                "Grid frequency",
                "Hz"
            ],
            [
                "10int",
                "AC output voltage",
                "V"
            ],
            [
                "10int",
                "AC output frequency",
                "Hz"
            ],
            [
                "int",
                "AC output apparent power",
                "VA"
            ],
            [
                "int",
                "AC output active power",
                "W"
            ],
            [
                "int",
                "Output load percent",
                "%"
            ],
            [
                "10int",
                "Battery voltage",
                "V"
            ],
            [
                "10int",
                "Battery voltage from SCC",
                "V"
            ],
            [
                "10int",
                "Battery voltage from SCC2",
                "V"
            ],
            [
                "int",
                "Battery discharge current",
                "A"
            ],
            [
                "int",
                "Battery charging current",
                "A"
            ],
            [
                "int",
                "Battery capacity",
                "%"
            ],
            [
                "int",
                "Inverter heat sink temperature",
                "oC"
            ],
            [
                "int",
                "MPPT1 charger temperature",
                "oC"
            ],
            [
                "int",
                "MPPT2 charger temperature",
                "oC"
            ],
            [
                "int",
                "PV1 Input power",
                "W"
            ],
            [
                "int",
                "PV2 Input power",
                "W"
            ],
            [
                "10int",
                "PV1 Input voltage",
                "V"
            ],
            [
                "10int",
                "PV2 Input voltage",
                "V"
            ],
            [
                "option",
                "Setting value configuration state",
                [
                    "Nothing changed",
                    "Something changed"
                ]
            ],
            [
                "option",
                "MPPT1 charger status",
                [
                    "abnormal",
                    "normal but not charged",
                    "charging"
                ]
            ],
            [
                "option",
                "MPPT2 charger status",
                [
                    "abnormal",
                    "normal but not charged",
                    "charging"
                ]
            ],
            [
                "option",
                "Load connection",
                [
                    "disconnect",
                    "connect"
                ]
            ],
            [
                "option",
                "Battery power direction",
                [
                    "donothing",
                    "charge",
                    "discharge"
                ]
            ],
            [
                "option",
                "DC/AC power direction",
                [
                    "donothing",
                    "AC-DC",
                    "DC-AC"
                ]
            ],
            [
                "option",
                "Line power direction",
                [
                    "donothing",
                    "input",
                    "output"
                ]
            ],
            [
                "int",
                "Local parallel ID",
                ""
            ]
        ],
        "supports": [
            "PI18"
        ],
        "test_responses": [
            ""
        ],
        "type": "QUERY"
    },
    "MCHGC": {
        "description": "Set Max Charging Current (for parallel units)",
        "help": " -- examples: MCHGC040 (set unit 0 to max charging current of 40A), MCHGC160 (set unit 1 to max charging current of 60A)",
        "name": "MCHGC",
        "regex": "MCHGC(\\d\\d\\d)$",
        "response": [
            [
                "ack",
                "Command execution",
                {
                    "ACK": "Successful",
                    "NAK": "Failed"
                }
            ]
        ],
        "test_responses": [
            [
                "(NAK",
                "7373"
            ],
            [
                "(ACK",
                "3920"
            ]
        ],
        "type": "SETTER"
    },
    "MNCHGC": {
        "description": "Set Utility Max Charging Current (more than 100A) (for 4000/5000)",
        "help": " -- example: MNCHGC1120 (set unit 1 utility max charging current to 120A)",
        "name": "MNCHGC",
        "regex": "MNCHGC(\\d\\d\\d\\d)$",
        "response": [
            [
                "ack",
                "Command execution",
                {
                    "ACK": "Successful",
                    "NAK": "Failed"
                }
            ]
        ],
        "test_responses": [
            [
                "(NAK",
                "7373"
            ],
            [
                "(ACK",
                "3920"
            ]
        ],
        "type": "SETTER"
    },
    "MOD": {
        "description": "Working mode query",
        "help": " -- Query the working mode",
        "name": "MOD",
        "prefix": "^P006",
        "regex": "",
        "response": [
            [
                "option",
                "Working mode",
                [
                    "Power on mode",
                    "Standby mode",
                    "Bypass mode",
                    "Battery mode",
                    "Fault mode",
                    "Hybrid mode(Line mode, Grid mode)"
                ]
            ]
        ],
        "supports": [
            "PI18"
        ],
        "test_responses": [
            ""
        ],
        "type": "QUERY"
    },
    "MUCHGC": {
        "description": "Set Utility Max Charging Current",
        "help": " -- example: MUCHGC130 (set unit 1 utility max charging current to 30A)",
        "name": "MUCHGC",
        "regex": "MUCHGC(\\d\\d\\d)$",
        "response": [
            [
                "ack",
                "Command execution",
                {
                    "ACK": "Successful",
                    "NAK": "Failed"
                }
            ]
        ],
        "test_responses": [
            [
                "(NAK",
                "7373"
            ],
            [
                "(ACK",
                "3920"
            ]
        ],
        "type": "SETTER"
    },
    "PBCV": {
        "description": "Set Battery re-charge voltage",
        "help": " -- example PBCV44.0 - set re-charge voltage to 44V (12V unit: 11V/11.3V/11.5V/11.8V/12V/12.3V/12.5V/12.8V, 24V unit: 22V/22.5V/23V/23.5V/24V/24.5V/25V/25.5V, 48V unit: 44V/45V/46V/47V/48V/49V/50V/51V)",
        "name": "PBCV",
        "regex": "PBCV(\\d\\d\\.\\d)$",
        "response": [
            [
                "ack",
                "Command execution",
                {
                    "ACK": "Successful",
                    "NAK": "Failed"
                }
            ]
        ],
        "test_responses": [
            [
                "(NAK",
                "7373"
            ],
            [
                "(ACK",
                "3920"
            ]
        ],
        "type": "SETTER"
    },
    "PBDV": {
        "description": "Set Battery re-discharge voltage",
        "help": " -- example PBDV48.0 - set re-discharge voltage to 48V (12V unit: 00.0V/12V/12.3V/12.5V/12.8V/13V/13.3V/13.5V/13.8V/14V/14.3V/14.5, 24V unit: 00.0V/24V/24.5V/25V/25.5V/26V/26.5V/27V/27.5V/28V/28.5V/29V, 48V unit: 00.0V/48V/49V/50V/51V/52V/53V/54V/55V/56V/57V/58V, 00.0V means battery is full(charging in float mode).)",
        "name": "PBDV",
        "regex": "PBDV(\\d\\d\\.\\d)$",
        "response": [
            [
                "ack",
                "Command execution",
                {
                    "ACK": "Successful",
                    "NAK": "Failed"
                }
            ]
        ],
        "test_responses": [
            [
                "(NAK",
                "7373"
            ],
            [
                "(ACK",
                "3920"
            ]
        ],
        "type": "SETTER"
    },
    "PBFT": {
        "description": "Set Battery Float Charging Voltage",
        "help": " -- example PBFT58.0 - set battery float charging voltage to 58V (48.0 - 58.4V for 48V unit)",
        "name": "PBFT",
        "regex": "PBFT(\\d\\d\\.\\d)$",
        "response": [
            [
                "ack",
                "Command execution",
                {
                    "ACK": "Successful",
                    "NAK": "Failed"
                }
            ]
        ],
        "test_responses": [
            [
                "(NAK",
                "7373"
            ],
            [
                "(ACK",
                "3920"
            ]
        ],
        "type": "SETTER"
    },
    "PBT": {
        "description": "Set Battery Type",
        "help": " -- examples: PBT00 (set battery as AGM), PBT01 (set battery as FLOODED), PBT02 (set battery as USER)",
        "name": "PBT",
        "regex": "PBT(0[012])$",
        "response": [
            [
                "ack",
                "Command execution",
                {
                    "ACK": "Successful",
                    "NAK": "Failed"
                }
            ]
        ],
        "test_responses": [
            [
                "(NAK",
                "7373"
            ],
            [
                "(ACK",
                "3920"
            ]
        ],
        "type": "SETTER"
    },
    "PCP": {
        "description": "Set Device Charger Priority",
        "help": " -- examples: PCP00 (set utility first), PCP01 (set solar first), PCP02 (HS only: set solar and utility), PCP03 (set solar only charging)",
        "name": "PCP",
        "regex": "PCP(0[0123])$",
        "response": [
            [
                "ack",
                "Command execution",
                {
                    "ACK": "Successful",
                    "NAK": "Failed"
                }
            ]
        ],
        "test_responses": [
            [
                "(NAK",
                "7373"
            ],
            [
                "(ACK",
                "3920"
            ]
        ],
        "type": "SETTER"
    },
    "PCVV": {
        "description": "Set Battery C.V. (constant voltage) charging voltage",
        "help": " -- example PCVV48.0 - set charging voltage to 48V (48.0 - 58.4V for 48V unit)",
        "name": "PCVV",
        "regex": "PCVV(\\d\\d\\.\\d)$",
        "response": [
            [
                "ack",
                "Command execution",
                {
                    "ACK": "Successful",
                    "NAK": "Failed"
                }
            ]
        ],
        "test_responses": [
            [
                "(NAK",
                "7373"
            ],
            [
                "(ACK",
                "3920"
            ]
        ],
        "type": "SETTER"
    },
    "PEPD": {
        "description": "Set the enabled / disabled state of various Inverter settings (e.g. buzzer, overload, interrupt alarm)",
        "help": " -- examples: PEABJ/PDKUVXYZ (enable A buzzer, B overload bypass, J power saving / disable K LCD go to default after 1min, U overload restart, V overtemp restart, X backlight, Y alarm on primary source interrupt, Z fault code record)",
        "name": "PEPD",
        "regex": "PE(.*)/PD(.*)$",
        "response": [
            [
                "ack",
                "Command execution",
                {
                    "ACK": "Successful",
                    "NAK": "Failed"
                }
            ]
        ],
        "test_responses": [
            [
                "(NAK",
                "7373"
            ],
            [
                "(ACK",
                "3920"
            ]
        ],
        "type": "SETTER"
    },
    "PF": {
        "description": "Set Control Parameters to Default Values",
        "help": " -- example PF (reset control parameters to defaults)",
        "name": "PF",
        "regex": "",
        "response": [
            [
                "ack",
                "Command execution",
                {
                    "ACK": "Successful",
                    "NAK": "Failed"
                }
            ]
        ],
        "test_responses": [
            [
                "(NAK",
                "7373"
            ],
            [
                "(ACK",
                "3920"
            ]
        ],
        "type": "SETTER"
    },
    "PGR": {
        "description": "Set Grid Working Range",
        "help": " -- examples: PCR00 (set device working range to appliance), PCR01 (set device working range to UPS)",
        "name": "PGR",
        "regex": "PGR(0[01])$",
        "response": [
            [
                "ack",
                "Command execution",
                {
                    "ACK": "Successful",
                    "NAK": "Failed"
                }
            ]
        ],
        "test_responses": [
            [
                "(NAK",
                "7373"
            ],
            [
                "(ACK",
                "3920"
            ]
        ],
        "type": "SETTER"
    },
    "PI": {
        "description": "Device Protocol Version inquiry",
        "help": " -- queries the device protocol version",
        "name": "PI",
        "prefix": "^P005",
        "regex": "",
        "response": [
            [
                "string",
                "Protocol Version",
                ""
            ]
        ],
        "supports": [
            "PI18"
        ],
        "test_responses": [
            ""
        ],
        "type": "QUERY"
    },
    "POP": {
        "description": "Set Device Output Source Priority",
        "help": " -- examples: POP00 (set utility first), POP01 (set solar first), POP02 (set SBU priority)",
        "name": "POP",
        "regex": "POP(0[012])$",
        "response": [
            [
                "ack",
                "Command execution",
                {
                    "ACK": "Successful",
                    "NAK": "Failed"
                }
            ]
        ],
        "test_responses": [
            [
                "(NAK",
                "7373"
            ],
            [
                "(ACK",
                "3920"
            ]
        ],
        "type": "SETTER"
    },
    "POPM": {
        "description": "Set Device Output Mode (for 4000/5000)",
        "help": " -- examples: POPM01 (set unit 0 to 1 - parallel output), POPM10 (set unit 1 to 0 - single machine output), POPM02 (set unit 0 to 2 - phase 1 of 3), POPM13 (set unit 1 to 3 - phase 2 of 3), POPM24 (set unit 2 to 4 - phase 3 of 3)",
        "name": "POPM",
        "regex": "POPM(\\d[01234])$",
        "response": [
            [
                "ack",
                "Command execution",
                {
                    "ACK": "Successful",
                    "NAK": "Failed"
                }
            ]
        ],
        "test_responses": [
            [
                "(NAK",
                "7373"
            ],
            [
                "(ACK",
                "3920"
            ]
        ],
        "type": "SETTER"
    },
    "PPCP": {
        "description": "Set Parallel Device Charger Priority (for 4000/5000)",
        "help": " -- examples: PPCP000 (set unit 1 to 00 - utility first), PPCP101 (set unit 1 to 01 - solar first), PPCP202 (set unit 2 to 02 - solar and utility), PPCP003 (set unit 0 to 03 - solar only charging)",
        "name": "PPCP",
        "regex": "PPCP(\\d0[0123])$",
        "response": [
            [
                "ack",
                "Command execution",
                {
                    "ACK": "Successful",
                    "NAK": "Failed"
                }
            ]
        ],
        "test_responses": [
            [
                "(NAK",
                "7373"
            ],
            [
                "(ACK",
                "3920"
            ]
        ],
        "type": "SETTER"
    },
    "PPVOKC": {
        "description": "Set PV OK Condition",
        "help": " -- examples: PPVOKC0 (as long as one unit has connected PV, parallel system will consider PV OK), PPVOKC1 (only if all inverters have connected PV, parallel system will consider PV OK)",
        "name": "PPVOKC",
        "regex": "PPVOKC([01])$",
        "response": [
            [
                "ack",
                "Command execution",
                {
                    "ACK": "Successful",
                    "NAK": "Failed"
                }
            ]
        ],
        "test_responses": [
            [
                "(NAK",
                "7373"
            ],
            [
                "(ACK",
                "3920"
            ]
        ],
        "type": "SETTER"
    },
    "PSDV": {
        "description": "Set Battery Cut-off Voltage",
        "help": " -- example PSDV40.0 - set battery cut-off voltage to 40V (40.0 - 48.0V for 48V unit)",
        "name": "PSDV",
        "regex": "PSDV(\\d\\d\\.\\d)$",
        "response": [
            [
                "ack",
                "Command execution",
                {
                    "ACK": "Successful",
                    "NAK": "Failed"
                }
            ]
        ],
        "test_responses": [
            [
                "(NAK",
                "7373"
            ],
            [
                "(ACK",
                "3920"
            ]
        ],
        "type": "SETTER"
    },
    "PSPB": {
        "description": "Set Solar Power Balance",
        "help": " -- examples: PSPB0 (PV input max current will be the max charged current), PSPB1 (PV input max power will be the sum of the max charge power and loads power)",
        "name": "PSPB",
        "regex": "PSPB([01])$",
        "response": [
            [
                "ack",
                "Command execution",
                {
                    "ACK": "Successful",
                    "NAK": "Failed"
                }
            ]
        ],
        "test_responses": [
            [
                "(NAK",
                "7373"
            ],
            [
                "(ACK",
                "3920"
            ]
        ],
        "type": "SETTER"
    },
    "Q1": {
        "description": "Q1 query",
        "name": "Q1",
        "regex": "",
        "response": [
            [
                "int",
                "Time until the end of absorb charging",
                "sec"
            ],
            [
                "int",
                "Time until the end of float charging",
                "sec"
            ],
            [
                "option",
                "SCC Flag",
                [
                    "SCC not communicating?",
                    "SCC is powered and communicating"
                ]
            ],
            [
                "string",
                "AllowSccOnFlag",
                ""
            ],
            [
                "string",
                "ChargeAverageCurrent",
                ""
            ],
            [
                "int",
                "SCC PWM temperature",
                "Deg_C"
            ],
            [
                "int",
                "Inverter temperature",
                "Deg_C"
            ],
            [
                "int",
                "Battery temperature",
                "Deg_C"
            ],
            [
                "int",
                "Transformer temperature",
                "Deg_C"
            ],
            [
                "int",
                "GPIO13",
                ""
            ],
            [
                "option",
                "Fan lock status",
                [
                    "Not locked",
                    "Locked"
                ]
            ],
            [
                "string",
                "Not used",
                ""
            ],
            [
                "int",
                "Fan PWM speed",
                "Percent"
            ],
            [
                "int",
                "SCC charge power",
                "W"
            ],
            [
                "string",
                "Parallel Warning??",
                ""
            ],
            [
                "float",
                "Sync frequency",
                ""
            ],
            [
                "keyed",
                "Inverter charge status",
                {
                    "10": "nocharging",
                    "11": "bulk stage",
                    "12": "absorb",
                    "13": "float"
                }
            ]
        ],
        "test_responses": [
            [
                "(00000 00000 01 01 00 059 045 053 068 00 00 000 0040 0580 0000 50.00 139",
                "39B9"
            ]
        ],
        "type": "QUERY"
    },
    "QBOOT": {
        "description": "DSP Has Bootstrap inquiry",
        "name": "QBOOT",
        "regex": "",
        "response": [
            [
                "option",
                "DSP Has Bootstrap",
                [
                    "No",
                    "Yes"
                ]
            ]
        ],
        "test_responses": [
            ""
        ],
        "type": "QUERY"
    },
    "QDI": {
        "description": "Default Settings inquiry",
        "help": " -- queries the default settings from the Inverter",
        "name": "QDI",
        "regex": "",
        "response": [
            [
                "float",
                "AC Output Voltage",
                "V"
            ],
            [
                "float",
                "AC Output Frequency",
                "Hz"
            ],
            [
                "int",
                "Max AC Charging Current",
                "A"
            ],
            [
                "float",
                "Battery Under Voltage",
                "V"
            ],
            [
                "float",
                "Battery Float Charge Voltage",
                "V"
            ],
            [
                "float",
                "Battery Bulk Charge Voltage",
                "V"
            ],
            [
                "float",
                "Battery Recharge Voltage",
                "V"
            ],
            [
                "int",
                "Max Charging Current",
                "A"
            ],
            [
                "option",
                "Input Voltage Range",
                [
                    "Appliance",
                    "UPS"
                ]
            ],
            [
                "option",
                "Output Source Priority",
                [
                    "Utility first",
                    "Solar first",
                    "SBU first"
                ]
            ],
            [
                "option",
                "Charger Source Priority",
                [
                    "Utility first",
                    "Solar first",
                    "Solar + Utility",
                    "Only solar charging permitted"
                ]
            ],
            [
                "option",
                "Battery Type",
                [
                    "AGM",
                    "Flooded",
                    "User"
                ]
            ],
            [
                "option",
                "Buzzer",
                [
                    "enabled",
                    "disabled"
                ]
            ],
            [
                "option",
                "Power saving",
                [
                    "disabled",
                    "enabled"
                ]
            ],
            [
                "option",
                "Overload restart",
                [
                    "disabled",
                    "enabled"
                ]
            ],
            [
                "option",
                "Over temperature restart",
                [
                    "disabled",
                    "enabled"
                ]
            ],
            [
                "option",
                "LCD Backlight",
                [
                    "disabled",
                    "enabled"
                ]
            ],
            [
                "option",
                "Primary source interrupt alarm",
                [
                    "disabled",
                    "enabled"
                ]
            ],
            [
                "option",
                "Record fault code",
                [
                    "disabled",
                    "enabled"
                ]
            ],
            [
                "option",
                "Overload bypass",
                [
                    "disabled",
                    "enabled"
                ]
            ],
            [
                "option",
                "LCD reset to default",
                [
                    "disabled",
                    "enabled"
                ]
            ],
            [
                "option",
                "Output mode",
                [
                    "single machine output",
                    "parallel output",
                    "Phase 1 of 3 Phase output",
                    "Phase 2 of 3 Phase output",
                    "Phase 3 of 3 Phase output"
                ]
            ],
            [
                "float",
                "Battery Redischarge Voltage",
                "V"
            ],
            [
                "option",
                "PV OK condition",
                [
                    "As long as one unit of inverters has connect PV, parallel system will consider PV OK",
                    "Only All of inverters have connect PV, parallel system will consider PV OK"
                ]
            ],
            [
                "option",
                "PV Power Balance",
                [
                    "PV input max current will be the max charged current",
                    "PV input max power will be the sum of the max charged power and loads power"
                ]
            ]
        ],
        "test_responses": [
            [
                "(230.0 50.0 0030 42.0 54.0 56.4 46.0 60 0 0 2 0 0 0 0 0 1 1 0 0 1 0 54.0 0 1 000",
                "9E60"
            ]
        ],
        "type": "QUERY"
    },
    "QFLAG": {
        "description": "Flag Status inquiry",
        "help": " -- queries the enabled / disabled state of various Inverter settings (e.g. buzzer, overload, interrupt alarm)",
        "name": "QFLAG",
        "regex": "",
        "response": [
            [
                "enflags",
                "Device Status",
                {
                    "a": {
                        "name": "Buzzer",
                        "state": "disabled"
                    },
                    "b": {
                        "name": "Overload Bypass",
                        "state": "disabled"
                    },
                    "j": {
                        "name": "Power Saving",
                        "state": "disabled"
                    },
                    "k": {
                        "name": "LCD Reset to Default",
                        "state": "disabled"
                    },
                    "u": {
                        "name": "Overload Restart",
                        "state": "disabled"
                    },
                    "v": {
                        "name": "Over Temperature Restart",
                        "state": "disabled"
                    },
                    "x": {
                        "name": "LCD Backlight",
                        "state": "disabled"
                    },
                    "y": {
                        "name": "Primary Source Interrupt Alarm",
                        "state": "disabled"
                    },
                    "z": {
                        "name": "Record Fault Code",
                        "state": "disabled"
                    }
                }
            ]
        ],
        "test_responses": [
            [
                "(EakxyDbjuvz",
                "2F29"
            ]
        ],
        "type": "QUERY"
    },
    "QID": {
        "description": "Device Serial Number inquiry",
        "help": " -- queries the device serial number",
        "name": "QID",
        "regex": "",
        "response": [
            [
                "string",
                "Serial Number",
                ""
            ]
        ],
        "test_responses": [
            [
                "(9293333010501",
                "BB07"
            ]
        ],
        "type": "QUERY"
    },
    "QMCHGCR": {
        "description": "Max Charging Current Options inquiry",
        "help": " -- queries the maximum charging current setting of the Inverter",
        "name": "QMCHGCR",
        "regex": "",
        "response": [
            [
                "string",
                "Max Charging Current",
                "A"
            ]
        ],
        "test_responses": [
            ""
        ],
        "type": "QUERY"
    },
    "QMOD": {
        "description": "Mode inquiry",
        "help": " -- queries the Inverter mode",
        "name": "QMOD",
        "regex": "",
        "response": [
            [
                "keyed",
                "Device Mode",
                {
                    "B": "Battery",
                    "F": "Fault",
                    "H": "Power saving",
                    "L": "Line",
                    "P": "Power on",
                    "S": "Standby"
                }
            ]
        ],
        "test_responses": [
            [
                "(Se5",
                "6439"
            ]
        ],
        "type": "QUERY"
    },
    "QMUCHGCR": {
        "description": "Max Utility Charging Current Options inquiry",
        "help": " -- queries the maximum utility charging current setting of the Inverter",
        "name": "QMUCHGCR",
        "regex": "",
        "response": [
            [
                "string",
                "Max Utility Charging Current",
                "A"
            ]
        ],
        "test_responses": [
            ""
        ],
        "type": "QUERY"
    },
    "QOPM": {
        "description": "Output Mode inquiry",
        "help": " -- queries the output mode of the Inverter (e.g. single, parallel, phase 1 of 3 etc)",
        "name": "QOPM",
        "regex": "",
        "response": [
            [
                "option",
                "Output mode",
                [
                    "single machine output",
                    "parallel output",
                    "Phase 1 of 3 Phase output",
                    "Phase 2 of 3 Phase output",
                    "Phase 3 of 3 Phase output"
                ]
            ]
        ],
        "test_responses": [
            ""
        ],
        "type": "QUERY"
    },
    "QP2GS": {
        "description": "Parallel Information inquiry",
        "help": " -- example: QP2GS1 queries the values of various metrics from instance 1 of parallel setup Inverters (numbers from 0)",
        "name": "QP2GS",
        "regex": "QP2GS(\\d)$",
        "response": [
            [
                "int",
                "Parallel instance number??",
                ""
            ],
            [
                "int",
                "Serial number",
                ""
            ],
            [
                "keyed",
                "Work mode",
                {
                    "B": "Battery Mode",
                    "F": "Fault Mode",
                    "H": "Power Saving Mode",
                    "L": "Line Mode",
                    "P": "Power On Mode",
                    "S": "Standby Mode"
                }
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
                    "86": "Parallel output setting different"
                }
            ],
            [
                "float",
                "L2 AC input voltage",
                "V"
            ],
            [
                "float",
                "L2 AC input frequency",
                "Hz"
            ],
            [
                "float",
                "L2 AC output voltage",
                "V"
            ],
            [
                "float",
                "L2 AC output frequency",
                "Hz"
            ],
            [
                "int",
                "L2 AC output apparent power",
                "VA"
            ],
            [
                "int",
                "L2 AC output active power",
                "W"
            ],
            [
                "int",
                "L2 Load percentage",
                "%"
            ],
            [
                "float",
                "L2 Battery voltage",
                "V"
            ],
            [
                "int",
                "L2 Battery charging current",
                "A"
            ],
            [
                "int",
                "L2 Battery capacity",
                "%"
            ],
            [
                "float",
                "PV2 Input Voltage",
                "V"
            ],
            [
                "int",
                "PV2 charging current",
                "A"
            ],
            [
                "flags",
                "Inverter Status",
                [
                    "is_l2_scc_ok",
                    "is_l2_ac_charging",
                    "is_l2_scc_charging",
                    "is_battery_over_voltage",
                    "is_battery_under_voltage",
                    "is_l2_line_lost",
                    "is_l2_load_on",
                    "is_configuration_changed"
                ]
            ]
        ],
        "supports": [
            "LV5048"
        ],
        "test_responses": [
            [
                "(11 92911906100045 L 00 124.2 59.98 124.2 59.98 0149 0130 005 56.1 000 100 000.0 00 01000010",
                "A9A8"
            ]
        ],
        "type": "QUERY"
    },
    "QPGS": {
        "description": "Parallel Information inquiry LV5048",
        "help": " -- example: QPGS1 queries the values of various metrics from instance 1 of parallel setup Inverters (numbers from 0)",
        "name": "QPGS",
        "regex": "QPGS(\\d)$",
        "response": [
            [
                "option",
                "Parallel instance number",
                [
                    "Not valid",
                    "valid"
                ]
            ],
            [
                "int",
                "Serial number",
                ""
            ],
            [
                "keyed",
                "Work mode",
                {
                    "B": "Battery Mode",
                    "F": "Fault Mode",
                    "H": "Power Saving Mode",
                    "L": "Line Mode",
                    "P": "Power On Mode",
                    "S": "Standby Mode"
                }
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
                    "86": "Parallel output setting different"
                }
            ],
            [
                "float",
                "L1 AC input voltage",
                "V"
            ],
            [
                "float",
                "L1 AC input frequency",
                "Hz"
            ],
            [
                "float",
                "L1 AC output voltage",
                "V"
            ],
            [
                "float",
                "L1 AC output frequency",
                "Hz"
            ],
            [
                "int",
                "L1 AC output apparent power",
                "VA"
            ],
            [
                "int",
                "L1 AC output active power",
                "W"
            ],
            [
                "int",
                "L1 Load percentage",
                "%"
            ],
            [
                "float",
                "Battery voltage",
                "V"
            ],
            [
                "int",
                "Battery charging current",
                "A"
            ],
            [
                "int",
                "Battery capacity",
                "%"
            ],
            [
                "float",
                "PV1 Input Voltage",
                "V"
            ],
            [
                "int",
                "Total charging current",
                "A"
            ],
            [
                "int",
                "Total AC output apparent power",
                "VA"
            ],
            [
                "int",
                "Total output active power",
                "W"
            ],
            [
                "int",
                "Total AC output percentage",
                "%"
            ],
            [
                "flags",
                "Inverter Status",
                [
                    "is_l1_scc_ok",
                    "is_l1_ac_charging_on",
                    "is_l1_scc_charging_on",
                    "is_battery_over_voltage",
                    "is_battery_under_voltage",
                    "is_l1_line_off",
                    "is_l1_load_on",
                    "is_configuration_changed"
                ]
            ],
            [
                "option",
                "Output mode",
                [
                    "Standalone?",
                    "Parallel output 0 degrees",
                    "Phase 1 of 3 Phase output",
                    "Phase 2 of 3 Phase output",
                    "Phase 3 of 3 Phase output",
                    "Parallel output 120 degrees",
                    "Parallel output 180 degrees"
                ]
            ],
            [
                "option",
                "Charger source priority",
                [
                    "Utility first",
                    "Solar first",
                    "Solar + Utility",
                    "Solar only"
                ]
            ],
            [
                "int",
                "Max charger current",
                "A"
            ],
            [
                "int",
                "Max charger range",
                "A"
            ],
            [
                "int",
                "Max AC charger current",
                "A"
            ],
            [
                "int",
                "PV1 charging current",
                "A"
            ],
            [
                "int",
                "Battery discharge current",
                "A"
            ]
        ],
        "supports": [
            "LV5048"
        ],
        "test_responses": [
            [
                "(1 92911906100045 L 00 122.9 59.98 122.9 59.98 0331 0272 013 56.1 004 100 000.0 004 01577 01400 009 01000010 6 0 060 220 40 00 000",
                "C7C2"
            ]
        ],
        "type": "QUERY"
    },
    "QPI": {
        "description": "Protocol ID inquiry",
        "help": " -- queries the device protocol ID. e.g. 30 for HS series",
        "name": "QPI",
        "regex": "",
        "response": [
            [
                "string",
                "Protocol ID",
                ""
            ]
        ],
        "test_responses": [
            [
                "(PI30",
                "9A0B"
            ]
        ],
        "type": "QUERY"
    },
    "QPIGS": {
        "description": "General Status Parameters inquiry",
        "help": " -- queries the value of various metrics from the Inverter",
        "name": "QPIGS",
        "nosupports": [
            "LV5048"
        ],
        "regex": "",
        "response": [
            [
                "float",
                "AC Input Voltage",
                "V"
            ],
            [
                "float",
                "AC Input Frequency",
                "Hz"
            ],
            [
                "float",
                "AC Output Voltage",
                "V"
            ],
            [
                "float",
                "AC Output Frequency",
                "Hz"
            ],
            [
                "int",
                "AC Output Apparent Power",
                "VA"
            ],
            [
                "int",
                "AC Output Active Power",
                "W"
            ],
            [
                "int",
                "AC Output Load",
                "%"
            ],
            [
                "int",
                "BUS Voltage",
                "V"
            ],
            [
                "float",
                "Battery Voltage",
                "V"
            ],
            [
                "int",
                "Battery Charging Current",
                "A"
            ],
            [
                "int",
                "Battery Capacity",
                "%"
            ],
            [
                "int",
                "Inverter Heat Sink Temperature",
                "Deg_C"
            ],
            [
                "int",
                "PV Input Current for Battery",
                "A"
            ],
            [
                "float",
                "PV Input Voltage",
                "V"
            ],
            [
                "float",
                "Battery Voltage from SCC",
                "V"
            ],
            [
                "int",
                "Battery Discharge Current",
                "A"
            ],
            [
                "flags",
                "Device Status",
                [
                    "is_sbu_priority_version_added",
                    "is_configuration_changed",
                    "is_scc_firmware_updated",
                    "is_load_on",
                    "is_battery_voltage_to_steady_while_charging",
                    "is_charging_on",
                    "is_scc_charging_on",
                    "is_ac_charging_on"
                ]
            ]
        ],
        "test_responses": [
            [
                "(000.0 00.0 230.0 49.9 0161 0119 003 460 57.50 012 100 0069 0014 103.8 57.45 00000 00110110 00 00 00856 010",
                "248C"
            ]
        ],
        "type": "QUERY"
    },
    "QPIGS2": {
        "description": "General Status Parameters inquiry",
        "help": " -- queries the value of various metrics from the Inverter",
        "name": "QPIGS2",
        "regex": "",
        "response": [
            [
                "float",
                "L2 AC Input Voltage",
                "V"
            ],
            [
                "float",
                "L2 AC Input Frequency",
                "Hz"
            ],
            [
                "float",
                "L2 AC Output Voltage",
                "V"
            ],
            [
                "float",
                "L2 AC Output Frequency",
                "Hz"
            ],
            [
                "int",
                "L2 AC Output Apparent Power",
                "VA"
            ],
            [
                "int",
                "L2 AC Output Active Power",
                "W"
            ],
            [
                "int",
                "L2 AC Output Load",
                "%"
            ],
            [
                "int",
                "PV2 Battery Charging Current",
                "A"
            ],
            [
                "float",
                "PV2 Input Voltage",
                "V"
            ],
            [
                "float",
                "L2 Battery Voltage",
                "V"
            ],
            [
                "flags",
                "Device Status",
                [
                    "is_l2_scc_ok",
                    "is_l2_ac_charging_on",
                    "is_l2_scc_charging_on",
                    "reserved",
                    "is_l2_line_not_ok",
                    "is_load_on",
                    "reserved"
                ]
            ]
        ],
        "supports": [
            "LV5048"
        ],
        "test_responses": [
            ""
        ],
        "type": "QUERY"
    },
    "QPIRI": {
        "description": "Current Settings inquiry",
        "help": " -- queries the current settings from the Inverter",
        "name": "QPIRI",
        "nosupports": [
            "LV5048"
        ],
        "regex": "",
        "response": [
            [
                "float",
                "AC Input Voltage",
                "V"
            ],
            [
                "float",
                "AC Input Current",
                "A"
            ],
            [
                "float",
                "AC Output Voltage",
                "V"
            ],
            [
                "float",
                "AC Output Frequency",
                "Hz"
            ],
            [
                "float",
                "AC Output Current",
                "A"
            ],
            [
                "int",
                "AC Output Apparent Power",
                "VA"
            ],
            [
                "int",
                "AC Output Active Power",
                "W"
            ],
            [
                "float",
                "Battery Voltage",
                "V"
            ],
            [
                "float",
                "Battery Recharge Voltage",
                "V"
            ],
            [
                "float",
                "Battery Under Voltage",
                "V"
            ],
            [
                "float",
                "Battery Bulk Charge Voltage",
                "V"
            ],
            [
                "float",
                "Battery Float Charge Voltage",
                "V"
            ],
            [
                "option",
                "Battery Type",
                [
                    "AGM",
                    "Flooded",
                    "User"
                ]
            ],
            [
                "int",
                "Max AC Charging Current",
                "A"
            ],
            [
                "int",
                "Max Charging Current",
                "A"
            ],
            [
                "option",
                "Input Voltage Range",
                [
                    "Appliance",
                    "UPS"
                ]
            ],
            [
                "option",
                "Output Source Priority",
                [
                    "Utility first",
                    "Solar first",
                    "SBU first"
                ]
            ],
            [
                "option",
                "Charger Source Priority",
                [
                    "Utility first",
                    "Solar first",
                    "Solar + Utility",
                    "Only solar charging permitted"
                ]
            ],
            [
                "int",
                "Max Parallel Units",
                "units"
            ],
            [
                "keyed",
                "Machine Type",
                {
                    "00": "Grid tie",
                    "01": "Off Grid",
                    "10": "Hybrid"
                }
            ],
            [
                "option",
                "Topology",
                [
                    "transformerless",
                    "transformer"
                ]
            ],
            [
                "option",
                "Output Mode",
                [
                    "single machine output",
                    "parallel output",
                    "Phase 1 of 3 Phase output",
                    "Phase 2 of 3 Phase output",
                    "Phase 3 of 3 Phase output"
                ]
            ],
            [
                "float",
                "Battery Redischarge Voltage",
                "V"
            ],
            [
                "option",
                "PV OK Condition",
                [
                    "As long as one unit of inverters has connect PV, parallel system will consider PV OK",
                    "Only All of inverters have connect PV, parallel system will consider PV OK"
                ]
            ],
            [
                "option",
                "PV Power Balance",
                [
                    "PV input max current will be the max charged current",
                    "PV input max power will be the sum of the max charged power and loads power"
                ]
            ]
        ],
        "test_responses": [
            [
                "(230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10 010 1 0 0 6 01 0 0 54.0 0 1",
                "6F7E"
            ]
        ],
        "type": "QUERY"
    },
    "QPIWS": {
        "description": "Warning status inquiry",
        "help": " -- queries any active warnings flags from the Inverter",
        "name": "QPIWS",
        "regex": "",
        "response": [
            [
                "stat_flags",
                "Warning status",
                [
                    "Reserved",
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
                    "Reserved",
                    "Reserved"
                ]
            ]
        ],
        "test_responses": [
            [
                "(00000100000000000000000000000000",
                "FE82"
            ]
        ],
        "type": "QUERY"
    },
    "QVFW": {
        "description": "Main CPU firmware version inquiry",
        "help": " -- queries the main CPU firmware version",
        "name": "QVFW",
        "regex": "",
        "response": [
            [
                "string",
                "Main CPU firmware version",
                ""
            ]
        ],
        "test_responses": [
            [
                "(VERFW:00072.70",
                "53A7"
            ]
        ],
        "type": "QUERY"
    },
    "QVFW2": {
        "description": "Secondary CPU firmware version inquiry",
        "help": " -- queries the secondary CPU firmware version",
        "name": "QVFW2",
        "regex": "",
        "response": [
            [
                "string",
                "Secondary CPU firmware version",
                ""
            ]
        ],
        "test_responses": [
            ""
        ],
        "type": "QUERY"
    }
}

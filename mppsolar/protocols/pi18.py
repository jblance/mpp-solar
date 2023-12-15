import logging

from .abstractprotocol import AbstractProtocol
from .protocol_helpers import crcPI as crc

log = logging.getLogger("pi18")

COMMANDS = {
    # QUERY #
    "PI": {
        "name": "PI",
        "prefix": "^P005",
        "description": "Device Protocol Version inquiry",
        "help": " -- queries the device protocol version \n",
        "type": "QUERY",
        "response": [["string", "Protocol Version", ""]],
        "test_responses": [
            b"^D00518;\x03\r",
        ],
    },
    #    "T": {
    #        "name": "T",
    #        "prefix": "^P004",
    #        "description": "Queryy current time",
    #        "help": " -- queries the device protocol version \n",
    #    },
    "ET": {
        "name": "ET",
        "prefix": "^P005",
        "description": "Total PV Generated Energy Inquiry",
        "help": " -- display Total PV generated energy",
        "type": "QUERY",
        "response_type": "SEQUENTIAL",
        "response": [
            [
                "int",
                "Total PV Generated Energy",
                "Wh",
                {"icon": "mdi:counter", "device-class": "energy", "state_class": "total"},
            ]
        ],
        "test_responses": [
            b"",
        ],
    },
    "EY": {
        "name": "EY",
        "prefix": "^P009",
        "description": "Yearly PV Generated Energy Inquiry",
        "help": " -- display Yearly PV generated energy, format is EYyyyy",
        "type": "QUERY",
        "response_type": "INDEXED",
        "response": [
            [
                1,
                "PV Generated Energy for Year",
                "int",
                "Wh",
                {"icon": "mdi:counter", "device-class": "energy", "state_class": "total"},
            ],
            [2, "Year", "info:cv[:4]", ""],
        ],
        "test_responses": [
            b"^D01105580051\x0b\x9f\r",
        ],
        "regex": "EY(\\d\\d\\d\\d)$",
    },
    "EM": {
        "name": "EM",
        "prefix": "^P011",
        "description": "Monthly PV Generated Energy Inquiry",
        "help": " -- display monthly PV generated energy, format is EMyyyymm",
        "type": "QUERY",
        "response_type": "INDEXED",
        "response": [
            [
                1,
                "PV Generated Energy for Month",
                "int",
                "Wh",
                {"icon": "mdi:counter", "device-class": "energy", "state_class": "total"},
            ],
            [2, "Year", "info:cv[:4]", ""],
            [3, "Month", "info:calendar.month_name[int(cv[4:6])]", ""],
        ],
        "test_responses": [
            b"",
        ],
        "regex": "EM(\\d\\d\\d\\d\\d\\d)$",
    },
    "ED": {
        "name": "ED",
        "prefix": "^P013",
        "description": "Daily PV Generated Energy Inquiry",
        "help": " -- display daily PV generated energy, format is EDyyyymmdd",
        "type": "QUERY",
        "response_type": "INDEXED",
        "response": [
            [1, "PV Generated Energy for Day", "int", "Wh", {"icon": "mdi:counter", "device-class": "energy"}],
            [2, "Year", "info:cv[:4]", ""],
            [3, "Month", "info:calendar.month_name[int(cv[4:6])]", ""],
            [4, "Day", "info:cv[6:]", ""],
        ],
        "test_responses": [
            b"^D009000091\xba\x10\r",
        ],
        "regex": "ED(\\d\\d\\d\\d\\d\\d\\d\\d)$",
    },
    "ID": {
        "name": "ID",
        "prefix": "^P005",
        "description": "Device Serial Number inquiry",
        "help": " -- queries the device serial number",
        "type": "QUERY",
        "response": [["string", "Serial Number", ""]],
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
            ["int", "Main CPU Version", ""],
            ["int", "Slave 1 CPU Version", ""],
            ["int", "Slave 2 CPU Version", ""],
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
            ["10int", "AC input rated voltage", "V", {"icon": "mdi:power-plug", "device-class": "voltage"}],
            ["10int", "AC input rated current", "A", {"icon": "mdi:current-ac", "device-class": "current"}],
            ["10int", "AC output rated voltage", "V", {"icon": "mdi:power-plug", "device-class": "voltage"}],
            ["10int", "AC output rated frequency", "Hz", {"icon": "mdi:sine-wave", "device-class": "frequency"}],
            ["10int", "AC output rated current", "A", {"icon": "mdi:current-ac", "device-class": "current"}],
            [
                "int",
                "AC output rating apparent power",
                "VA",
                {"icon": "mdi:power-plug", "device-class": "apparent_power"},
            ],
            ["int", "AC output rating active power", "W", {"icon": "mdi:power-plug", "device-class": "power"}],
            ["10int", "Battery rated voltage", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            ["10int", "Battery re-charge voltage", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            ["10int", "Battery re-discharge voltage", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            ["10int", "Battery under voltage", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            ["10int", "Battery bulk voltage", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            ["10int", "Battery float voltage", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            #["option", "Battery type", ["AGM", "Flooded", "User"]],
            ["option", "Battery Type", [ "AGM", "Flooded", "User", "Pylontech", "TBD", "WECO", "Soltaro", "3rd party Lithium", "LIB", "LIC", ]],
            ["int", "Max AC charging current", "A", {"icon": "mdi:current-dc", "device-class": "current"}],
            ["int", "Max charging current", "A", {"icon": "mdi:current-dc", "device-class": "current"}],
            ["option", "Input voltage rang", ["Appliance", "UPS"]],
            ["option", "Output source priority", ["Solar-Utility-Battery", "Solar-Battery-Utility"]],
            ["option", "Charger source priority", ["Solar First", "Solar and Utility", "Only Solar"]],
            ["int", "Parallel max num", ""],
            ["option", "Machine type", ["Off-Grid", "Grid-Tie"]],
            ["option", "Topology", ["transformerless", "ransformer"]],
            [
                "option",
                "Output model setting",
                [
                    "Single module",
                    "parallel output",
                    "Phase 1 of three phase output",
                    "Phase 2 of three phase output",
                    "Phase 3 of three phase output",
                ],
            ],
            ["option", "Solar power priority", ["Battery-Load-Utiliy + AC Charger", "Load-Battery-Utiliy"]],
            ["int", "MPPT strings", ""],
        ],
        "test_responses": [
            b"^D0882300,217,2300,500,217,5000,5000,480,500,540,450,552,545,2,10,060,1,1,1,9,1,0,0,0,1,00\r",
            b"^D0882300,217,2300,500,217,5000,5000,480,500,540,450,560,560,2,02,060,1,0,1,9,1,0,0,0,1,00\xe9\r",
        ],
    },
    "GS": {
        "name": "GS",
        "prefix": "^P005",
        "description": "General status query",
        "help": " -- Query general status information",
        "type": "QUERY",
        "response": [
            ["10int", "Grid voltage", "V", {"icon": "mdi:transmission-tower", "device-class": "voltage"}],
            ["10int", "Grid frequency", "Hz", {"icon": "mdi:sine-wave", "device-class": "frequency"}],
            [
                "10int",
                "AC output voltage",
                "V",
                {"icon": "mdi:home-lightning-bolt-outline", "device-class": "voltage"},
            ],
            ["10int", "AC output frequency", "Hz", {"icon": "mdi:sine-wave", "device-class": "frequency"}],
            [
                "int",
                "AC output apparent power",
                "VA",
                {"icon": "mdi:home-lightning-bolt", "device-class": "apparent_power"},
            ],
            ["int", "AC output active power", "W", {"icon": "mdi:lightning-bolt", "device-class": "power"}],
            ["int", "Output load percent", "%", {"icon": "mdi:brightness-percent"}],
            ["10int", "Battery voltage", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            ["10int", "Battery voltage from SCC", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            ["10int", "Battery voltage from SCC2", "V", {"icon": "mdi:battery-outline", "device-class": "voltage"}],
            ["int", "Battery discharge current", "A", {"icon": "mdi:current-dc", "device-class": "current"}],
            ["int", "Battery charging current", "A", {"icon": "mdi:current-dc", "device-class": "current"}],
            ["int", "Battery capacity", "%", {"icon": "mdi:brightness-percent"}],
            [
                "int",
                "Inverter heat sink temperature",
                "°C",
                {"icon": "mdi:thermometer", "device-class": "temperature"},
            ],
            ["int", "MPPT1 charger temperature", "°C", {"icon": "mdi:thermometer", "device-class": "temperature"}],
            ["int", "MPPT2 charger temperature", "°C", {"icon": "mdi:thermometer", "device-class": "temperature"}],
            ["int", "PV1 Input power", "W", {"icon": "mdi:solar-power", "device-class": "power"}],
            ["int", "PV2 Input power", "W", {"icon": "mdi:solar-power", "device-class": "power"}],
            ["10int", "PV1 Input voltage", "V", {"icon": "mdi:solar-power", "device-class": "voltage"}],
            ["10int", "PV2 Input voltage", "V", {"icon": "mdi:solar-power", "device-class": "voltage"}],
            [
                "option",
                "Setting value configuration state",
                ["Nothing changed", "Something changed"],
            ],
            [
                "option",
                "MPPT1 charger status",
                ["abnormal", "normal but not charged", "charging"],
            ],
            [
                "option",
                "MPPT2 charger status",
                ["abnormal", "normal but not charged", "charging"],
            ],
            ["option", "Load connection", ["disconnect", "connect"]],
            ["option", "Battery power direction", ["donothing", "charge", "discharge"]],
            ["option", "DC/AC power direction", ["donothing", "AC-DC", "DC-AC"]],
            ["option", "Line power direction", ["donothing", "input", "output"]],
            ["int", "Local parallel ID", ""],
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
            [
                "option",
                "Working mode",
                [
                    "Power on mode",
                    "Standby mode",
                    "Bypass mode",
                    "Battery mode",
                    "Fault mode",
                    "Hybrid mode(Line mode, Grid mode)",
                ],
            ],
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
            ["option", "Buzzer beep", ["Disabled", "Enabled"]],
            ["option", "Overload bypass function", ["Disabled", "Enabled"]],
            ["option", "display back to default page", ["Disabled", "Enabled"]],
            ["option", "Overload restart", ["Disabled", "Enabled"]],
            ["option", "Over temperature restart", ["Disabled", "Enabled"]],
            ["option", "Backlight on", ["Disabled", "Enabled"]],
            ["option", "Alarm primary source interrupt", ["Disabled", "Enabled"]],
            ["option", "Fault code record", ["Disabled", "Enabled"]],
            ["int", "Reserved", ""],
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
            ["int", "Max. charging current value 1", "A"],
            ["int", "Max. charging current value 2", "A"],
            ["int", "Max. charging current value 3", "A"],
            ["int", "Max. charging current value 4", "A"],
            ["int", "Max. charging current value 5", "A"],
            ["int", "Max. charging current value 6", "A"],
            ["int", "Max. charging current value 7", "A"],
            ["int", "Max. charging current value 8", "A"],
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
            ["int", "Max. AC charging current value 1", "A"],
            ["int", "Max. AC charging current value 2", "A"],
            ["int", "Max. AC charging current value 3", "A"],
            ["int", "Max. AC charging current value 4", "A"],
            ["int", "Max. AC charging current value 5", "A"],
            ["int", "Max. AC charging current value 6", "A"],
            ["int", "Max. AC charging current value 7", "A"],
            ["int", "Max. AC charging current value 8", "A"],
            ["int", "Max. AC charging current value 9", "A"],
        ],
        "test_responses": [
            b"",
        ],
    },
    # SETTER ###
    #    "LON": {
    #        "name": "LON",
    #        "prefix": "^S007",
    #        "description": "Set enable/disable machine supply power to the loads",
    #        "help": " -- example: LON1 (0: disable, 1: enable)",
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
        "description": "Set output souce priority 				(Manual Option 01)",
        "help": " -- example: POP0 		(set Output POP0 [0: Solar-Utility-Batter],  POP1 [1: Solar-Battery-Utility]",
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
    "PSP": {
        "name": "PSP",
        "prefix": "^S007",
        "description": "Set solar power priority 				(Manual Option 05)",
        "help": " -- example: PSP0 		(set Priority PSP0 [0: Battery-Load-Utiliy (+AC Charge)],  PSP1 [1: Load-Battery-Utiliy]",
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
    "PEI": {
        "name": "PEI",
        "prefix": "^S006",
        "description": "Set Machine type,  enable: Grid-Tie 			(Manual Option 09)",
        "help": " -- example: PEI 		(set enable Grid-Tie)",
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
        "description": "Set Machine type, disable: Grid-Tie 			(Manual Option 09)",
        "help": " -- example: PDI 		(set disable Grid-Tie)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "PCP": {
        "name": "PCP",
        "prefix": "^S009",
        "description": "Set charging source priority 				(Manual Option 10)",
        "help": " -- example: PCP0,1 		(set unit 0 [0-9] to 0: Solar first, 1: Solar and Utility, 2: Only solar)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "PCP([0-9],[012])$",
    },
    "MCHGC": {
        "name": "MCHGC",
        "prefix": "^S013",
        "description": "Set Battery Max Charging Current Solar + AC 		(Manual Option 11)",
        "help": " -- example: MCHGC0,030 	(set unit 0 [0-9] to max charging current of  30A [    010 020 030 040 050 060 070 080])",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "MCHGC([0-9],0[1-8]0)$",
    },
    "MUCHGC": {
        "name": "MUCHGC",
        "prefix": "^S014",
        "description": "Set Battery Max AC Charging Current 			(Manual Option 13)",
        "help": " -- example: MUCHGC0,030 	(set unit 0 [0-9] utility charging current to 30A [002 010 020 030 040 050 060 070 080])",
        "type": "SETTER",
        "response": [["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [
            b"",
        ],
        "regex": "MUCHGC([0-9]),(002|0[1-8]0)$",
    },
    "PBT": {
        "name": "PBT",
        "prefix": "^S007",
        "description": "Set Battery Type 					(Manual Option 14)",
        "help": " -- example: PBT0 		(set battery as PBT0 [0: AGM], PBT1 [1: FLOODED], PBT2 [2: USER])",
        "type": "SETTER",
        "response": [["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PBT([012])$",
    },
    "MCHGV": {
        "name": "MCHGV",
        "prefix": "^S015",
        "description": "Set Battery Bulk,Float charge voltages 		     (Manual Option 17,18)",
        "help": " -- example: MCHGV552,540 	(set Bulk - CV voltage [480~584] in 0.1V xxx, Float voltage [480~584] in 0.1V yyy)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        # Regex 480 - 584 Volt
        "regex": "MCHGV(4[8-9][0-9]|5[0-7][0-9]|58[0-5]),(4[8-9][0-9]|5[0-7][0-9]|58[0-4])$",
    },
    "PSDV": {
        "name": "PSDV",
        "prefix": "^S010",
        "description": "Set Battery Cut-off Voltage	 			(Manual Option 19)",
        "help": " -- example: PSDV450 		(set battery cut-off voltage to 45V [400~480V] for 48V unit)",
        "type": "SETTER",
        "response": [["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "PSDV(4[0-7][0-9]|480)$",
    },
    "BUCD": {
        "name": "BUCD",
        "prefix": "^S014",
        "description": "Set Battery Stop dis,charging when Grid is available (Manual Option 20,21)",
        "help": " -- example: BUCD440,480	(set Stop discharge Voltage [440~510] in 0.1V xxx, Stop Charge Voltage [000(Full) or 480~580] in 0.1V yyy)",
        "type": "SETTER",
        "response": [["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}]],
        "test_responses": [
            b"(NAK\x73\x73\r",
            b"(ACK\x39\x20\r",
        ],
        "regex": "BUCD((4[4-9]0|5[0-1]0),(000|4[8-9]0|5[0-8]0))$",
    },
}


class pi18(AbstractProtocol):
    def __str__(self):
        return "PI18 protocol handler"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI18"
        self.NOCRC = False
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = [
            "ET",
            "EY",
            "EM",
            "ED",
            "ID",
            "VFW",
            "PIRI",
            "GS",
            "MOD",
            # "FWS",
            "FLAG",
            # "DI",
            "MCHGCR",
            "MUCHGCR",
        ]
        self.SETTINGS_COMMANDS = [
            "PEI" "PDI" "POP"
            # "PCP",
            "PSP",
            "MCHGV",
            "MUCHGC",
        ]
        self.DEFAULT_COMMAND = "PI"
        self.PID = "PI"
        self.ID_COMMANDS = [("PI", "Protocol Version"), ("VFW", "Main CPU Version")]

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

        # Full command components
        _cmd = bytes(self._command, "utf-8")
        log.debug(f"_cmd is: {_cmd}")

        _type = self._command_defn["type"]
        log.debug(f"_type is: {_type}")

        # Hand coded prefix
        _prefix = self._command_defn["prefix"]
        log.debug(f"_prefix: {_prefix}")
        # Auto determined prefix - TODO
        data_length = len(_cmd) + 3
        if _type == "QUERY":
            auto_prefix = f"^P{data_length:03}"
        elif _type == "SETTER":
            auto_prefix = f"^S{data_length:03}"
        else:
            log.info(f"No type defined for command {_cmd}")
            auto_prefix = f"^P{data_length:03}"
        log.debug(f"auto_prefix: {auto_prefix}")

        _pre_cmd = bytes(_prefix, "utf-8") + _cmd
        # _pre_cmd = bytes(auto_prefix, "utf-8") + _cmd
        log.debug(f"_pre_cmd: {_pre_cmd}")

        # Determine if crc is needed or not
        CRC = True
        # For commands that dont need CRC
        if self._command_defn.get("nocrc") is True:
            CRC = False
        # for protocols that mostly dont need CRC
        if self.NOCRC:
            CRC = False
        # override to allow crc
        if self._command_defn.get("nocrc") is False:
            CRC = True
        log.debug("CRC: %s" % CRC)

        if CRC:
            # calculate the CRC
            crc_high, crc_low = crc(_pre_cmd)
            # combine byte_cmd, CRC , return
            full_command = _pre_cmd + bytes([crc_high, crc_low, 13])
        else:
            full_command = _pre_cmd + bytes([13])

        log.debug(f"full command: {full_command}")
        return full_command

    def get_responses(self, response):
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

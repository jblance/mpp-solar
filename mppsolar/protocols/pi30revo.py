import logging

from .abstractprotocol import AbstractProtocol
from .protocol_helpers import crcPI as crc
from .protocol_helpers import crc8P1 as chk

log = logging.getLogger("pi30revo")

COMMANDS = {
    "PQSE": {
        "name": "PQSE",
        "description": "Read current machine configuration information",
        "help": " -- queries the value of various metrics from the Inverter",
        "type": "QUERY",
        "crctype": "chk",
        "response": [
            [
                "multi",
                [
                    ["option", "Language", ["English", "Chinese"]],
                    [
                        "option",
                        "Work Mode",
                        [
                            "Utility Priority",
                            "Solar Priority",
                            "Battery Priority",
                            "PV+mains power+no external CT",
                            "PV+mains power+external CT",
                        ],
                    ],
                    ["option", "Input Range", ["Wide", "Narrow"]],
                    ["option", "Output Voltage", ["220V", "230V", "240V"]],
                    ["option", "Output Frequency", ["50Hz", "60Hz"]],
                    [
                        "option",
                        "Battery Type",
                        ["Lead Acid", "Lithium", "None", "Custom"],
                    ],
                ],
            ],
            ["float", "Battery Bulk Charge Voltage", "V"],
            ["float", "Battery Float Charge Voltage", "V"],
            ["float", "Battery Low Voltage Alarm Point", "V"],
            ["float", "Battery Low Voltage Cutoff Point", "V"],
            ["int", "Total Charging Current", "A"],
            ["int", "AC Charging Current", "A"],
            ["string", "Year", ""],
            ["string", "Month", ""],
            ["string", "Day", ""],
            ["string", "Hour", ""],
            ["string", "Minute", ""],
            [
                "multi",
                [
                    ["option", "Buzzer", ["Enabled", "Disabled"]],
                    ["option", "Grid", ["Not Connected", "Connected"]],
                    ["option", "Single Phase Parallel", ["Disabled", "Enabled"]],
                    ["option", "Three Phase Parallel", ["Disabled", "Enabled"]],
                    ["string", "Three Phase ID"],
                ],
            ],
            ["float", "Battery Full Recovery Point", "V"],
        ],
        "test_responses": [
            b"(000100 56.0 54.0 44.0 42.0 030 010 2018 06 01 20 00 00 00\x3c\n",
        ],
    },
    "QALL": {
        "name": "QALL",
        "description": "Current Status Data inquiry",
        "help": " -- queries the value of various metrics from the Inverter",
        "type": "QUERY",
        "crctype": "chk",
        "response": [
            ["int", "AC Input Voltage", "V"],
            ["float", "AC Input Frequency", "Hz"],
            ["int", "AC Output Voltage", "V"],
            ["float", "AC Output Frequency", "Hz"],
            ["int", "AC Output Active Power", "W"],
            ["int", "AC Output Load", "%"],
            ["float", "Battery Voltage", "V"],
            ["int", "Battery Capacity", "%"],
            ["int", "Battery Charging Current", "A"],
            ["int", "Battery Discharging Current", "A"],
            ["int", "PV Input Voltage", "V"],
            ["float", "PV Input Current", "A"],
            ["int", "PV Power", "W"],
            ["int", "Daily PV Power Generated", "WH"],
            ["int", "Total PV Power Generated", "kWH"],
            [
                "keyed",
                "Device Mode",
                {
                    "P": "Power on",
                    "S": "Standby",
                    "L": "Line",
                    "B": "Battery",
                    "F": "Fault",
                    "H": "Power saving",
                },
            ],
            [
                "keyed",
                "Warning Code",
                {
                    "00": "No warning",
                    "01": "Low battery",
                    "02": "Mains low voltage",
                    "03": "Mains high voltage",
                    "04": "Overload",
                    "05": "Over temperature",
                    "06": "Fan lock",
                    "07": "Battery overvoltage",
                    "08": "Discharge overcurrent",
                    "21": "PV undervoltage",
                    "22": "PV overvoltage",
                    "23": "PV overcurrent",
                    "24": "PV over temperature",
                    "25": "PV overload",
                    "26": "PV boost failed",
                    "39": "BMS Communication lost",
                },
            ],
            [
                "keyed",
                "Fault Code",
                {
                    "00": "No fault",
                    "01": "BUS overvoltage",
                    "02": "Inverter overvoltage",
                    "03": "Inverter low voltage",
                    "04": "BUS soft start failure",
                    "05": "Overload fault",
                    "06": "Output short circuit",
                    "07": "Low battery voltage failure",
                    "08": "Inverter soft start failure",
                    "09": "BUS low voltage",
                    "10": "Parallel failure",
                    "11": "Over temperature fault",
                    "12": "Battery over-voltage fault",
                    "13": "Phase A lost",
                    "14": "Phase B lost",
                    "15": "Phase C lost",
                    "16": "AC output voltage and frequency setting is different",
                    "17": "AC input voltage and frequency detected different",
                    "18": "Power feedback protection",
                    "19": "Firmware Version inconsistent",
                    "20": "Current sharing fault",
                    "23": "PV overcurrent",
                    "24": "PV over temperature",
                },
            ],
        ],
        "test_responses": [
            b"(000 00.0 000 00.0 0000 000 00.0 000 000 000 000 00.0 0000 000000 000000 S 00 00\x04\n",
        ],
    },
    "QMOD": {
        "name": "QMOD",
        "description": "Mode inquiry",
        "help": " -- queries the Inverter mode",
        "type": "QUERY",
        "crctype": "crc",
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
                    "H": "Power saving",
                },
            ]
        ],
        "test_responses": [
            b"(S\x64\x39\r",
        ],
    },
    "QPI": {
        "name": "QPI",
        "description": "Protocol ID inquiry",
        "help": " -- queries the device protocol ID. e.g. PI30 for HS series",
        "type": "QUERY",
        "crctype": "crc",
        "response": [
            ["string", "Protocol ID", ""],
        ],
        "test_responses": [
            b"(PI30\x9a\x0b\r",
        ],
    },
    "QPIGS": {
        "name": "QPIGS",
        "description": "General Status Parameters inquiry",
        "help": " -- queries the value of various metrics from the Inverter",
        "type": "QUERY",
        "crctype": "crc",
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
            ["float", "PV Power", "W"],
            ["float", "PV Input Voltage", "V"],
            ["float", "Battery Voltage from SCC", "V"],
            ["int", "Daily Power Generated", "WH"],
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
            ["int", "RSV1", "A"],
            ["int", "RSV2", "A"],
            ["int", "PV Input Power", "W"],
            [
                "flags",
                "Device Status2",
                ["Is Charging to Float", "Is Switched On", "Is Reserved"],
            ],
        ],
        "test_responses": [
            b"(221.0 49.9 221.0 49.9 0000 0707 012 401 00.10 012 000 0026 0000 000.0 00.10 00000 00010000 00 00 00000 010\xe9}\r"
        ],
    },
    "QPIRI": {
        "name": "QPIRI",
        "description": "Current Settings inquiry",
        "help": " -- queries the current settings from the Inverter",
        "type": "QUERY",
        "crctype": "crc",
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
            ["option", "Battery Type", ["AGM", "Flooded", "User"]],
            ["int", "Max AC Charging Current", "A"],
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
            ["int", "Max Parallel Units", "units"],
            [
                "keyed",
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
                    "Phase 2 of 2 phase output",
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
        ],
        "test_responses": [
            b"(230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10 010 1 0 0 6 01 0 0 54.0 0 1\x6F\x7E\r",
        ],
    },
}


class pi30revo(AbstractProtocol):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI30REVO"
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = ["QPIGS"]
        self.SETTINGS_COMMANDS = ["QPIRI"]
        self.DEFAULT_COMMAND = "QPI"
        # log.info(f'Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands')

    def is_CRC_valid(self, response):
        """
        Test response using CRC approach
        """
        crc_high, crc_low = crc(response[:-3])
        if response[-3:-1] == bytes([crc_high, crc_low]):
            log.debug("CRCs match")
            return True
        return False

    def is_CHK_valid(self, response):
        """
        Test response using CHK approach
        """
        checksum = chk(response[:-2])
        if response[-2:-1] == bytes([checksum]):
            log.debug("Checksums match")
            return True
        return False

    def get_responses(self, response) -> list:
        """
        Split and trim for this protocol is complicated by 2 possible crc approaches
          each with different lengths
        """
        # This protocol responses can either have a CRC or a Checksum..
        # If there is a valid checksum, assume it is using the checksum approach
        if self.is_CHK_valid(response):
            return response[1:-2].split(b" ")
        # Just use the default approach then
        # Trim leading '(' + trailing CRC and \r of response, then split
        if type(response) is str:
            return response[1:-3].split(" ")
        return response[1:-3].split(b" ")

    def check_response_valid(self, response):
        if response is None:
            return False, {"ERROR": ["No response", ""]}
        if len(response) <= 3:
            return False, {"ERROR": ["Response to short", ""]}

        # This protocol responses can either have a CRC or a Checksum...
        if b"(NAK" in response:
            return False, {"ERROR": ["NAK", ""]}

        if self.is_CHK_valid(response) or self.is_CRC_valid(response):
            return True, {}
        else:
            return False, {"ERROR": ["Invalid response CRC", ""]}

    def get_full_command(self, command) -> bytes:
        """
        Override the default get_full_command as its different for PI30REVO
        """
        log.info(f"sing protocol {self._protocol_id} with {len(self.COMMANDS)} commands")
        # These need to be set to allow other functions to work`
        self._command = command
        self._command_defn = self.get_command_defn(command)
        # End of required variables setting

        byte_cmd = bytes(command, "utf-8")
        if (
            self._command_defn
            and "crctype" in self._command_defn
            and self._command_defn["crctype"] == "chk"
        ):
            log.debug(f"Using CHK checksum approach for command {self._command}")
            checksum = chk(byte_cmd)
            log.debug(f"checksum {checksum}")
            full_command = byte_cmd + bytes([checksum]) + bytes([13])
        else:
            log.debug(f"Using PI30 CRC checksum approach for command {self._command}")
            # calculate the CRC
            crc_high, crc_low = crc(byte_cmd)
            # combine byte_cmd, CRC , return
            full_command = byte_cmd + bytes([crc_high, crc_low, 13])

        log.debug(f"full command: {full_command}")
        return full_command

""" powermon / protocols / jkserial.py """
import logging

import construct as cs

from powermon.commands.command_definition import CommandDefinition
from powermon.commands.reading_definition import ReadingType, ResponseType
from powermon.commands.result import ResultType
from powermon.commands.command import CommandType
from powermon.errors import InvalidResponse, CommandDefinitionMissing
from powermon.ports.porttype import PortType
from powermon.protocols.abstractprotocol import AbstractProtocol
from powermon.protocols.helpers import crc_jk232 as crc

log = logging.getLogger("jkserial")


# construct 'structures' to cover decoding of response packet
cell_details = cs.Struct("no" / cs.Byte, "voltage_mV" / cs.Int16ub)
all_data_response = cs.Struct(
    "stx" / cs.Const(b"NW"),
    "packet_length" / cs.Int16ub,
    "terminal_no" / cs.Bytes(4),
    "command_word" / cs.Byte,
    "frame_source" / cs.Enum(cs.Byte, BMS=0, Bluetooth=1, GPS=2, PC=3),
    "transport_type" / cs.Enum(cs.Byte, Response_Frame=1, BMS_Active_Upload=2),
    "_id" / cs.Const(b"\x79"),
    "data_length" / cs.Byte,
    "cell_count" / cs.Computed(cs.this.data_length // 3),
    "cell_array" / cs.Array(cs.this.cell_count, cell_details),
    "_id" / cs.Const(b"\x80"),
    "power_tube_temperature" / cs.Int16ub,
    "_id" / cs.Const(b"\x81"),
    "battery_box_temperature" / cs.Int16ub,
    "_id" / cs.Const(b"\x82"),
    "battery_temperature" / cs.Int16ub,
    "_id" / cs.Const(b"\x83"),
    "battery_voltage_10mV" / cs.Int16ub,
    "_id" / cs.Const(b"\x84"),
    "battery_current" / cs.BitStruct("direction" / cs.Enum(cs.Bit, discharge=0, charge=1), "current" / cs.BitsInteger(15)),  # possible 10000 - cs.Int16ub (if \xc0 = 00)
    "_id" / cs.Const(b"\x85"),
    "battery_soc" / cs.Byte,
    "_id" / cs.Const(b"\x86"),
    "number_of_temp_sensors" / cs.Byte,
    "_id" / cs.Const(b"\x87"),
    "cycle_count" / cs.Int16ub,
    "_id" / cs.Const(b"\x89"),
    "total_cycle_capacity" / cs.Int32ub,
    "_id" / cs.Const(b"\x8a"),
    "battery_strings" / cs.Int16ub,
    "_id" / cs.Const(b"\x8b"),
    "warning_messages" / cs.BitStruct(
        'reserved_2' / cs.Flag,
        'reserved_1' / cs.Flag,
        '309_b_protection' / cs.Flag,
        '309_a_protection' / cs.Flag,
        'cell_under_voltage_alarm' / cs.Flag,
        'cell_over_voltage_alarm' / cs.Flag,
        'battery_low_temperature_alarm' / cs.Flag,
        'battery_box_over_temperature_alarm' / cs.Flag,
        'cell_pressure_difference_alarm' / cs.Flag,
        'discharge_over_current_alarm' / cs.Flag,
        'charging_over_current_alarm' / cs.Flag,
        'battery_over_temperature_alarm' / cs.Flag,
        'discharge_under_voltage_alarm' / cs.Flag,
        'charging_over_voltage_alarm' / cs.Flag,
        'mos_tube_over_temperature_alarm' / cs.Flag,
        'low_capacity_alarm' / cs.Flag),
    "_id" / cs.Const(b"\x8c"),
    "status_info" / cs.BitStruct(
        cs.Padding(12),
        'battery_down' / cs.Flag,
        'equalization_switching_state' / cs.Flag,
        'discharge_mos_on' / cs.Flag,
        'charge_mos_on' / cs.Flag,),
    # "test_optional" / cs.Optional(cs.Const(b"\x8d")),
    "_id" / cs.Const(b"\x8e"),
    "battery_overvoltage_protection_10mV" / cs.Int16ub,
    "_id" / cs.Const(b"\x8f"),
    "battery_undervoltage_protection_10mV" / cs.Int16ub,
    "_id" / cs.Const(b"\x90"),
    "cell_overvoltage_protection_mV" / cs.Int16ub,
    "_id" / cs.Const(b"\x91"),
    "cell_overvoltage_protection_recovery_mV" / cs.Int16ub,
    "_id" / cs.Const(b"\x92"),
    "cell_overvoltage_protection_delay_secs" / cs.Int16ub,
    "_id" / cs.Const(b"\x93"),
    "cell_undervoltage_protection_mV" / cs.Int16ub,
    "_id" / cs.Const(b"\x94"),
    "cell_undervoltage_protection_recovery_mV" / cs.Int16ub,
    "_id" / cs.Const(b"\x95"),
    "cell_undervoltage_protection_delay_secs" / cs.Int16ub,
    "_id" / cs.Const(b"\x96"),
    "cell_differential_protection_mV" / cs.Int16ub,
    "_id" / cs.Const(b"\x97"),
    "discharge_protection_current_A" / cs.Int16ub,
    "_id" / cs.Const(b"\x98"),
    "discharge_protection_current_delay_secs" / cs.Int16ub,
    "_id" / cs.Const(b"\x99"),
    "charge_protection_current_A" / cs.Int16ub,
    "_id" / cs.Const(b"\x9a"),
    "charge_protection_current_delay_secs" / cs.Int16ub,
    "_id" / cs.Const(b"\x9b"),
    "equalization_starting_voltage_mV" / cs.Int16ub,

    "rest" / cs.Bytes(93),  # TODO: add rest of packet

    "_id" / cs.Const(b"\xb7"),
    "software_id" / cs.Bytes(15),
    "_id" / cs.Const(b"\xb8"),
    "start_calibration" / cs.Enum(cs.Byte, StartCalibration=1, CloseCalibration=0),
    "_id" / cs.Const(b"\xb9"),
    "battery_capacity_Ah" / cs.Int32ub,
    "_id" / cs.Const(b"\xba"),
    "manufacturer_name" / cs.Bytes(24),
    "_id" / cs.Const(b"\xc0"),
    "protocol_version" / cs.Int8ub,
    "record_number" / cs.Bytes(4),
    "end_of_identity" / cs.Const(b"h"),
    "checksum" / cs.Bytes(4)
)

COMMANDS = {
    "all_data": {
        "name": "all_data",
        "description": "Get All BMS Data",
        "help": " -- Get All BMS Data",
        "construct": all_data_response,
        "command_type": CommandType.SERIAL_READONLY,
        "command_code": "00",
        "result_type": ResultType.CONSTRUCT,
        "reading_definitions": [
            {"index": "cell_count", "description": "Cell Count"},
            {"index": "cell_1_voltage", "description": "Cell 1 Voltage", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "cell_2_voltage", "description": "Cell 2 Voltage", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "cell_3_voltage", "description": "Cell 3 Voltage", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "cell_4_voltage", "description": "Cell 4 Voltage", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "cell_5_voltage", "description": "Cell 5 Voltage", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "cell_6_voltage", "description": "Cell 6 Voltage", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "cell_7_voltage", "description": "Cell 7 Voltage", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "cell_8_voltage", "description": "Cell 8 Voltage", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "cell_9_voltage", "description": "Cell 9 Voltage", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "cell_10_voltage", "description": "Cell 10 Voltage", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "cell_11_voltage", "description": "Cell 11 Voltage", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "cell_12_voltage", "description": "Cell 12 Voltage", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "cell_13_voltage", "description": "Cell 13 Voltage", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "cell_14_voltage", "description": "Cell 14 Voltage", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "cell_15_voltage", "description": "Cell 15 Voltage", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "cell_16_voltage", "description": "Cell 16 Voltage", "reading_type": ReadingType.MILLI_VOLTS},

            {"index": "power_tube_temperature", "description": "MOS Temperature", "reading_type": ReadingType.TEMPERATURE},
            {"index": "battery_box_temperature", "description": "Battery Box Temperature", "reading_type": ReadingType.TEMPERATURE},
            {"index": "battery_temperature", "description": "Battery Temperature", "reading_type": ReadingType.TEMPERATURE},
            {"index": "number_of_temp_sensors", "description": "Number of Temperature Sensors"},

            {"index": "battery_voltage_10mV", "description": "Battery Voltage", "reading_type": ReadingType.VOLTS, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/100"},
            {"index": "direction", "description": "direction", "response_type": ResponseType.STRING},
            {"index": "current", "description": "Battery Current", "reading_type": ReadingType.CURRENT, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/100"},
            {"index": "protocol_version", "description": "Protocol Version", "response_type": ResponseType.STRING},
            {"index": "battery_soc", "description": "Battery State of Charge", "reading_type": ReadingType.PERCENTAGE},
            {"index": "cycle_count", "description": "Battery Cycle Count"},
            {"index": "battery_strings", "description": "Battery Strings"},
            {"index": "total_cycle_capacity", "description": "Total Cycle Count Capacity", "reading_type": ReadingType.ENERGY},
            {"index": "battery_capacity_Ah", "description": "Battery Capacity", "reading_type": ReadingType.ENERGY},

            {"index": "software_id", "description": "Software ID", "response_type": ResponseType.BYTES},
            {"index": "manufacturer_name", "description": "Manufacturer Name", "response_type": ResponseType.TEMPLATE_BYTES, "format_template" : "r.removeprefix('Input Userda')"},

            {"index": "charge_mos_on", "description": "Charge MOS On", "response_type": ResponseType.BOOL},
            {"index": "discharge_mos_on", "description": "Discharge MOS On", "response_type": ResponseType.BOOL},
            {"index": "equalization_switching_state", "description": "Equalization Switching State", "response_type": ResponseType.BOOL},
            {"index": "equalization_starting_voltage_mV", "description": "Equalization Starting Voltage Setting", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "battery_down", "description": "Battery Down", "response_type": ResponseType.BOOL},
            {"index": "start_calibration", "description": "Start Calibration", "response_type": ResponseType.STRING},
            {"index": "warning_messages", "description": "Warning Messages", "reading_type": ReadingType.HEX_STR, "response_type": ResponseType.INT},

            {"index": "low_capacity_alarm", "description": "Low Capacity Alarm", "response_type": ResponseType.BOOL},
            {"index": "mos_tube_over_temperature_alarm", "description": "MOS Tube Over Temperature Alarm", "response_type": ResponseType.BOOL},
            {"index": "charging_over_voltage_alarm", "description": "charging_over_voltage_alarm", "response_type": ResponseType.BOOL},
            {"index": "discharge_under_voltage_alarm", "description": "discharge_under_voltage_alarm", "response_type": ResponseType.BOOL},
            {"index": "battery_over_temperature_alarm", "description": "battery_over_temperature_alarm", "response_type": ResponseType.BOOL},
            {"index": "charging_over_current_alarm", "description": "charging_over_current_alarm", "response_type": ResponseType.BOOL},
            {"index": "discharge_over_current_alarm", "description": "discharge_over_current_alarm", "response_type": ResponseType.BOOL},
            {"index": "cell_pressure_difference_alarm", "description": "cell_pressure_difference_alarm", "response_type": ResponseType.BOOL},
            {"index": "battery_box_over_temperature_alarm", "description": "battery_box_over_temperature_alarm", "response_type": ResponseType.BOOL},
            {"index": "battery_low_temperature_alarm", "description": "battery_low_temperature_alarm", "response_type": ResponseType.BOOL},
            {"index": "cell_over_voltage_alarm", "description": "cell_over_voltage_alarm", "response_type": ResponseType.BOOL},
            {"index": "cell_under_voltage_alarm", "description": "cell_under_voltage_alarm", "response_type": ResponseType.BOOL},
            {"index": "309_a_protection", "description": "309_a_protection", "response_type": ResponseType.BOOL},
            {"index": "309_b_protection", "description": "309_b_protection", "response_type": ResponseType.BOOL},

            {"index": "battery_overvoltage_protection_10mV", "description": "Battery Overvoltage Protection Setting", "reading_type": ReadingType.VOLTS, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/100"},
            {"index": "battery_undervoltage_protection_10mV", "description": "Battery Undervoltage Protection Setting", "reading_type": ReadingType.VOLTS, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/100"},
            {"index": "cell_overvoltage_protection_mV", "description": "Cell Overvoltage Protection Setting", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "cell_overvoltage_protection_recovery_mV", "description": "Cell Overvoltage Protection Recovery Setting", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "cell_overvoltage_protection_delay_secs", "description": "Cell Overvoltage Protection Recovery Delay Setting", "reading_type": ReadingType.TIME_SECONDS},
            {"index": "cell_undervoltage_protection_mV", "description": "Cell Undervoltage Protection Setting", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "cell_undervoltage_protection_recovery_mV", "description": "Cell Undervoltage Protection Recovery Setting", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "cell_undervoltage_protection_delay_secs", "description": "Cell Undervoltage Protection Recovery Delay Setting", "reading_type": ReadingType.TIME_SECONDS},
            {"index": "cell_differential_protection_mV", "description": "Cell Voltage Difference Protection Setting", "reading_type": ReadingType.MILLI_VOLTS},
            {"index": "charge_protection_current_A", "description": "Charge Current Protection Setting", "reading_type": ReadingType.CURRENT},
            {"index": "charge_protection_current_delay_secs", "description": "Charge Current Protection Delay Setting", "reading_type": ReadingType.TIME_SECONDS},
            {"index": "discharge_protection_current_A", "description": "Discharge Current Protection Setting", "reading_type": ReadingType.CURRENT},
            {"index": "discharge_protection_current_delay_secs", "description": "Discharge Current Protection Delay Setting", "reading_type": ReadingType.TIME_SECONDS},

            # fields to ignore
            {"index": "stx", "description": "", "reading_type": ReadingType.IGNORE},
            {"index": "_id", "description": "", "reading_type": ReadingType.IGNORE},
            {"index": "packet_length", "description": "", "reading_type": ReadingType.IGNORE},
            {"index": "terminal_no", "description": "", "reading_type": ReadingType.IGNORE},
            {"index": "command_word", "description": "", "reading_type": ReadingType.IGNORE},
            {"index": "frame_source", "description": "", "reading_type": ReadingType.IGNORE},
            {"index": "transport_type", "description": "", "reading_type": ReadingType.IGNORE},
            {"index": "data_length", "description": "", "reading_type": ReadingType.IGNORE},
            {"index": "record_number", "description": "", "reading_type": ReadingType.IGNORE},
            {"index": "end_of_identity", "description": "", "reading_type": ReadingType.IGNORE},
            {"index": "checksum", "description": "", "reading_type": ReadingType.IGNORE},
            {"index": "reserved_1", "description": "", "reading_type": ReadingType.IGNORE},
            {"index": "reserved_2", "description": "", "reading_type": ReadingType.IGNORE},
            {"index": "rest", "description": "", "reading_type": ReadingType.IGNORE},

            # ["BigHex2Short:(r&0x7FFF)/100*(((r&0x8000)>>15)*2-1)", 2, "Battery_Current", "A"],

        ],
        "test_responses": [
            b'NW\x01\x1b\x00\x00\x00\x00\x03\x00\x01y*\x01\x0f\x90\x02\x0f\x91\x03\x0f\x94\x04\x0f\x8e\x05\x0f\x92\x06\x0f\x91\x07\x0f\x91\x08\x0f\x91\t\x0f\x93\n\x0f\x8e\x0b\x0f\x91\x0c\x0f\x90\r\x0f\x90\x0e\x0f\x8d\x80\x00!\x81\x00\x1c\x82\x00\x1e\x83\x15\xca\x84\x81\xc5\x85d\x86\x02\x87\x00\x19\x89\x00\x00\x16\xda\x8a\x00\x0e\x8b\x00\x00\x8c\x00\x03\x8e\x16\xb2\x8f\x10\xf4\x90\x106\x91\x10\x04\x92\x00\x05\x93\x0c\x1c\x94\x0c\x80\x95\x00\x05\x96\x01,\x97\x00n\x98\x01,\x99\x00U\x9a\x00\x1e\x9b\x0b\xb8\x9c\x002\x9d\x01\x9e\x00Z\x9f\x00F\xa0\x00d\xa1\x00d\xa2\x00\x14\xa3\x00<\xa4\x00<\xa5\x00\x01\xa6\x00\x03\xa7\xff\xec\xa8\xff\xf6\xa9\x0e\xaa\x00\x00\x00\xea\xab\x01\xac\x01\xad\x047\xae\x01\xaf\x01\xb0\x00\n\xb1\x14\xb2123456\x00\x00\x00\x00\xb3\x00\xb4Input Us\xb52306\xb6\x00\x01\x82\xe3\xb711.XW_S11.261__\xb8\x00\xb9\x00\x00\x00\xea\xbaInput UserdaJK_B1A20S15P\xc0\x01\x00\x00\x00\x00h\x00\x00Q\xd6',
            bytes.fromhex("4e 57 00 fd 00 00 00 00 06 00 01 79 0c 01 0d 06 02 0d 06 03 0d 07 04 0d 07 80 00 10 81 00 0e 82 00 0d 83 05 35 84 00 00 85 62 86 02 87 00 00 89 00 00 00 05 8a 00 04 8b 00 03 8c 00 03 8e 05 a0 8f 04 10 90 0e 10 91 0d de 92 00 05 93 0a 28 94 0a 5a 95 00 05 96 01 2c 97 00 78 98 00 1e 99 00 3c 9a 00 1e 9b 0d 48 9c 00 05 9d 01 9e 00 50 9f 00 41 a0 00 64 a1 00 64 a2 00 14 a3 00 32 a4 00 37 a5 00 03 a6 00 08 a7 ff ec a8 ff f6 a9 04 aa 00 00 01 31 ab 01 ac 01 ad 03 7e ae 01 af 00 b0 00 0a b1 14 b2 35 33 31 34 00 00 00 00 00 00 b3 00 b4 49 6e 70 75 74 20 55 73 b5 32 33 31 32 b6 00 00 36 a6 b7 31 31 2e 58 57 5f 53 31 31 2e 32 31 48 5f 5f b8 00 b9 00 00 01 31 ba 49 6e 70 75 74 20 55 73 65 72 64 61 45 64 64 69 65 42 6c 75 65 42 4d 53 c0 01 00 00 00 00 68 00 00 44 6f"),
        ],
    },
    "battery_voltage": {
        "name": "battery_voltage",
        "description": "Get the battery voltage",
        "help": " -- Get the battery voltage",
        # "construct": balancer_data_response,
        "command_type": CommandType.JKSERIAL_READ,
        "command_code": "83",
        "result_type": ResultType.SINGLE,
        "reading_definitions": [{"description": "Battery Voltage"}],
        "test_responses": []}
}


class JkSerial(AbstractProtocol):
    """ JKBMS TTL serial communication protocol handler """
    def __str__(self):
        return "JKBMS TTL serial communication protocol handler"

    def __init__(self) -> None:
        super().__init__()
        self._protocol_id = b"JKSERIAL"
        self.add_command_definitions(COMMANDS)
        self.add_supported_ports([PortType.SERIAL])
        self.check_definitions_count(expected=2)

    def check_valid(self, response: str, command_definition: CommandDefinition = None) -> bool:
        """ check response is valid """
        log.debug("check valid for %s, definition: %s", response, command_definition)
        if response is None:
            raise InvalidResponse("Response is None")
        if len(response) <= 3:
            raise InvalidResponse("Response is too short")
        # check start bytes = 0x4e57 / NW
        if response[0:2] != b"NW":
            raise InvalidResponse(f"Start bytes ({response[0:2]} not 'NW')")
        return True

    def check_crc(self, response: str, command_definition: CommandDefinition = None):
        return True

    def trim_response(self, response: str, command_definition: CommandDefinition = None) -> str:
        """ Remove extra characters from response """
        log.debug("trim %s, definition: %s", response, command_definition)
        return response

    def get_full_command(self, command) -> bytes:
        """
        Override the default get_full_command as its different
        """
        log.info("Using protocol: %s with %i commands", self.protocol_id, len(self.command_definitions))
        command_defn = self.get_command_definition(command)
        # raise error is no command_defn found
        if command_defn is None:
            raise CommandDefinitionMissing(f"No definition found in JKSERIAL for {command}")

        # command byte: 0x01 (activation), 0x02 (write), 0x03 (read), 0x05 (password), 0x06 (read all)
        match command_defn.command_type:
            case CommandType.SERIAL_READONLY:
                command_byte = 0x06
            case CommandType.JKSERIAL_ACTIVATION:
                command_byte = 0x01
            case CommandType.JKSERIAL_SETTER:
                command_byte = 0x02
            case _:
                command_byte = 0x03

        # Read basic information and status
        # full command is 21 bytes long
        cmd = bytearray(21)
        command_code = int(command_defn.command_code, 16)

        # start bit  0x4E
        cmd[0] = 0x4E                         # start sequence
        cmd[1] = 0x57                         # start sequence
        cmd[2] = 0x00                         # data length lb
        cmd[3] = 0x13                         # data length hb
        cmd[4] = 0x00                         # bms terminal number
        cmd[5] = 0x00                         # bms terminal number
        cmd[6] = 0x00                         # bms terminal number
        cmd[7] = 0x00                         # bms terminal number
        cmd[8] = command_byte
        cmd[9] = 0x03                         # frame source: 0x00 (bms), 0x01 (bluetooth), 0x02 (gps), 0x03 (computer)
        cmd[10] = 0x00                        # frame type: 0x00 (read data), 0x01 (reply frame), 0x02 (BMS active upload)
        cmd[11] = command_code                # register: 0x00 (read all registers), 0x8E...0xBF (holding registers)
        cmd[12] = 0x00                        # record number
        cmd[13] = 0x00                        # record number
        cmd[14] = 0x00                        # record number
        cmd[15] = 0x00                        # record number
        cmd[16] = 0x68                        # end sequence
        cmd[17] = 0x00                        # crc unused
        cmd[18] = 0x00                        # crc unused
        crc_high, crc_low = crc(cmd[0:17])
        cmd[19] = crc_high
        cmd[20] = crc_low

        log.debug("cmd with crc: %s", cmd)
        return cmd

    def split_response(self, response: str, command_definition: CommandDefinition = None) -> list:
        """ split response into individual items, return as ordered list or list of tuples """
        result_type = getattr(command_definition, "result_type", None)
        log.debug("jkserial splitting %s, result_type %s", response, result_type)
        # build a list of (index, value) tuples, after parsing with a construct
        responses = []
        # parse with construct
        result = command_definition.construct.parse(response)
        # print(result)
        for x in result:
            # if x == "cell_array":
            #     print(x, result[x])
            match type(result[x]):
                case cs.ListContainer:
                    # print(result[x])
                    if x == "cell_array":
                        for _container in result[x]:
                            key = f"cell_{_container['no']}_voltage"
                            value = _container['voltage_mV']
                            responses.append((key, value))
                case cs.Container:
                    for y in result[x]:
                        if y != "_io":
                            key = y
                            value = result[x][y]
                            responses.append((key, value))
                case _:
                    if x != "_io":
                        key = x
                        value = result[x]
                        responses.append((key, value))
            # case _:
            #     responses = response.split()
        log.debug("responses: '%s'", responses)
        return responses

""" powermon / protocols / jkserial.py """
import logging

import construct as cs

from powermon.commands.command_definition import CommandDefinition
from powermon.commands.reading_definition import ReadingType, ResponseType
from powermon.commands.result import ResultType
from powermon.errors import InvalidResponse
from powermon.ports.porttype import PortType
from powermon.protocols.abstractprotocol import AbstractProtocol
from powermon.protocols.helpers import crc_jk232 as crc

log = logging.getLogger("jk232")

cell_details = cs.Struct("no" / cs.Byte, "voltage_mV" / cs.Int16ub)
balancer_data_response = cs.Struct(
    "stx" / cs.Const(b"NW"),
    "length" / cs.Int16ub,
    "terminal-no" / cs.Bytes(4),
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
    "warning_messages" / cs.Bytes(2),
    "_id" / cs.Const(b"\x8c"),
    "status_info" / cs.BitStruct(cs.Padding(12),
        'battery_down' / cs.Flag,
        'equalization_switching_state' / cs.Flag,
        'discharge_mos_on' / cs.Flag,
        'charge_mos_on' / cs.Flag,),
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

    "rest" / cs.Bytes(93),

    "_id" / cs.Const(b"\xb7"),
    "software_id" / cs.Bytes(15),
    "_id" / cs.Const(b"\xb8"),
    "start_calibration" / cs.Byte,
    "_id" / cs.Const(b"\xb9"),
    "battery_capacity_Ah" / cs.Int32ub,
    "_id" / cs.Const(b"\xba"),
    "manufacturer_name" / cs.Bytes(24),
    "_id" / cs.Const(b"\xc0"),
    "agreement_no" / cs.Bytes(1),
    "record_number" / cs.Bytes(4),
    "end_of_identity" / cs.Const(b"h"),
    "checksum" / cs.Bytes(4)
)

COMMANDS = {
    "getBalancerData": {
        "name": "getBalancerData",
        # "command_code": "00",
        "description": "Get Balancer Data",
        "help": " -- Get Balancer Data",
        # "type": "QUERY",
        "construct": balancer_data_response,
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

            {"index": "power_tube_temperature", "description": "MOS Temperature","reading_type": ReadingType.TEMPERATURE},
            {"index": "battery_box_temperature", "description": "Battery Box Temperature","reading_type": ReadingType.TEMPERATURE},
            {"index": "battery_temperature", "description": "Battery Temperature","reading_type": ReadingType.TEMPERATURE},

            {"index": "battery_voltage_10mV", "description": "Battery Voltage", "reading_type": ReadingType.VOLTS, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/100"},
            {"index": "direction", "description": "direction", "response_type": ResponseType.STRING},

            # ["discard", 1, "MOS_Temp", ""],
            # ["BigHex2Short", 2, "MOS_Temp", "°C"],
            # ["discard", 1, "Battery_T1", ""],
            # ["BigHex2Short", 2, "Battery_T1", "°C"],
            # ["discard", 1, "Battery_T2", ""],
            # ["BigHex2Short", 2, "Battery_T2", "°C"],
            # ["discard", 1, "Battery_Voltage", ""],
            # ["BigHex2Short:r/100", 2, "Battery_Voltage", "V"],
            # ["discard", 1, "Battery_Current", ""],
            # ["BigHex2Short:(r&0x7FFF)/100*(((r&0x8000)>>15)*2-1)", 2, "Battery_Current", "A"],
            # ["discard", 1, "Percent_Remain", ""],
            # ["Hex2Int", 1, "Percent_Remain", "%"],
            # ["discard", 2, "Number of battery sensors", ""],  # useless so dropped
            # ["discard", 1, "Cycle_Count", ""],
            # ["BigHex2Short", 2, "Cycle_Count", ""],
            # ["discard", 1, "Total_capacity", ""],
            # ["BigHex2Float", 4, "Total_capacity", "Ahr"], # Needs other formula
            # ["discard", 3, "Total number of battery strings", ""],  # dropping
            # ["discard", 1, "Battery Warning Message", ""],
            # ["Hex2Str", 2, "Battery Warning Message", ""],
            # ["discard", 1, "Battery status information", ""],
            # ["Hex2Str", 2, "Battery status information", ""],
            # ["discard", 15 * 3, "settings", ""],
            # ["discard", 1, "Balancer Active", ""],
            # ["Hex2Int", 1, "Balancer Active", ""],
            # ["discard", 7 * 3, "more settings", ""],
            # ["discard", 4 * 3, "temp settings", ""],
            # ["discard", 2, "string count", ""], # dropping
            # ["discard", 1, "Capacity Setting", ""],
            # ["BigHex2Float", 4, "Capacity Setting", "Ahr"],
            # ["discard", 1, "Charge Enabled", ""],
            # ["Hex2Int", 1, "Charge Enabled", ""],
            # ["discard", 1, "Discharge Enabled", ""],
            # ["Hex2Int", 1, "Discharge Enabled", ""],
            # ["discard", 20 + 96, "remaining data", ""]
        ],
        "test_responses": [
            #bytes.fromhex("4e 57 01 1b 00 00 00 00 03 00 01 79 2a 01 0f 91 02 0f 94 03 0f 99 04 0f 92 05 0f 94 06 0f 94 07 0f 94 08 0f 91 09 0f 96 0a 0f 91 0b 0f 92 0c 0f 93 0d"),
            b'NW\x01\x1b\x00\x00\x00\x00\x03\x00\x01y*\x01\x0f\x90\x02\x0f\x91\x03\x0f\x94\x04\x0f\x8e\x05\x0f\x92\x06\x0f\x91\x07\x0f\x91\x08\x0f\x91\t\x0f\x93\n\x0f\x8e\x0b\x0f\x91\x0c\x0f\x90\r\x0f\x90\x0e\x0f\x8d\x80\x00!\x81\x00\x1c\x82\x00\x1e\x83\x15\xca\x84\x81\xc5\x85d\x86\x02\x87\x00\x19\x89\x00\x00\x16\xda\x8a\x00\x0e\x8b\x00\x00\x8c\x00\x03\x8e\x16\xb2\x8f\x10\xf4\x90\x106\x91\x10\x04\x92\x00\x05\x93\x0c\x1c\x94\x0c\x80\x95\x00\x05\x96\x01,\x97\x00n\x98\x01,\x99\x00U\x9a\x00\x1e\x9b\x0b\xb8\x9c\x002\x9d\x01\x9e\x00Z\x9f\x00F\xa0\x00d\xa1\x00d\xa2\x00\x14\xa3\x00<\xa4\x00<\xa5\x00\x01\xa6\x00\x03\xa7\xff\xec\xa8\xff\xf6\xa9\x0e\xaa\x00\x00\x00\xea\xab\x01\xac\x01\xad\x047\xae\x01\xaf\x01\xb0\x00\n\xb1\x14\xb2123456\x00\x00\x00\x00\xb3\x00\xb4Input Us\xb52306\xb6\x00\x01\x82\xe3\xb711.XW_S11.261__\xb8\x00\xb9\x00\x00\x00\xea\xbaInput UserdaJK_B1A20S15P\xc0\x01\x00\x00\x00\x00h\x00\x00Q\xd6',
            bytes.fromhex("4e 57 00 fd 00 00 00 00 06 00 01 79 0c 01 0d 06 02 0d 06 03 0d 07 04 0d 07 80 00 10 81 00 0e 82 00 0d 83 05 35 84 00 00 85 62 86 02 87 00 00 89 00 00 00 05 8a 00 04 8b 00 00 8c 00 03 8e 05 a0 8f 04 10 90 0e 10 91 0d de 92 00 05 93 0a 28 94 0a 5a 95 00 05 96 01 2c 97 00 78 98 00 1e 99 00 3c 9a 00 1e 9b 0d 48 9c 00 05 9d 01 9e 00 50 9f 00 41 a0 00 64 a1 00 64 a2 00 14 a3 00 32 a4 00 37 a5 00 03 a6 00 08 a7 ff ec a8 ff f6 a9 04 aa 00 00 01 31 ab 01 ac 01 ad 03 7e ae 01 af 00 b0 00 0a b1 14 b2 35 33 31 34 00 00 00 00 00 00 b3 00 b4 49 6e 70 75 74 20 55 73 b5 32 33 31 32 b6 00 00 36 a6 b7 31 31 2e 58 57 5f 53 31 31 2e 32 31 48 5f 5f b8 00 b9 00 00 01 31 ba 49 6e 70 75 74 20 55 73 65 72 64 61 45 64 64 69 65 42 6c 75 65 42 4d 53 c0 01 00 00 00 00 68 00 00 44 6f"),
        ],
    },
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
        self.STATUS_COMMANDS = ["getBalancerData",]
        self.SETTINGS_COMMANDS = []
        self.DEFAULT_COMMAND = "getBalancerData"
        self.check_definitions_count(expected=1)

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
        # These need to be set to allow other functions to work`
        self._command = command
        self._command_defn = self.get_command_definition(command)
        # End of required variables setting
        if self._command_defn is None:
            # Maybe return a default here?
            return None

        # Read basic information and status
        # full command is 21 bytes long
        cmd = bytearray(21)
        # command_code = int(self._command_defn["command_code"], 16)
        command_code = int("00")

        # start bit  0x4E
        cmd[0] = 0x4E                         # start sequence
        cmd[1] = 0x57                         # start sequence
        cmd[2] = 0x00                         # data length lb
        cmd[3] = 0x13                         # data length hb
        cmd[4] = 0x00                         # bms terminal number
        cmd[5] = 0x00                         # bms terminal number
        cmd[6] = 0x00                         # bms terminal number
        cmd[7] = 0x00                         # bms terminal number
        # if self._command_defn["type"] == "SETTER":
        if False:
            cmd[8] = 0x02                     # command word: 0x01 (activation), 0x02 (write), 0x03 (read), 0x05 (password), 0x06 (read all)
        else:
            cmd[8] = 0x03
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

        log.debug(f"cmd with crc: {cmd}")
        return cmd

    def split_response(self, response: str, command_definition: CommandDefinition = None) -> list:
        """ split response into individual items, return as ordered list or list of tuples """
        result_type = getattr(command_definition, "result_type", None)
        log.debug("jkserial splitting %s, result_type %s", response, result_type)
        # match result_type:
        #     case None:
        #         responses = []
        #     case ResultType.ACK | ResultType.SINGLE | ResultType.MULTIVALUED:
        #         responses = response
        #     case ResultType.SLICED:
        #         responses = []
        #         for position in range(command_definition.reading_definition_count()):
        #             rd = command_definition.get_reading_definition(position=position)
        #             responses.append(response[rd.slice_array[0]:rd.slice_array[1]])
        #     case ResultType.VED_INDEXED:
        #         # build a list of (index,value) tuples
        #         responses = []
        #         for item in response.split(b'\r\n'):
        #             try:
        #                 key, value = item.split(b'\t')
        #             except ValueError:
        #                 continue
        #             if isinstance(key, bytes):
        #                 key = key.decode()
        #             responses.append((key.strip(), value.strip()))
            # case ResultType.CONSTRUCT:
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
                    #print(f"{x}:listcontainer")
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

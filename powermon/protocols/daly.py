""" protocols / ved.py """
import logging

import construct as cs

from powermon.commands.command import CommandType
from powermon.commands.command_definition import CommandDefinition
from powermon.commands.reading_definition import ReadingType, ResponseType
from powermon.commands.result import ResultType
# from powermon.errors import CommandError, InvalidCRC, InvalidResponse
from powermon.ports.porttype import PortType
from powermon.protocols.abstractprotocol import AbstractProtocol

log = logging.getLogger("daly")

soc_construct = cs.Struct(
    "start_flag" / cs.Bytes(1),
    "module_address" / cs.Bytes(1),
    "command_id" / cs.Bytes(1),
    "data_length" / cs.Byte,
    "battery_voltage" / cs.Int16ub,
    "acquistion_voltage" / cs.Int16ub,
    "current" / cs.Int16ub,
    "soc" / cs.Int16ub,
    "checksum" / cs.Bytes(1)
)

COMMANDS = {
    "SOC": {
        "name": "SOC",
        "description": "State of Charge",
        "help": " -- display the battery state of charge",
        # "type": "DALY",
        "command_type": CommandType.SERIAL_READ_UNTIL_DONE,
        "command_code": "90",
        "result_type": ResultType.CONSTRUCT,
        "construct": soc_construct,
        "construct_min_response": 13,
        "reading_definitions": [
            {"index": "start_flag", "description": "start flag", "reading_type": ReadingType.IGNORE, "response_type": ResponseType.HEX_CHAR},
            {"index": "module_address", "description": "module address", "reading_type": ReadingType.IGNORE, "response_type": ResponseType.HEX_CHAR},
            {"index": "command_id", "description": "command id", "reading_type": ReadingType.IGNORE, "response_type": ResponseType.HEX_CHAR},
            {"index": "data_length", "description": "data length", "reading_type": ReadingType.IGNORE},
            {"index": "battery_voltage", "description": "Battery Bank Voltage", "reading_type": ReadingType.VOLTS, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/10"},
            {"index": "acquistion_voltage", "description": "acquistion", "reading_type": ReadingType.VOLTS, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/10"},
            {"index": "current", "description": "Current", "reading_type": ReadingType.CURRENT, "response_type": ResponseType.TEMPLATE_INT, "format_template": "(r-30000)/10"},
            {"index": "soc", "description": "SOC", "reading_type": ReadingType.PERCENTAGE, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/10"},
            {"index": "checksum", "description": "checksum", "reading_type": ReadingType.IGNORE, "response_type": ResponseType.HEX_CHAR}],
        "test_responses": [
            b"\xa5\x01\x90\x08\x02\x10\x00\x00uo\x03\xbc\xf3",
            b"\xa5\x01\x90\x08\x02\x14\x00\x00uE\x03x\x89",
            b"\xa5\x01\x90\x08\x01\t\x00\x00u\xcf\x03\n\x99",
            b"",
        ],
    },
}


class Daly(AbstractProtocol):
    """
    Daly BMS protocol handler
    """

    def __str__(self):
        return "DALY protocol handler for DALY BMS"

    def __init__(self) -> None:
        super().__init__()
        self.protocol_id = b"DALY"
        self.add_command_definitions(COMMANDS)
        self.add_supported_ports([PortType.SERIAL, PortType.USB])
        self.check_definitions_count(expected=None)

    def get_full_command(self, command) -> bytes:
        """
        Override the default get_full_command
        """
        log.info("Using protocol %s with %i commands", self.protocol_id, len(self.command_definitions))

        command_definition : CommandDefinition = self.get_command_definition(command)
        if command_definition is None:
            return None

        # DALY commands
        #
        #
        # 95 -> a58095080000000000000000c2
        #       a58090080000000000000000bd
        source = 0x80  # 4 = USB, 8 = Bluetooth
        command = command_definition.command_code
        data_length = 8
        full_command = bytearray()
        full_command.append(0xa5)  # start flag
        full_command.append(source)
        full_command.append(bytes.fromhex(command_definition.command_code)[0])
        full_command.append(data_length)
        full_command += bytearray(data_length)
        full_command.append(sum(full_command) & 0xFF)
        full_command.append(10)
        full_command = bytes(full_command)
        log.debug("full_command: %s", full_command)
        return full_command

        # command_type = command_definition.command_type
        # match command_type:
        #     case CommandType.VICTRON_GET:
        #         # command components
        #         raw_command_code = command_definition.command_code  # eg 1000 for batteryCapacity
        #         if raw_command_code is None:
        #             raise CommandError(f"command_code not found for {command=} - check protocol definition for this command")
        #         command_code = f"{unpack('<h', bytes.fromhex(raw_command_code))[0]:04X}"
        #         flags = "00"

        #         # build command
        #         cmd = f"{command_type.value}{command_code}{flags}"
        #         # pad cmd and convert to bytes and determine checksum
        #         checksum = victron_checksum(bytes.fromhex(f"0{cmd}"))

        #         # build full command
        #         cmd = f":{cmd}{checksum:02X}\n".encode()
        #         log.debug("full command: %s", cmd)
        #         return cmd
        #     case CommandType.VICTRON_LISTEN:
        #         # Just listen - dont need to send a command
        #         log.debug("command is LISTEN type so returning %s", command_type)
        #         return command_type
        # raise CommandError(f"unable to generate full command for {command}, type {command_type} - is the definition wrong or CommandType not implemented?")

    def check_valid(self, response: str, command_definition: CommandDefinition = None) -> bool:
        """ check response is valid """
        log.debug("check valid for %s, definition: %s", response, command_definition)
        return True
        # if response is None:
        #     raise InvalidResponse("Response is None")
        # if len(response) <= 3:
        #     raise InvalidResponse("Response is too short")
        # command_type = command_definition.command_type
        # match command_type:
        #     case CommandType.VICTRON_GET:
        #         if response.count(b':') != 1:
        #             raise InvalidResponse("Response incomplete - missing ':'")
        # return True

    def check_crc(self, response: str, command_definition: CommandDefinition = None) -> bool:
        """ crc check, needs override in protocol """
        log.debug("checking crc for %s", response)
        return True
        # command_type = command_definition.command_type
        # match command_type:
        #     case CommandType.VICTRON_GET:
        #         # HEX protocol response
        #         log.debug("checking validity of '%s'", response)
        #         _r = response.split(b":")[1][:-1].decode()
        #         # print(f"trimmed response {_r}")
        #         _r = f"0{_r}"
        #         # print(f"padded response {_r}")
        #         _r = bytes.fromhex(_r)
        #         # print(f"bytes response {_r}")
        #         data = _r[:-1]
        #         checksum = _r[-1:][0]
        #         expected_checksum = victron_checksum(data)
        #         if expected_checksum == checksum:
        #             log.debug("VED Hex Checksum matches in response '%s' checksum:'%s'", response, checksum)
        #             return True
        #         else:
        #             # print("VED Hex Checksum does not match")
        #             raise InvalidCRC(f"response has invalid CRC - got '\\x{checksum:02x}', calculated '\\x{expected_checksum:02x}")
        #     case CommandType.VICTRON_LISTEN:
        #         return True
        # return True

    def trim_response(self, response: str, command_definition: CommandDefinition = None) -> str:
        """ Remove extra characters from response """
        log.debug("response: %s", response)
        return response
        # command_type = command_definition.command_type
        # _ret = None
        # match command_type:
        #     case CommandType.VICTRON_GET:
        #         # HEX response, e.g. b":70010007800C6\n"
        #         _ret = response.split(b":")[1][:-3]
        #     case CommandType.VICTRON_LISTEN:
        #         # VEDTEXT response, return the lot
        #         _ret = response
        # log.debug("trim_response: %s", _ret)
        # return _ret

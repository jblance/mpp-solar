""" tests / pmon / unit / test_protocol_daly.py """
import unittest
import construct as cs

from powermon.commands.command_definition import CommandDefinition
from powermon.commands.result import ResultType
from powermon.commands.command import CommandType
from powermon.commands.reading_definition import ReadingType, ResponseType
from powermon.errors import InvalidResponse
from powermon.protocols import get_protocol_definition


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

command_definitions_config = {
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
        {"index": "checksum", "description": "checksum", "reading_type": ReadingType.IGNORE, "response_type": ResponseType.HEX_CHAR}]}
cd = CommandDefinition.from_config(command_definitions_config)
cd.construct = soc_construct
cd.construct_min_response = 13
protocol = get_protocol_definition(protocol="daly")


class TestProtocolDaly(unittest.TestCase):
    """ exercise different functions in DALY protocol """

    def test_check_crc(self):
        """ test a for correct CRC validation """
        result = protocol.check_crc(response=b"\x00\x1a:70010007800C6\n", command_definition=cd)
        self.assertTrue(result)

    def test_construct_short_response(self):
        """ test for correct failure if response is too short for construct parsing """
        self.assertRaises(InvalidResponse, protocol.split_response, response=b'', command_definition=cd)

""" powermon / protocols / pi18.py """
import logging

from powermon.commands.command_definition import CommandDefinition
from powermon.commands.reading_definition import ReadingType, ResponseType
from powermon.commands.result import ResultType
from powermon.ports.porttype import PortType
from powermon.protocols.pi30 import BATTERY_TYPE_LIST, OUTPUT_MODE_LIST, PI30

log = logging.getLogger("pi18")

SETTER_COMMANDS = {}


QUERY_COMMANDS = {
    "PIRI": {
        "name": "PIRI",
        "prefix": "^P007",
        "description": "Current Settings inquiry",
        "help": " -- queries the current settings from the Inverter",
        "result_type": ResultType.COMMA_DELIMITED,
        "reading_definitions": [
            {"description": "AC Input Voltage", "reading_type": ReadingType.VOLTS, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/10"},
            {"description": "AC Input Current", "reading_type": ReadingType.CURRENT, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/10"},
            {"description": "AC Output Voltage", "reading_type": ReadingType.VOLTS, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/10"},
            {"description": "AC Output Frequency", "reading_type": ReadingType.FREQUENCY, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/10"},
            {"description": "AC Output Current", "reading_type": ReadingType.CURRENT, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/10"},
            {"description": "AC Output Apparent Power", "reading_type": ReadingType.APPARENT_POWER},
            {"description": "AC Output Active Power", "reading_type": ReadingType.WATTS},
            {"description": "Battery Voltage", "reading_type": ReadingType.VOLTS, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/10"},
            {"description": "Battery re-charge Voltage", "reading_type": ReadingType.VOLTS, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/10"},
            {"description": "Battery re-discharge Voltage", "reading_type": ReadingType.VOLTS, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/10"},
            {"description": "Battery Under Voltage", "reading_type": ReadingType.VOLTS, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/10"},
            {"description": "Battery Bulk Charge Voltage", "reading_type": ReadingType.VOLTS, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/10"},
            {"description": "Battery Float Charge Voltage", "reading_type": ReadingType.VOLTS, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/10"},
            {"description": "Battery Type",
                "reading_type": ReadingType.MESSAGE,
                "response_type": ResponseType.LIST,
                "options": BATTERY_TYPE_LIST},
            {"description": "Max AC Charging Current", "reading_type": ReadingType.CURRENT},
            {"description": "Max Charging Current", "reading_type": ReadingType.CURRENT},
            {"description": "Input Voltage Range",
                "response_type": ResponseType.LIST,
                "options": ["Appliance", "UPS"]},
            {"description": "Output Source Priority",
                "response_type": ResponseType.LIST,
                "options": ["Solar - Utility - Battery", "Solar - Battery - Utility"]},
            {"description": "Charger Source Priority",
                "response_type": ResponseType.LIST,
                "options": ["Solar First", "Solar + Utility", "Only solar charging permitted"]},
            {"description": "Max Parallel Units"},
            {"description": "Machine Type",
                "response_type": ResponseType.LIST,
                "options": ["Off Grid", "Grid Tie"]},
            {"description": "Topology",
                "response_type": ResponseType.LIST,
                "options": ["transformerless", "transformer"]},
            {"description": "Output Mode",
                "reading_type": ReadingType.MESSAGE, "response_type": ResponseType.LIST,
                "options": OUTPUT_MODE_LIST},
            {"description": "Solar power priority",
                "response_type": ResponseType.LIST,
                "options": ["Battery-Load-Utiliy + AC Charger", "Load-Battery-Utiliy"]},
            {"description": "MPPT strings"},
            {"description": "Unknown flags?", "response_type": ResponseType.STRING},
        ],
        "test_responses": [
            b"^D0882300,217,2300,500,217,5000,5000,480,480,530,440,570,570,2,10,070,1,1,1,9,0,0,0,0,1,00\xe1k\r",
            # ac_input_voltage=Invalid response for AC Input Voltage
            b'^D0882300,217,2300,500,217,5000,5000,480,480,530,440,570,570,2,10,070,1,1,1,9,0,0,0,0,1,00'
        ],
    },
}

COMMANDS_TO_REMOVE = ["QPIRI"]


class PI18(PI30):
    """ pi18 protocol handler """
    def __str__(self):
        return "PI18 protocol handler"

    def __init__(self) -> None:
        super().__init__()
        self.protocol_id = b"PI18"
        self.add_command_definitions(QUERY_COMMANDS)
        self.add_command_definitions(SETTER_COMMANDS, result_type=ResultType.ACK)
        self.remove_command_definitions(COMMANDS_TO_REMOVE)
        self.check_definitions_count(expected=44)
        self.add_supported_ports([PortType.SERIAL, PortType.USB])

    def check_crc(self, response: str, command_definition: CommandDefinition = None):
        """ crc check, override for now """
        log.debug("check crc for %s in pi30", response)
        return True

    def trim_response(self, response: str, command_definition: CommandDefinition = None) -> str:
        """ Remove extra characters from response """
        log.debug("trim %s, definition: %s", response, command_definition)
        if response.startswith(b"^D"):
            # trim ^Dxxx where xxx is data length
            response = response[5:]
        if response.endswith(b'\r'):
            # has checksum, so trim last 3 chars
            response = response[:-3]
        if response.startswith(b'('):
            # pi30 style response
            response = response[1:]
        return response

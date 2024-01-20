import unittest
from unittest import mock
import datetime
import time
from powermon.commands.command import Command
from powermon.commands.command_definition import CommandDefinition
from powermon.protocols.abstractprotocol import AbstractProtocol
from powermon.commands.result import ResultType
from powermon.commands.reading_definition import ReadingType, ResponseType
from powermon.commands.parameter import ParameterType, ParameterFormat

class test_command(unittest.TestCase):
    def test_command_definition_none(self):
        command = Command(code="test", commandtype="test", outputs=[], trigger=None)
        with self.assertRaises(ValueError):
            command.command_definition = None
        
    def test_command_definition_invalid(self):
        command = Command(code="test", commandtype="test", outputs=[], trigger=None)
        command_definition = mock.Mock()
        command_definition.is_command_code_valid.return_value = False
        with self.assertRaises(ValueError):
            command.command_definition = command_definition
        
    def test_command_definition_valid(self):
        command = Command(code="test", commandtype="test", outputs=[], trigger=None)
        command_definition = mock.Mock()
        command_definition.is_command_code_valid.return_value = True
        command.command_definition = command_definition
        self.assertEqual(command.command_definition, command_definition)
        
    # This test is covering a few too many objects to be a unit test
    def test_build_result(self):
        protocol = AbstractProtocol()
        #This is just here for comparison
        qed_command_definition_new = {
            "QED": {
                "name": "QED",
                "description": "Daily PV Generated Energy Inquiry",
                "help": " -- display daily generated energy, format is QEDyyyymmdd",
                "result_type": ResultType.SINGLE,
                "reading_definitions": [
                    {"index":0, "description":"PV Generated Energy for Day", "reading_type":ReadingType.WATT_HOURS, "response_type":ResponseType.INT, "icon": "mdi:solar-power", "device-class": "energy", "state_class": "total"},
                ],
                "parameters": [
                    {"name":"date", "description":"Date for query", "parameter_type":ParameterType.DATE, "parameter_format":ParameterFormat.YYYYMMDD}
                ],
                "test_responses": [
                    b"(00238800!J\r",
                ],
                "regex": "QED(\\d\\d\\d\\d\\d\\d\\d\\d)$",
            }
        }
        protocol.add_command_definitions(qed_command_definition_new)
        qed_command_definition = protocol.get_command_definition("QED20210901")
        command = Command(code="QED20210901", commandtype="GETTER", outputs=[], trigger=None)
        command.command_definition = qed_command_definition
        result = command.build_result(b"(00238800!J\r", protocol=protocol)
        reading = result.readings[0]
        self.assertEqual(reading.data_unit, "Wh")
        self.assertEqual(reading.data_value, 238800)
        self.assertEqual(reading.data_name, "PV Generated Energy for Day")
        
        
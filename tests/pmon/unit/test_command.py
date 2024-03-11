""" tests / pmon / unit / test_command.py """
import unittest
from datetime import (date, datetime,  # pylint: disable=W0611 # noqa: 401
                      timedelta)
from time import sleep
from unittest import mock

from powermon.commands.command import Command
from powermon.commands.reading_definition import ReadingType
from powermon.commands.result import ResultType
from powermon.protocols.abstractprotocol import AbstractProtocol


class TestCommand(unittest.TestCase):
    """ test the Command class """
    def test_command_definition_none(self):
        """ command should raise exception if definition is set to None """
        command = Command(code="test", commandtype="test", outputs=[], trigger=None)
        with self.assertRaises(ValueError):
            command.command_definition = None

    def test_command_definition_invalid(self):
        """ command should raise exception if definition is set an invalid value """
        command = Command(code="test", commandtype="test", outputs=[], trigger=None)
        command_definition = mock.Mock()
        command_definition.is_command_code_valid.return_value = False
        with self.assertRaises(ValueError):
            command.command_definition = command_definition

    def test_command_definition_valid(self):
        """ test successfull setting of definition """
        command = Command(code="test", commandtype="test", outputs=[], trigger=None)
        command_definition = mock.Mock()
        command_definition.is_command_code_valid.return_value = True
        command.command_definition = command_definition
        self.assertEqual(command.command_definition, command_definition)

    # This test is covering a few too many objects to be a unit test
    def test_build_result(self):
        """ test building a result """
        protocol = AbstractProtocol()
        # This is just here for comparison
        qed_command_definition_new = {
            "QED": {
                "name": "QED",
                "description": "Daily PV Generated Energy Inquiry",
                "help": " -- display daily generated energy, format is QEDyyyymmdd",
                "result_type": ResultType.SINGLE,
                "reading_definitions": [
                    {"description": "PV Generated Energy for Day", "reading_type": ReadingType.WATT_HOURS},
                ],
                "test_responses": [
                    b"(00238800!J\r",
                ],
                "regex": "QED(\\d\\d\\d\\d\\d\\d\\d\\d)$",
            }
        }
        protocol.add_command_definitions(qed_command_definition_new)
        qed_command_definition = protocol.get_command_definition("QED20210901")
        command = Command(code="QED20210901", commandtype=None, outputs=[], trigger=None)
        command.command_definition = qed_command_definition
        result = command.build_result(b"(00238800!J\r", protocol=protocol)
        reading = result.readings[0]
        self.assertEqual(reading.data_unit, "Wh")
        self.assertEqual(reading.data_value, 238800)
        self.assertEqual(reading.data_name, "PV Generated Energy for Day")

    def test_template_command(self):
        """ test that a correct template 'works' """
        command_config = {'command': """f'QED{datetime.today().strftime("%Y%m%d")}'""", 'type': 'templated'}
        command = Command.from_config(command_config)
        expected_code = f'QED{datetime.today().strftime("%Y%m%d")}'
        # print(expected_code)
        self.assertEqual(command.code, expected_code)

    def test_template_command_touch(self):
        """ test that the command code is updated for a template after a touch' """
        command_config = {'command': """f'QED{datetime.today().strftime("%Y%m%S")}'""", 'type': 'templated'}
        expected_code = f'QED{datetime.today().strftime("%Y%m%S")}'
        # print(expected_code)
        command = Command.from_config(command_config)
        self.assertEqual(command.code, expected_code)
        sleep(2)
        command.touch()
        expected_code = f'QED{datetime.today().strftime("%Y%m%S")}'
        # print(expected_code)
        self.assertEqual(command.code, expected_code)

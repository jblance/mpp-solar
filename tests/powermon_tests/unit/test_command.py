import unittest
from unittest import mock
import datetime
import time
from powermon.commands.command import Command

class test_command(unittest.TestCase):
    def test_command_definition_none(self):
        command = Command(code="test", commandtype="test", outputs=[], trigger=None)
        self.assertRaises(ValueError, command.set_command_definition, None)
        
    def test_command_definition_invalid(self):
        command = Command(code="test", commandtype="test", outputs=[], trigger=None)
        command_definition = mock.Mock()
        command_definition.is_command_code_valid.return_value = False
        self.assertRaises(ValueError, command.set_command_definition, command_definition)
        
    def test_command_definition_valid(self):
        command = Command(code="test", commandtype="test", outputs=[], trigger=None)
        command_definition = mock.Mock()
        command_definition.is_command_code_valid.return_value = True
        command.set_command_definition(command_definition)
        self.assertEqual(command.command_definition, command_definition)
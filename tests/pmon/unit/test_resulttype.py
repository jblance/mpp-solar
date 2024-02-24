""" tests / pmon / unit / test_resulttype.py """
# import struct
import unittest

import construct as cs

from powermon.commands.result import ResultType
from powermon.protocols.abstractprotocol import AbstractProtocol
from powermon.commands.reading_definition import ReadingDefinition, ResponseType
from powermon.commands.command_definition import CommandDefinition
from powermon.errors import CommandDefinitionIncorrect


class TestResultTypes(unittest.TestCase):
    """ test different result types """
    def test_result_type_construct(self):
        """ test construct result type """
        construct = cs.Struct("voltage" / cs.Int16ub)
        reading_definition_config = {"response_type": ResponseType.STRING}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.CONSTRUCT, reading_definitions=[reading_definition])
        command_definition.construct = construct
        command_definition.construct_min_response = 1
        result = AbstractProtocol.split_response(self, response=b"\x0f\x90", command_definition=command_definition)
        expected = [('voltage', 3984)]
        self.assertEqual(result, expected)

    def test_result_type_construct_with_no_construct(self):
        """ test construct result type when no construct supplied """
        reading_definition_config = {"response_type": ResponseType.STRING}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.CONSTRUCT, reading_definitions=[reading_definition])
        command_definition.construct = None
        self.assertRaises(CommandDefinitionIncorrect, AbstractProtocol.split_response, AbstractProtocol, response="response", command_definition=command_definition)

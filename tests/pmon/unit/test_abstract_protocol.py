import unittest

from powermon.protocols.abstractprotocol import AbstractProtocol
from powermon.commands.result import ResultType


class test_protocol_pi30(unittest.TestCase):
    def test_add_command_definitions(self):
        protocol = AbstractProtocol()
        # Just here for comparison
        pbt_command_definition_new = {
            "PBT": {
                "name": "PBT",
                "description": "Set Battery Type",
                "help": " -- examples: PBT00 (set battery as AGM), PBT01 (set battery as FLOODED), PBT02 (set battery as USER)",
                "regex": "PBT(0[012])$",
            }
        }
        protocol.add_command_definitions(pbt_command_definition_new, result_type=ResultType.ACK)

        # Returns None since it doesn't match the regex
        # Raises an exception now
        # pbt_definition = protocol.get_command_with_command_string("PBT")
        # self.assertIsNone(pbt_definition)


        # Returns since it does match the regex
        pbt_definition = protocol.get_command_definition("PBT00")
        self.assertIsNotNone(pbt_definition)

        self.assertEqual(pbt_definition.code, "PBT")
        self.assertEqual(pbt_definition.result_type, ResultType.ACK)

    # def test_icon_and_deviceclass_from_response(self):
    #     protocol = pi30()
    #     command_definition = protocol.get_command_definition("Q1")

    #     self.assertEqual(command_definition.response_definitions[13].get_description(), "SCC charge power")
    #     self.assertEqual(command_definition.response_definitions[13].icon, "mdi:solar-power")
    #     self.assertEqual(command_definition.response_definitions[13].device_class, "power") 

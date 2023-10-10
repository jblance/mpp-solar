import unittest
from powermon.protocols.pi30 import pi30
from powermon.commands.result import ResultType

class test_protocol_pi30(unittest.TestCase):
    def test_add_command_definitions(self):
        protocol = pi30()
        test_definition = protocol.get_command_definition("TEST")
        self.assertEqual(test_definition, None)
        test_command_definition = {
            "TEST": {
                "name": "TEST",
                "description": "Secondary CPU firmware version inquiry",
                "help": " -- queries the secondary CPU firmware version",
                "response_type": ResultType.INDEXED,
                "response": [[0, "Secondary CPU firmware version", "bytes.decode", ""]],
                "test_responses": [b"(VERFW:00072.70\x53\xA7\r"],
            }
        }
        protocol.add_command_definitions(test_command_definition, "QUERY")
        test_definition = protocol.get_command_definition("TEST")
        self.assertEqual(test_definition.code, "TEST")
        self.assertEqual(test_definition.response_type, ResultType.INDEXED)
        self.assertEqual(test_definition.get_type(), "QUERY")
        
    def test_icon_and_deviceclass_from_response(self):
        protocol = pi30()
        command_definition = protocol.get_command_definition("Q1")
        
        self.assertEqual(command_definition.response_definitions[13].get_description(), "SCC charge power")
        self.assertEqual(command_definition.response_definitions[13].icon, "mdi:solar-power")
        self.assertEqual(command_definition.response_definitions[13].device_class, "power") 
        
        
import unittest
import datetime
from powermon.protocols.abstractprotocol import AbstractProtocol
from powermon.commands.result import ResultType
from powermon.commands.reading_definition import ResponseType
from powermon.commands.reading_definition import ReadingType
from powermon.commands.parameter import ParameterType
from powermon.commands.parameter import ParameterFormat

class test_protocol_pi30(unittest.TestCase):
    def test_add_command_definitions(self):
        protocol = AbstractProtocol()
        #Just here for comparison
        pbt_old_command_definitions = {
            "PBT": {
                "name": "PBT",
                "description": "Set Battery Type",
                "help": " -- examples: PBT00 (set battery as AGM), PBT01 (set battery as FLOODED), PBT02 (set battery as USER)",
                "response_type": ResultType.ACK,
                "response": [[0, "Command execution", ResponseType.ACK, {"NAK": "Failed", "ACK": "Successful"}]],
                "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
                "regex": "PBT(0[012])$",
            },
        }
        pbt_command_definition_new = {
            "PBT": {
                "name": "PBT",
                "description": "Set Battery Type",
                "help": " -- examples: PBT00 (set battery as AGM), PBT01 (set battery as FLOODED), PBT02 (set battery as USER)",
                "result_type": ResultType.ACK,
                "reading_definitions": [{"index":0, "decription":"Command execution", "reading_type":ReadingType.ACK, "response_type":ResponseType.ACK}],
                "test_responses": [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",],
                "regex": "PBT(0[012])$",
            }
        }
        protocol.add_command_definitions(pbt_command_definition_new, "QUERY")
        
        #Returns None since it doesn't match the regex
        pbt_definition = protocol.get_command_with_command_string("PBT")
        self.assertIsNone(pbt_definition)
        
        #Returns since it does match the regex
        pbt_definition = protocol.get_command_with_command_string("PBT00")
        self.assertIsNotNone(pbt_definition)
        
        self.assertEqual(pbt_definition.code, "PBT")
        self.assertEqual(pbt_definition.result_type, ResultType.ACK)
        self.assertEqual(pbt_definition.get_type(), "QUERY")
        
    def test_command_defintition_parameters(self):
        protocol = AbstractProtocol()
        #This is just here for comparison
        qed_command_definition_old = {
            "QED": {
                "name": "QED",
                "description": "Daily PV Generated Energy Inquiry",
                "help": " -- display daily generated energy, format is QEDyyyymmdd",
                "response_type": ResultType.INDEXED,
                "response": [
                    [0, "PV Generated Energy for Day", ResponseType.INT, "Wh", {"icon": "mdi:solar-power", "device-class": "energy", "state_class": "total"},],
                    [1, "Year", ResponseType.INFO+":cn[3:7]", ""],
                    [2, "Month", ResponseType.INFO+":calendar.month_name[int(cn[7:9])]", ""],
                    [3, "Day", ResponseType.INFO+":cn[9:]", ""],
                ],
                "test_responses": [
                    b"(00238800!J\r",
                ],
                "regex": "QED(\\d\\d\\d\\d\\d\\d\\d\\d)$",
            }
        }
        qed_command_definition_new = {
            "QED": {
                "name": "QED",
                "description": "Daily PV Generated Energy Inquiry",
                "help": " -- display daily generated energy, format is QEDyyyymmdd",
                "result_type": ResultType.INDEXED,
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
        
        protocol.add_command_definitions(qed_command_definition_new, "QUERY")
        qed_command = protocol.get_command_with_command_string("QED20230115")
        self.assertIsNotNone(qed_command)
        
        query_date = datetime.date(2023, 1, 15)
        
        self.assertEqual(query_date,qed_command.parameters["date"].value)
        
        
        
    # def test_icon_and_deviceclass_from_response(self):
    #     protocol = pi30()
    #     command_definition = protocol.get_command_definition("Q1")
        
    #     self.assertEqual(command_definition.response_definitions[13].get_description(), "SCC charge power")
    #     self.assertEqual(command_definition.response_definitions[13].icon, "mdi:solar-power")
    #     self.assertEqual(command_definition.response_definitions[13].device_class, "power") 
        
        
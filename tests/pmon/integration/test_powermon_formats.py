import subprocess
import unittest
# import json
import yaml
from powermon.device import Device
from powermon.outputformats.hass import Hass
from powermon.outputformats.table import Table
from powermon.commands.result import Result
from powermon.commands.reading import Reading


class test_powermon_formats(unittest.TestCase):
    maxDiff = 9999

#     def test_format_hass(self):

#         config = yaml.safe_load("""device:
#   name: Test_Inverter
#   id: 123456789
#   model: 8048MAX
#   manufacturer: MPP-Solar
#   port:
#     type: test
#     protocol: PI30
#     """)
#         topic0 = "homeassistant/sensor/mpp_protocol_id/config"
#         payload0 = '{"name": "mpp protocol_id", "state_topic": "homeassistant/sensor/mpp_protocol_id/state", "unique_id": "mpp_protocol_id", "force_update": "true", "last_reset": "2023-05-30 03:41:31.850677", "device": {"name": "Test_Inverter", "identifiers": [123456789], "model": "8048MAX", "manufacturer": "MPP-Solar"}}'
#         topic1 = "homeassistant/sensor/mpp_protocol_id/state"
#         payload1 = "PI30"
#         device = Device.from_config(config=config.get("device"))
#         # print(device)
#         hass_formatter = Hass()
#         _result = Result(command_code=None)
#         response = Reading(data_name="protocol_id", data_value="PI30", data_unit="")
#         _result.add_readings([response])
#         result = hass_formatter.format(_result)

#         # print('\n')
#         # print(result[0]['payload'][-90:])
#         # print(payload0[-112:])

#         self.assertEqual(len(result), 2)
#         self.assertEqual(result[0]['topic'], topic0)
#         # need to exclude checking last_reset value as it is time based
#         self.assertEqual(result[0]['payload'][:160], payload0[:160])
#         self.assertEqual(result[0]['payload'][-112:], payload0[-112:])

#         self.assertEqual(result[1]['topic'], topic1)
#         self.assertEqual(result[1]['payload'], payload1)
        


#     def test_format_htmltable(self):
#         try:
#             expected = """<table><tr><th>Parameter</th><th>Value</th><th>Unit</th></tr>
# <tr><td>protocol_id</td><td>PI30</td><td></td></tr>
# </table>\n"""
#             result = subprocess.run(
#                 ["powermon", "--once", "--config", '{"device": {"port":{"type":"test"}}, "commands": [{"command":"QPI", "outputs": [{"type": "screen", "format": "htmltable"}]}]} '],
#                 check=True,
#                 capture_output=True,
#                 text=True,
#             )
#             # print(result.stdout)
#             self.assertEqual(result.stdout, expected)
#             self.assertEqual(result.returncode, 0)
#         except subprocess.CalledProcessError as error:
#             print(error.stdout)
#             print(error.stderr)
#             raise error


#     def test_format_raw(self):
#         try:
#             expected = "b'(PI30\\x9a\\x0b\\r'\n"
#             result = subprocess.run(
#                 ["powermon", "--once", "--config", '{"device": {"port":{"type":"test"}}, "commands": [{"command":"QPI", "outputs": [{"type": "screen", "format": "raw"}]}]} '],
#                 check=True,
#                 capture_output=True,
#                 text=True,
#             )
#             # print(result.stdout)
#             self.assertEqual(result.stdout, expected)
#             self.assertEqual(result.returncode, 0)
#         except subprocess.CalledProcessError as error:
#             print(error.stdout)
#             print(error.stderr)
#             raise error

#     def test_format_simple(self):
#         try:
#             expected = "protocol_id=PI30\n"
#             result = subprocess.run(
#                 ["powermon", "--once", "--config", '{"device": {"port":{"type":"test"}}, "commands": [{"command":"QPI", "outputs": [{"type": "screen", "format": "simple"}]}]} '],
#                 check=True,
#                 capture_output=True,
#                 text=True,
#             )
#             # print(result.stdout)
#             self.assertEqual(result.stdout, expected)
#             self.assertEqual(result.returncode, 0)
#         except subprocess.CalledProcessError as error:
#             print(error.stdout)
#             print(error.stderr)
#             raise error

#     def test_format_table(self):
#         try:
#             expected = """-----------------------------------------
# Command: QPI - Protocol ID inquiry     \n-----------------------------------------
# Parameter    Value   Unit           \nprotocol_id  PI30                   \n"""
#             result = subprocess.run(
#                 ["powermon", "--once", "--config", '{"device": {"port":{"type":"test"}}, "commands": [{"command":"QPI", "outputs": [{"type": "screen", "format": "table"}]}]} '],
#                 check=True,
#                 capture_output=True,
#                 text=True,
#             )
#             # print("expected:: ", expected)
#             # print("result:: ", result.stdout)
#             #self.assertEqual(result.stdout, expected)
#             self.assertEqual(result.returncode, 0)
#         except subprocess.CalledProcessError as error:
#             print(error.stdout)
#             print(error.stderr)
#             raise error

    def test_format_topics(self):
        print("test_format_topics todo")  # TODO: implement
        return

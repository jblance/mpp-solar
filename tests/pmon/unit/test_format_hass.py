""" tests / pmon / unit / test_format_hass.py """
import json
import unittest

from powermon.commands.command import Command
from powermon.commands.command_definition import CommandDefinition
# from powermon.commands.reading import Reading
from powermon.commands.reading_definition import (ReadingDefinition,
                                                  ReadingType, ResponseType)
from powermon.commands.result import Result, ResultType
from powermon.device import DeviceInfo
from powermon.outputformats.hass import Hass


class TestFormatHass(unittest.TestCase):
    """ test the HASS formatter """
    def test_format_hass(self):
        """ test generation of hass config and state messages """
        hass_formatter = Hass({})
        device_info = DeviceInfo(name="device_name", device_id="device_id", model="device_model", manufacturer="device_manufacturer")
        reading_definition = ReadingDefinition.from_config({"description": "Energy Today", "reading_type": ReadingType.WATT_HOURS, "response_type": ResponseType.INT, "icon": "mdi:solar-power", "device-class": "energy", "state_class": "total"}, 0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "CODE"})
        command.command_definition = command_definition
        result = Result(command=command, raw_response=b"(238800\xcd\xcd\r", responses=b"238800")
        fd = hass_formatter.format(command, result, device_info=device_info)
        # print(fd)
        # Should be a list of len 2
        self.assertIsInstance(fd, list)
        self.assertEqual(len(fd), 2)
        # first item should be a config message (a dict with only topic and payload keys)
        self.assertIsInstance(fd[0], dict)
        self.assertListEqual(list(fd[0]), ['topic', 'payload'])
        self.assertEqual(fd[0]['topic'], "homeassistant/sensor/energy_today/config")
        config_payload = json.loads(fd[0]["payload"])
        self.assertListEqual(list(config_payload), ['name', 'state_topic', 'unique_id', 'force_update', 'last_reset', 'device', 'unit_of_measurement', 'icon', 'state_class'])
        self.assertEqual(config_payload['name'], "energy_today")
        self.assertEqual(config_payload['state_topic'], "homeassistant/sensor/energy_today/state")
        self.assertEqual(config_payload['unique_id'], "energy_today_device_id")
        self.assertEqual(config_payload['unit_of_measurement'], "Wh")
        self.assertEqual(config_payload['icon'], "mdi:solar-power")
        self.assertEqual(config_payload['state_class'], "total")
        self.assertDictEqual(config_payload['device'], {'name': 'device_name', 'identifiers': ['device_id'], 'model': 'device_model', 'manufacturer': 'device_manufacturer'})

        # second list item is state message (a dict with only topic and payload keys)
        self.assertIsInstance(fd[1], dict)
        self.assertListEqual(list(fd[1]), ['topic', 'payload'])
        self.assertEqual(fd[1]['topic'], "homeassistant/sensor/energy_today/state")
        self.assertEqual(fd[1]["payload"], 238800)

        # print(config_payload)

""" tests / pmon / unit / test_reading_definition.py """
import unittest

from powermon.commands.reading_definition import (ReadingDefinition, ReadingType, ResponseType)


class TestReadingDefinitions(unittest.TestCase):
    """ exercise different reading definition functionality """

    def test_temperature_reading(self):
        """ test a correct temperature is returned in celcius """
        reading_definition_config = {"reading_type": ReadingType.TEMPERATURE, "response_type": ResponseType.INT}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        result = reading_definition.reading_from_raw_response(b"27")
        self.assertEqual(27, result[0].data_value)
        self.assertEqual("°C", result[0].data_unit)

    def test_temperature_reading_override(self):
        """ test a correct temperature is returned in farenheit when overriden """
        reading_definition_config = {"reading_type": ReadingType.TEMPERATURE, "response_type": ResponseType.INT}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        result = reading_definition.reading_from_raw_response(b"27", override={"temperature": "F"})
        self.assertEqual(80.6, result[0].data_value)
        self.assertEqual("°F", result[0].data_unit)

    def test_kilowatt_hours(self):
        """ test ReadingType.KILOWATT_HOURS """
        reading_definition_config = {"reading_type": ReadingType.KILOWATT_HOURS, "response_type": ResponseType.INT}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        result = reading_definition.reading_from_raw_response(b"123")
        self.assertEqual(123, result[0].data_value)
        self.assertEqual("kWh", result[0].data_unit)

    def test_hex_str_1a(self):
        """ test ReadingType.HEX_STR """
        reading_definition_config = {"description": "Checksum", "reading_type": ReadingType.HEX_STR, "response_type": ResponseType.HEX_CHAR}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        result = reading_definition.reading_from_raw_response(b"\x1a")
        self.assertEqual("0x1a", result[0].data_value)

    def test_hex_str_9c(self):
        """ test ReadingType.HEX_STR """
        reading_definition_config = {"description": "Checksum", "reading_type": ReadingType.HEX_STR, "response_type": ResponseType.HEX_CHAR}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        result = reading_definition.reading_from_raw_response(b"\x9c")
        self.assertEqual("0x9c", result[0].data_value)

    def test_ignore(self):
        """ test ReadingType.IGNORE """
        reading_definition_config = {"reading_type": ReadingType.IGNORE}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        result = reading_definition.reading_from_raw_response(b"ignoreme")
        self.assertEqual([], result)

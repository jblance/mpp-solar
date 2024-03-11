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

    def test_enflags(self):
        """  test ReadingType.MULTI_ENABLE_DISABLE """
        reading_definition_config = {"description": "Device Status", "reading_type": ReadingType.MULTI_ENABLE_DISABLE,
                                     "response_type": ResponseType.ENABLE_DISABLE_FLAGS,
                                     "options": {
                                         "a": "Buzzer",
                                         "b": "Overload Bypass",
                                         "j": "Power Saving",
                                         "k": "LCD Reset to Default",
                                         "u": "Overload Restart",
                                         "v": "Over Temperature Restart",
                                         "x": "LCD Backlight",
                                         "y": "Primary Source Interrupt Alarm",
                                         "z": "Record Fault Code",
                                     }}
        reading_definition = ReadingDefinition.from_config(reading_definition_config)
        result = reading_definition.reading_from_raw_response(b"EakxyDbjuvz")
        self.assertEqual(len(result), 9)
        self.assertEqual(result[0].data_name, "Buzzer")
        self.assertEqual(result[0].data_value, "enabled")
        self.assertEqual(result[1].data_name, "LCD Reset to Default")
        self.assertEqual(result[1].data_value, "enabled")
        self.assertEqual(result[2].data_name, "LCD Backlight")
        self.assertEqual(result[2].data_value, "enabled")
        self.assertEqual(result[3].data_name, "Primary Source Interrupt Alarm")
        self.assertEqual(result[3].data_value, "enabled")
        self.assertEqual(result[4].data_name, "Overload Bypass")
        self.assertEqual(result[4].data_value, "disabled")
        self.assertEqual(result[5].data_name, "Power Saving")
        self.assertEqual(result[5].data_value, "disabled")
        self.assertEqual(result[6].data_name, "Overload Restart")
        self.assertEqual(result[6].data_value, "disabled")
        self.assertEqual(result[7].data_name, "Over Temperature Restart")
        self.assertEqual(result[7].data_value, "disabled")
        self.assertEqual(result[8].data_name, "Record Fault Code")
        self.assertEqual(result[8].data_value, "disabled")

    def test_flags(self):
        """  test ReadingType.FLAGS """
        reading_definition_config = {"description": "Device Status",
                                     "reading_type": ReadingType.FLAGS,
                                     "response_type": ResponseType.FLAGS,
                                     "flags": [
                                         "Is SBU Priority Version Added",
                                         "Is Configuration Changed",
                                         "Is SCC Firmware Updated",
                                         "Is Load On",
                                         "Is Battery Voltage to Steady While Charging",
                                         "Is Charging On",
                                         "Is SCC Charging On",
                                         "Is AC Charging On",
                                     ]}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        result = reading_definition.reading_from_raw_response(b"00110110")
        self.assertEqual(len(result), 8)
        self.assertEqual(result[0].data_name, "Is SBU Priority Version Added")
        self.assertEqual(result[0].data_value, 0)
        self.assertEqual(result[1].data_name, "Is Configuration Changed")
        self.assertEqual(result[1].data_value, 0)
        self.assertEqual(result[2].data_name, "Is SCC Firmware Updated")
        self.assertEqual(result[2].data_value, 1)
        self.assertEqual(result[3].data_name, "Is Load On")
        self.assertEqual(result[3].data_value, 1)
        self.assertEqual(result[7].data_name, "Is AC Charging On")
        self.assertEqual(result[7].data_value, 0)

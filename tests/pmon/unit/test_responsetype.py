""" tests / pmon / unit / test_responsetype.py """
import struct
import unittest

from powermon.commands.reading_definition import ReadingDefinition, ReadingType, ResponseType


class TestResponseTypes(unittest.TestCase):
    """ exercise different response types """

    def test_option_invalid_key(self):
        """ test that when supplying an invalid key to a ResponseType.OPTION raises a KeyError exception """
        reading_definition_config = {"response_type": ResponseType.OPTION, "options": {"00": "New", "01": "Slave", "02": "Master"}}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        self.assertRaises(KeyError, reading_definition.translate_raw_response, b"03")

    def test_option_valid_key(self):
        """ test ResponseType.OPTION returns value associated with key """
        reading_definition_config = {"response_type": ResponseType.OPTION, "options": {"00": "New", "01": "Slave", "02": "Master"}}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        result = reading_definition.translate_raw_response(b"02")
        expected = "Master"
        self.assertEqual(result, expected)

    def test_list_invalid_index(self):
        """ test that when supplying an invalid index to a ResponseType.LIST raises a IndexError exception """
        reading_definition_config = {"response_type": ResponseType.LIST, "options": ["Utility first", "Solar first", "SBU first"]}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        self.assertRaises(IndexError, reading_definition.translate_raw_response, b"03")

    def test_list_valid_index(self):
        """ test ResponseType.LIST returns value associated with index """
        reading_definition_config = {"response_type": ResponseType.LIST, "options": ["Utility first", "Solar first", "SBU first"]}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        result = reading_definition.translate_raw_response(b"02")
        expected = "SBU first"
        self.assertEqual(result, expected)

    def test_le_2b_s(self):
        """ test ResponseType.LE_2B_s """
        reading_definition_config = {"response_type": ResponseType.LE_2B_S}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        result = reading_definition.translate_raw_response(b"7800")
        expected = 120
        self.assertEqual(result, expected)

    def test_le_2b_s_not_2b_short(self):
        """ test ResponseType.LE_2B_S when response is not 2B (only 1B) """
        reading_definition_config = {"response_type": ResponseType.LE_2B_S}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        self.assertRaises(struct.error, reading_definition.translate_raw_response, b"78")

    def test_template_bytes(self):
        """ test ResponseType.TEMPLATE_BYTES """
        reading_definition_config = {"reading_type": ReadingType.MESSAGE, "response_type": ResponseType.TEMPLATE_BYTES, "format_template" : "r[2:int(r[0:2])+2]"}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        result = reading_definition.translate_raw_response(b"1492932105105335005535")
        expected = "92932105105335"
        self.assertEqual(result, expected)

    def test_template_int(self):
        """ test ResponseType.TEMPLATE_INT """
        reading_definition_config = {"response_type": ResponseType.TEMPLATE_INT, "format_template": "r/1000"}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        result = reading_definition.translate_raw_response(b"12345")
        expected = 12.345
        self.assertEqual(result, expected)

    def test_bit_encoded(self):
        """ test ResponseType.BIT_ENCODED """
        reading_definition_config = {"response_type": ResponseType.BIT_ENCODED,
                                     "options": {0: "No alarm",
                                                 1: "Low Voltage",
                                                 2: "High Voltage",
                                                 4: "Low SOC",
                                                 8: "Low Starter Voltage",
                                                 16: "High Starter Voltage",
                                                 32: "Low Temperature",
                                                 64: "High Temperature",
                                                 128: "Mid Voltage",
                                                 256: "Overload",
                                                 512: "DC-ripple",
                                                 1024: "Low V AC out",
                                                 2048: "High V AC out",
                                                 4096: "Short Circuit",
                                                 8192: "BMS Lockout"}}

        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        result = reading_definition.translate_raw_response(b"250")
        expected = 'High Voltage,Low Starter Voltage,High Starter Voltage,Low Temperature,High Temperature,Mid Voltage'
        self.assertEqual(result, expected)

    def test_bool_false(self):
        """ test ResponseType.BOOL for false type responses"""
        reading_definition_config = {"response_type": ResponseType.BOOL}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        self.assertFalse(reading_definition.translate_raw_response(False))
        self.assertFalse(reading_definition.translate_raw_response("False"))
        self.assertRaises(ValueError, reading_definition.translate_raw_response, "FALSE")
        self.assertRaises(ValueError, reading_definition.translate_raw_response, "false")
        self.assertFalse(reading_definition.translate_raw_response(b"False"))
        self.assertRaises(ValueError, reading_definition.translate_raw_response, b"FALSE")
        self.assertRaises(ValueError, reading_definition.translate_raw_response, b"false")
        self.assertFalse(reading_definition.translate_raw_response(0))
        self.assertFalse(reading_definition.translate_raw_response("0"))
        self.assertFalse(reading_definition.translate_raw_response(b"0"))

    def test_bool_true(self):
        """ test ResponseType.BOOL for true type responses"""
        reading_definition_config = {"response_type": ResponseType.BOOL}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        self.assertTrue(reading_definition.translate_raw_response(True))
        self.assertTrue(reading_definition.translate_raw_response("True"))
        self.assertRaises(ValueError, reading_definition.translate_raw_response, "TRUE")
        self.assertRaises(ValueError, reading_definition.translate_raw_response, "true")
        self.assertTrue(reading_definition.translate_raw_response(b"True"))
        self.assertRaises(ValueError, reading_definition.translate_raw_response, b"TRUE")
        self.assertRaises(ValueError, reading_definition.translate_raw_response, b"true")
        self.assertTrue(reading_definition.translate_raw_response(1))
        self.assertTrue(reading_definition.translate_raw_response("1"))
        self.assertTrue(reading_definition.translate_raw_response(b"1"))
        self.assertTrue(reading_definition.translate_raw_response("9999"))

    def test_string(self):
        """ test ResponseType.STRING """
        reading_definition_config = {"response_type": ResponseType.STRING}
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        result = reading_definition.translate_raw_response(b"This is a string")
        expected = 'This is a string'
        self.assertEqual(result, expected)

    def test_enflags(self):
        """  test ResponseType.ENABLE_DISABLE_FLAGS """
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
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        result = reading_definition.translate_raw_response(b"EakxyDbjuvz")
        expected = {'Buzzer': 'enabled', 'LCD Reset to Default': 'enabled', 'LCD Backlight': 'enabled', 'Primary Source Interrupt Alarm': 'enabled', 'Overload Bypass': 'disabled', 'Power Saving': 'disabled', 'Overload Restart': 'disabled', 'Over Temperature Restart': 'disabled', 'Record Fault Code': 'disabled'}
        # print(result)
        self.assertDictEqual(result, expected)

    def test_flags(self):
        """  test ResponseType.FLAGS """
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
        result = reading_definition.translate_raw_response(b"00110110")
        expected = {'Is SBU Priority Version Added': 0, 'Is Configuration Changed': 0, 'Is SCC Firmware Updated': 1, 'Is Load On': 1, 'Is Battery Voltage to Steady While Charging': 0, 'Is Charging On': 1, 'Is SCC Charging On': 1, 'Is AC Charging On': 0}
        # print(result)
        self.assertDictEqual(result, expected)

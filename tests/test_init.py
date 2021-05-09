import unittest

import mppsolar
from mppsolar.outputs.baseoutput import baseoutput
from mppsolar.devices.mppsolar import mppsolar as _mppsolar
from mppsolar.devices.jkbms import jkbms as _jkbms
from mppsolar.devices.device import AbstractDevice as _abstractdevice


class test_init(unittest.TestCase):
    def test_get_outputs(self):
        """ test the get_outputs command"""
        list_of_outputs = (
            "hass_mqtt,influx_mqtt,influx2_mqtt,json_mqtt,json,mqtt,raw,screen,tag_mqtt"
        )
        outputs = mppsolar.get_outputs(list_of_outputs)

        # Check all outputs are valid
        for output in outputs:
            self.assertIsInstance(output, type(baseoutput()))

        # Check options are created
        number_in_list = len(list_of_outputs.split(","))
        self.assertEqual(len(outputs), number_in_list)

    def test_get_device_class(self):
        """ test get_device_class"""
        device_class = mppsolar.get_device_class("mppsolar")
        self.assertEqual(device_class, _mppsolar)
        self.assertEqual(device_class, type(_mppsolar()))

        device_class = mppsolar.get_device_class("jkbms")
        self.assertEqual(device_class, _jkbms)
        self.assertEqual(device_class, type(_jkbms()))

        # print(mppsolar.main())

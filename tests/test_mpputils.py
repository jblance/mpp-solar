import unittest
from mppsolar import mpputils
from mppsolar import mppinverter


class test_mpputils(unittest.TestCase):
    def test_failed_initialisation(self):
        """ Initialisation should fail if no device provided """
        self.assertRaises(mppinverter.NoDeviceError, mpputils.mppUtils)

    def test_mpputils_init_test(self):
        """ test initialisation of TEST connection"""
        utils = mpputils.mppUtils('TEST')
        # command = inverter.execute('QPIWS')
        # print(command)
        self.assertIsInstance(utils, mpputils.mppUtils)

    def test_serial_number(self):
        """ test serial number response from mppUtils """
        utils = mpputils.mppUtils('TEST')
        serial = utils.getSerialNumber()
        print(serial)
        self.assertEqual(serial, '9293333010501')

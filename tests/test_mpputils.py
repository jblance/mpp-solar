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
        """ test serial number byte_response from mppUtils """
        utils = mpputils.mppUtils('TEST')
        response = utils.getSerialNumber()
        print(response)
        self.assertEqual(response, '9293333010501')

    def test_all_commands(self):
        """ test known commands byte_response from mppUtils """
        utils = mpputils.mppUtils('TEST')
        response = utils.getKnownCommands()
        print(response)
        self.assertIsInstance(response, list)

    def test_full_status(self):
        """ test full status byte_response from mppUtils """
        utils = mpputils.mppUtils('TEST')
        response = utils.getFullStatus()
        print(response)
        self.assertIsInstance(response, dict)

    def test_settings(self):
        """ test getSettings byte_response from mppUtils """
        utils = mpputils.mppUtils('TEST')
        response = utils.getSettings()
        print(response)
        self.assertIsInstance(response, dict)

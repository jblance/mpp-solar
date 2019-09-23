import unittest
from mppsolar import mppinverter
from mppsolar import mppcommand


class test_mppinverter(unittest.TestCase):
    def test_failed_initialisation(self):
        """ Initialisation should fail if no device provided """
        self.assertRaises(mppinverter.NoDeviceError, mppinverter.mppInverter)

    def test_init_serial(self):
        """ test initialisation defaults for a serial connected inverter """
        inverter = mppinverter.mppInverter('/dev/ttyUSB0')
        self.assertEqual(inverter._baud_rate, 2400)
        self.assertEqual(inverter._serial_device, '/dev/ttyUSB0')
        self.assertIsNone(inverter._serial_number)
        self.assertFalse(inverter._test_device)
        self.assertFalse(inverter._direct_usb)
        self.assertIsInstance(inverter.getAllCommands(), list)

    def test_init_hidraw0(self):
        """ test initialisation as usb direct device """
        inverter = mppinverter.mppInverter('/dev/hidraw0')
        self.assertEqual(inverter._baud_rate, 2400)
        self.assertEqual(inverter._serial_device, '/dev/hidraw0')
        self.assertIsNone(inverter._serial_number)
        self.assertFalse(inverter._test_device)
        self.assertTrue(inverter._direct_usb)
        self.assertIsInstance(inverter.getAllCommands(), list)

    def test_init_hidraw9(self):
        """ test initialisation as usb direct device (high numbered device) """
        inverter = mppinverter.mppInverter('/dev/hidraw9')
        self.assertEqual(inverter._baud_rate, 2400)
        self.assertEqual(inverter._serial_device, '/dev/hidraw9')
        self.assertIsNone(inverter._serial_number)
        self.assertFalse(inverter._test_device)
        self.assertTrue(inverter._direct_usb)
        self.assertIsInstance(inverter.getAllCommands(), list)

    def test_init_test(self):
        """ test initialisation as a test device """
        inverter = mppinverter.mppInverter('TEST')
        self.assertEqual(inverter._baud_rate, 2400)
        self.assertEqual(inverter._serial_device, 'TEST')
        self.assertIsNone(inverter._serial_number)
        self.assertTrue(inverter._test_device)
        self.assertFalse(inverter._direct_usb)
        self.assertIsInstance(inverter.getAllCommands(), list)

    def test_serial_number(self):
        """ getSerialNumber should return the test serial number """
        inverter = mppinverter.mppInverter('TEST')
        self.assertEqual(inverter.getSerialNumber(), '9293333010501')

    def test_print_inverter_test(self):
        """ test string representation of inverter (TEST connection)"""
        inverter = mppinverter.mppInverter('TEST')
        print(inverter)
        self.assertIsInstance(inverter.__str__(), str)

    def test_print_inverter_usb(self):
        """ test string representation of inverter (Direct USB connected)"""
        inverter = mppinverter.mppInverter('/dev/hidraw0')
        print(inverter)
        self.assertIsInstance(inverter.__str__(), str)

    def test_print_inverter_serial(self):
        """ test string representation of inverter (Serial connected)"""
        inverter = mppinverter.mppInverter('/dev/ttyUSB0')
        print(inverter)
        self.assertIsInstance(inverter.__str__(), str)

    def test_execute_query_cmd(self):
        """ test execute of QUERY command (TEST connection)"""
        inverter = mppinverter.mppInverter('TEST')
        command = inverter.execute('QPIGS')
        print(command)
        self.assertIsInstance(command, mppcommand.mppCommand)

    def test_execute_setter_cmd(self):
        """ test execute of SETTER command (TEST connection)"""
        inverter = mppinverter.mppInverter('TEST')
        command = inverter.execute('PSDV56.4')
        print(command)
        self.assertIsInstance(command, mppcommand.mppCommand)

    def test_execute_regex_cmd(self):
        """ test execute of regex command (TEST connection)"""
        inverter = mppinverter.mppInverter('TEST')
        command = inverter.execute('QPGS0')
        print(command)
        self.assertIsInstance(command, mppcommand.mppCommand)

    def test_execute_invalid_cmd(self):
        """ test execute of INVALID command (TEST connection) - should return None"""
        inverter = mppinverter.mppInverter('TEST')
        command = inverter.execute('INVALID99')
        print(command)
        self.assertIsNone(command)

    def test_execute_enflags_cmd(self):
        """ test execute of enflags command (TEST connection)"""
        inverter = mppinverter.mppInverter('TEST')
        command = inverter.execute('QFLAG')
        print(command)
        self.assertIsInstance(command, mppcommand.mppCommand)

    def test_execute_statflags_cmd(self):
        """ test execute of statflags command (TEST connection)"""
        inverter = mppinverter.mppInverter('TEST')
        command = inverter.execute('QPIWS')
        print(command)
        self.assertIsInstance(command, mppcommand.mppCommand)

    def test_execute_q1_cmd(self):
        """ test execute of Q1 command (TEST connection)"""
        inverter = mppinverter.mppInverter('TEST')
        command = inverter.execute('Q1')
        print(command)
        self.assertIsInstance(command, mppcommand.mppCommand)

    def test_execute_qid_cmd(self):
        """ test execute of QID command (Serial connection)"""
        inverter = mppinverter.mppInverter('/dev/ttyUSB0')
        command = inverter.execute('Q1')
        print(command)
        self.assertIsInstance(command, mppcommand.mppCommand)

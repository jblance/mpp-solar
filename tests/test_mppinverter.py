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
        self.assertIsInstance(inverter.execute('QPIRI'), mppcommand.mppCommand)

#     #def test_knowncommands(self):
#         #""" getKnownCommands should return a list """
#         #self.assertIsInstance(mppcommands.getKnownCommands(), list)
#     #def test_getcommandtype(self):
#         #""" check getcommandtype returns correct type for simple matches """
#         #self.assertEqual(mppcommands.getCommandType('QPIRI'), 'QUERY')
#         #self.assertEqual(mppcommands.getCommandType('QMCHGCR'), 'QUERY')
#     #def test_getcommandtype_complex(self):
#         #""" check getcommandtype returns correct type for complex (regex) matches """
#         #self.assertEqual(mppcommands.getCommandType('QPGS0'), 'QUERY')
#         #self.assertEqual(mppcommands.getCommandType('PBT02'), 'SETTER')
#         #self.assertEqual(mppcommands.getCommandType('PSDV56.4'), 'SETTER')
#     #def test_getcommandtype_unknown(self):
#         #""" check getcommandtype returns UNKNOWN for unknown commands """
#         #self.assertEqual(mppcommands.getCommandType('NOTREAL'), 'UNKNOWN')  # Not a valid command
#         #self.assertEqual(mppcommands.getCommandType('PBT03'), 'UNKNOWN')  # Invalid option
#     #def test_getcommandcode(self):
#         #""" check getcommand code returns correct code """
#         #self.assertEqual(mppcommands.getCommandCode('QPIGS'), 'QPIGS')
#         #self.assertEqual(mppcommands.getCommandCode('QPIRI'), 'QPIRI')
#         #self.assertEqual(mppcommands.getCommandCode('QPGS0'), 'QPGSn')
#         #self.assertEqual(mppcommands.getCommandCode('PSDV56.4'), 'PSDVnn.n')
#     #def test_getcommandcode_invalid(self):
#         #""" getcommand code returns None when invalid command used """
#         #self.assertIsNone(mppcommands.getCommandCode('PBT99'))  # Invalid option
#         #self.assertIsNone(mppcommands.getCommandCode('INVALID'))  # Invalid command
#     #def test_getresponsedefinition(self):
#         #""" getResponseDefinition should return correct response code for valid commands """
#         #self.assertEqual(mppcommands.getResponseDefinition('QVFW'), [['string', 'Main CPU firmware version', '']])
#         #self.assertEqual(mppcommands.getResponseDefinition('PBT01'), [['ack', 'Command execution', {'NAK': 'Failed', 'ACK': 'Successful'}]])
#     #def test_getresponsedefinition_invalid(self):
#         #""" getResponseDefinition should return none for invalid commands """
#         #self.assertIsNone(mppcommands.getResponseDefinition('PBT69'))  # Invalid option
#         #self.assertIsNone(mppcommands.getResponseDefinition('INVALID'))  # Invalid command
#     #def test_iscommandvalid(self):
#         #""" isCommandValid should return True for valid commands """
#         #self.assertTrue(mppcommands.isCommandValid('QPIGS'))  # Simple match
#         #self.assertTrue(mppcommands.isCommandValid('PSDV56.4'))  # Complex match
#     #def test_iscommandvalid_invalid(self):
#         #""" isCommandValid should return False for invalid commands """
#         #self.assertFalse(mppcommands.isCommandValid('INVALID'))
#     #def test_isresponsevalid(self):
#         #""" isResponseVaild should return true for valid responses """
#         #mp = mppcommands.mppCommands('/dev/ttyUSB0')
#         #qpiri_resp = "(230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10 010 1 0 0 6 01 0 0 54.0 0 1o~\r"
#         #self.assertTrue(mp.isResponseValid('QPIRI', qpiri_resp))
#         #self.assertTrue(mp.isResponseValid('PBT01', '(NAKss\r'))
#         #self.assertTrue(mp.isResponseValid('PBT01', '(ACK9 \r'))
#     #def test_isresponsevalid_invalid(self):
#         #""" isResponseValid should return false for invalid responses """
#         #mp = mppcommands.mppCommands('/dev/ttyUSB0')
#         #qpiri_resp = "(230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10 010 1 0 0 6 01 0 0 54.0 0 1o~\r"
#         #qpiri_resp_inv_crc = "(230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10 010 1 0 0 6 01 0 0 54.0 0 1oo\r"
#         #qpiri_resp_nocrc = "(230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10 010 1 0 0 6 01 0 0 54.0 0"
#         #qpiri_resp_missing = "(230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10\x86\xc1\r"
#         #self.assertFalse(mp.isResponseValid('QPIRI', '(2'))  # Response too short
#         #self.assertFalse(mp.isResponseValid('QPIRI', qpiri_resp_inv_crc))  # Invalid crc in response
#         #self.assertFalse(mp.isResponseValid('QPIRI', qpiri_resp_nocrc))  # No crc in response
#         #self.assertFalse(mp.isResponseValid('QPIRI', qpiri_resp_missing))  # To few elements in response
#         #self.assertFalse(mp.isResponseValid('INVALID', qpiri_resp))  # Invalid command
#         #self.assertFalse(mp.isResponseValid('PBT01', '(INV%A\r'))  # Invalid command
#     #def test_getcommandfullstring(self):
#         #""" getCommandFullString should return full command """
#         #self.assertEqual(mppcommands.getCommandFullString('QPIRI'), 'QPIRI\xf8T\r')
#         #self.assertEqual(mppcommands.getCommandFullString('QPIGS'), 'QPIGS\xb7\xa9\r')
#     #def test_getresponse(self):
#         #""" getResponse should return a valid raw response - only for QPIRI """
#         #mp = mppcommands.mppCommands('TEST')  # Use test serial device
#         #qpiri_resp = mp.getResponse('QPIRI')
#         #qpiws_resp = mp.getResponse('QPIWS')
#         #self.assertEqual(qpiri_resp, "230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10 010 1 0 0 6 01 0 0 54.0 0 1")
#         #self.assertEqual(qpiws_resp, "00000100000000000000000000000000")
#     #def test_invalidtestcommand(self):
#         #""" getResponse should raise an exception if a test is attempted for a command without a test defined"""
#         #mp = mppcommands.mppCommands('TEST')  # Use test serial device
#         #self.assertRaises(mppcommands.NoTestResponseDefined, mp.getResponse, 'QPGS0')
#     #def test_getresponsedict(self):
#         #""" getResponseDict should return a valid dict """
#         #mp = mppcommands.mppCommands('TEST')  # Use test serial device
#         #qpiri_resp = mp.getResponseDict('QPIRI')
#         #qpiws_resp = mp.getResponseDict('QPIWS')
#         #self.assertEqual(qpiri_resp, qpiri_resp)  # TODO Fix
#         #self.assertEqual(qpiws_resp, qpiws_resp)  # TODO Fix

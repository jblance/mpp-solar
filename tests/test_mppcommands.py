import unittest
from mppsolar import mppcommands


class test_mppcommands(unittest.TestCase):
    def test_trunc_function(self):
        """ Test trunc function correctly returns truncated / padded text """
        self.assertEqual(mppcommands.trunc('Short test'), 'Short test                       ')
        self.assertEqual(mppcommands.trunc('A very much looonnger test string'), 'A very much looonnger test str...')

    def test_crc(self):
        """ Test crc function generates correct crc """
        self.assertListEqual(mppcommands.crc('QPIGS'), [183, 169])
        self.assertListEqual(mppcommands.crc('QPIRI'), [248, 84])
        self.assertListEqual(mppcommands.crc('PSDV56.4'), [249, 224])

    def test_failed_initialisation(self):
        """ Initialisation should fail if no device provided """
        self.assertRaises(mppcommands.NoDeviceError, mppcommands.mppCommands)

    def test_knowncommands(self):
        """ getKnownCommands should return a list """
        mp = mppcommands.mppCommands('/dev/ttyUSB0')
        self.assertIsInstance(mp.getKnownCommands(), list)

    def test_getcommandtype(self):
        """ check getcommandtype returns correct type for simple matches """
        mp = mppcommands.mppCommands('/dev/ttyUSB0')
        self.assertEqual(mp.getCommandType('QPIRI'), 'QUERY')
        self.assertEqual(mp.getCommandType('QMCHGCR'), 'QUERY')

    def test_getcommandtype_complex(self):
        """ check getcommandtype returns correct type for complex (regex) matches """
        mp = mppcommands.mppCommands('/dev/ttyUSB0')
        self.assertEqual(mp.getCommandType('QPGS0'), 'QUERY')
        self.assertEqual(mp.getCommandType('PBT02'), 'SETTER')
        self.assertEqual(mp.getCommandType('PSDV56.4'), 'SETTER')

    def test_getcommandtype_unknown(self):
        """ check getcommandtype returns UNKNOWN for unknown commands """
        mp = mppcommands.mppCommands('/dev/ttyUSB0')
        self.assertEqual(mp.getCommandType('NOTREAL'), 'UNKNOWN')  # Not a valid command
        self.assertEqual(mp.getCommandType('PBT03'), 'UNKNOWN')  # Invalid option

    def test_getcommandcode(self):
        """ check getcommand code returns correct code """
        mp = mppcommands.mppCommands('/dev/ttyUSB0')
        self.assertEqual(mp.getCommandCode('QPIGS'), 'QPIGS')
        self.assertEqual(mp.getCommandCode('QPIRI'), 'QPIRI')
        self.assertEqual(mp.getCommandCode('QPGS0'), 'QPGSn')
        self.assertEqual(mp.getCommandCode('PSDV56.4'), 'PSDVnn.n')

    def test_getcommandcode_invalid(self):
        """ getcommand code returns None when invalid command used """
        mp = mppcommands.mppCommands('/dev/ttyUSB0')
        self.assertIsNone(mp.getCommandCode('PBT99'))  # Invalid option
        self.assertIsNone(mp.getCommandCode('INVALID'))  # Invalid command

    def test_getresponsedefinition(self):
        """ getResponseDefinition should return correct response code for valid commands """
        mp = mppcommands.mppCommands('/dev/ttyUSB0')
        self.assertEqual(mp.getResponseDefinition('QVFW'), [['string', 'Main CPU firmware version', '']])
        self.assertEqual(mp.getResponseDefinition('PBT01'), [['ack', 'Command execution', {'NAK': 'Failed', 'ACK': 'Successful'}]])

    def test_getresponsedefinition_invalid(self):
        """ getResponseDefinition should return none for invalid commands """
        mp = mppcommands.mppCommands('/dev/ttyUSB0')
        self.assertIsNone(mp.getResponseDefinition('PBT69'))  # Invalid option
        self.assertIsNone(mp.getResponseDefinition('INVALID'))  # Invalid command

    def test_iscommandvalid(self):
        """ isCommandValid should return True for valid commands """
        mp = mppcommands.mppCommands('/dev/ttyUSB0')
        self.assertTrue(mp.isCommandValid('QPIGS'))  # Simple match
        self.assertTrue(mp.isCommandValid('PSDV56.4'))  # Complex match

    def test_iscommandvalid_invalid(self):
        """ isCommandValid should return False for invalid commands """
        mp = mppcommands.mppCommands('/dev/ttyUSB0')
        self.assertFalse(mp.isCommandValid('INVALID'))

    def test_isresponsevalid(self):
        """ isResponseVaild should return true for valid responses """
        mp = mppcommands.mppCommands('/dev/ttyUSB0')
        qpiri_resp = "(230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10 010 1 0 0 6 01 0 0 54.0 0 1o~\r"
        self.assertTrue(mp.isResponseValid('QPIRI', qpiri_resp))

    def test_isresponsevalid_invalid(self):
        """ isResponseValid should return false for invalid responses """
        mp = mppcommands.mppCommands('/dev/ttyUSB0')
        qpiri_resp = "(230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10 010 1 0 0 6 01 0 0 54.0 0 1o~\r"
        qpiri_resp_inv_crc = "(230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10 010 1 0 0 6 01 0 0 54.0 0 1oo\r"
        qpiri_resp_nocrc = "(230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10 010 1 0 0 6 01 0 0 54.0 0"
        qpiri_resp_missing = "(230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10 010 1 0 0 6 \x12h\r"
        self.assertFalse(mp.isResponseValid('QPIRI', '(2'))  # Response too short
        self.assertFalse(mp.isResponseValid('QPIRI', qpiri_resp_inv_crc))  # Invalid crc in response
        self.assertFalse(mp.isResponseValid('QPIRI', qpiri_resp_nocrc))  # No crc in response
        self.assertFalse(mp.isResponseValid('QPIRI', qpiri_resp_missing))  # To few elements in response
        self.assertFalse(mp.isResponseValid('INVALID', qpiri_resp))  # Invalid command

    def test_getcommandfullstring(self):
        """ getCommandFullString should return full command """
        mp = mppcommands.mppCommands('/dev/ttyUSB0')
        self.assertEqual(mp.getCommandFullString('QPIRI'), 'QPIRI\xf8T\r')
        self.assertEqual(mp.getCommandFullString('QPIGS'), 'QPIGS\xb7\xa9\r')

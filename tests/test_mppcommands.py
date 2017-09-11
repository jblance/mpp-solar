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

import unittest
from mppsolar import mppcommands


class test_mppcommands(unittest.TestCase):
    def test_trunc_function(self):
        """ Test trunc function correctly returns truncated / padded text """
        self.assertEqual(mppcommands.trunc('Short text'), 'Short test                       ')
        self.assertEqual(mppcommands.trunc('A very much looonnger test string'), 'A very much looonnger test str...')

    def test_failed_initialisation(self):
        """ Initialisation should fail if no device provided """
        self.assertRaises(mppcommands.NoDeviceError, mppcommands.mppCommands)

    def test_knowncommands(self):
        """ getKnownCommands should return a list """
        mp = mppcommands.mppCommands('/dev/ttyUSB0')
        self.assertIsInstance(mp.getKnownCommands(), list)

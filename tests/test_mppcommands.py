import unittest
import array
from mppsolar import mppcommands


class test_mppcommands(unittest.TestCase):
    def test_failed_initialisation(self):
        """ Initialisation should fail if no device provided """
        self.assertRaises(mppcommands.NoDeviceError, mppcommands.mppCommands)

    def test_knowncommands(self):
        """ getKnownCommands should return a list """
        mp = mppcommands.mppCommands('/dev/ttyUSB0')
        self.assertIsInstance(mp.getKnownCommands(), list)

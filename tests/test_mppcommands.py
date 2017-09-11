import unittest
from mppsolar import mppcommands


class test_mppcommands(unittest.TestCase):
    def test_1(self):
        mp = mppcommands.mppCommands('/dev/ttyUSB0')
        self.assertIsInstance(mp.getKnownCommands(), array.array)

    def test_init1(self):
        """ Initialisation should fail if no device provided """
        self.assertRaises(mppcommands.NoDeviceError, mppcommands.mppCommands)

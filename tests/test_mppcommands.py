import unittest
from mppsolar import mppcommands


class test_mppcommands(unittest.TestCase):
    def test_1(self):
        mp = mppcommands.mppCommands('/dev/ttyUSB0')
        mp.getKnownCommands()
        return True

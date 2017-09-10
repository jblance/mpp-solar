import unittest
from mppsolar.mppcommands import mppCommands


class test_mppcommands(unittest.TestCase):
    def testOne(self):
        mp = mppCommands('/dev/ttyUSB0')
        mp.getKnownCommands()
        return True

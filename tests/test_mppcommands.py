import unittest
from mppsolar.mpputils import mppUtils


class test_mppcommands(unittest.TestCase):
    def testOne(self):
        mp = mppUtils('/dev/ttyUSB0')
        mp.getKnownCommands()
        return True

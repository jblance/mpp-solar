import unittest
from .mppsolar import mpputils


class test_mppcommands(unittest.TestCase):
    def testOne(self):
        mp = mpputils.mppUtils('/dev/ttyUSB0')
        mp.getKnownCommands()
        return True

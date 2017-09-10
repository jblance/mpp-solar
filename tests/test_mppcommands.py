import unittest
from mppcommands import mppCommands


class test_mppcommands(unittest.TestCase):
    def check_1(self):
        mp = mppCommands()
        mp.getKnownCommands()
        return True

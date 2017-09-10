import unittest
import mppcommands


class test_mppcommands(unittest.TestCase):
    def check_1(self):
        mp = mppcommands.mppCommands()
        mp.getKnownCommands()
        return True

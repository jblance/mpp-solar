import unittest
from mppsolar import mppcommand


class test_mppcommand(unittest.TestCase):
    def test_crc(self):
        """ Test crc function generates correct crc """
        self.assertListEqual(mppcommand.crc('QPIGS'), [183, 169])
        self.assertListEqual(mppcommand.crc('QPIRI'), [248, 84])
        self.assertListEqual(mppcommand.crc('PSDV56.4'), [249, 224])
        self.assertListEqual(mppcommand.crc('186'), [41, 60])
        self.assertListEqual(mppcommand.crc('196'), [27, 14])

import unittest
from mppsolar import mppcommand

from builtins import bytes

class test_mppcommand(unittest.TestCase):
    def test_crc(self):
        """ Test crc function generates correct crc """
        self.assertListEqual(mppcommand.crc(bytes('QPIGS', 'utf-8')), [183, 169])
        self.assertListEqual(mppcommand.crc(bytes('QPIRI', 'utf-8')), [248, 84])
        self.assertListEqual(mppcommand.crc(bytes('PSDV56.4', 'utf-8')), [249, 224])
        self.assertListEqual(mppcommand.crc(bytes('186', 'utf-8')), [41, 60])
        self.assertListEqual(mppcommand.crc(bytes('196', 'utf-8')), [27, 14])

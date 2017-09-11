import unittest
import array
from mppsolar import mppcommands


class test_mppcommands(unittest.TestCase):
    def test_1(self):
        known = ['-------- List of known commands --------', 'PBTnn: Set Battery Type', 'PSDVnn.n: Set Battery Cut-off Voltage', 'Q1: Q1 query', 'QBOOT: DSP Has Bootstrap inquiry', 'QDI: Device Default Settings inquiry', 'QDM: QDM query', 'QFLAG: Device Flag Status inquiry', 'QID: Device Serial Number inquiry', 'QMCHGCR: Max Charging Current Options inquiry', 'QMN: QMN query', 'QMUCHGCR: Max Utility Charging Current Options inquiry', 'QOPM: Output Mode inquiry', 'QPGSn: Parallel Information inquiry', 'QPI: Device Protocol ID inquiry', 'QPIGS: Device General Status Parameters inquiry', 'QPIRI: Device Current Settings inquiry', 'QPIWS: Device warning status inquiry', 'QVFW: Main CPU firmware version inquiry', 'QVFW2: Secondary CPU firmware version inquiry']
        mp = mppcommands.mppCommands('/dev/ttyUSB0')
        self.assertListEqual(IsInstance(mp.getKnownCommands(), known)

    def test_init1(self):
        """ Initialisation should fail if no device provided """
        self.assertRaises(mppcommands.NoDeviceError, mppcommands.mppCommands)

""" tests / unit / test_protocol_pi30revo.py """
import unittest

from mppsolar.protocols.jk02 import jk02 as proto

protocol = proto()

def set_balance_start(value):
    assert value > 1500 and value < 4500
    # see https://github.com/jblance/mpp-solar/issues/114
    setBalanceStart2500 = bytearray([0xAA, 0x55, 0x90, 0xEB, 0x26, 0x04, 0xc4, 0x09, 0x00, 0x00, 0x23, 0xB2, 0xCD, 0x31, 0x2D, 0x28, 0xF2, 0x6B, 0x04, 0xFA])
    x = setBalanceStart2500.copy()
    x[7] = int(value / 256)
    x[6] = value % 256
    x[-1] = sum(x[0:-1])%256
    #print('%x %x %x' % (x[6], x[7], x[-1]))
    # assert x == setBalanceStart2500
    # print(setBalanceStart2500)
    return x


class TestJk02(unittest.TestCase):
    """ unit tests of jk02 protocol """
    maxDiff = None

    def test_get_full_command_get_cell_data(self):
        """ test for full command generation for getCellData"""
        result = protocol.get_full_command("getCellData")
        expected = b'\xaaU\x90\xeb\x96\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10'
        # print(result)
        # print(expected)
        self.assertEqual(expected, result)


    def test_get_full_command_set_cell_ovp(self):
        """ test for full command generation for setCellOVP"""
        result = protocol.get_full_command("setCellOVP3.65")
        expected = b'\xaaU\x90\xeb\x04\x04B\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd2'
        # print()
        # print('result', result)
        # print('expect', bytearray(expected))
        # print(set_balance_start(2500))
        self.assertEqual(expected, result)

    def test_get_full_command_set_balance_start(self):
        """ test for full command generation for setBalanceStart2.5"""
        # return
        result = protocol.get_full_command("setBalanceStart2.5")
        expected = b'\xaaU\x90\xeb&\x04\xc4\t\x00\x00#\xb2\xcd1-(\xf2k\x04\xfa'
        # print()
        # print("result", result)
        # print("expect", bytearray(expected))
        # print("bal2.5", set_balance_start(2500))
        # for i, x in enumerate(result):
        #     print(i, hex(result[i]), hex(expected[i]), result[i]==expected[i])
        self.assertEqual(expected, result)

    def test_get_full_command_set_charging_on(self):
        """ test for full command generation for setChargingOn"""
        result = protocol.get_full_command("setChargingOn")
        expected = b'\xaaU\x90\xeb\x1d\x04\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x9c'
        # print()
        # print("result", result)
        # print("expect", bytearray(expected))
        # for i, x in enumerate(result):
        #     print(i, hex(result[i]), hex(expected[i]), result[i]==expected[i])
        self.assertEqual(expected, result)

    def test_get_full_command_set_charging_off(self):
        """ test for full command generation for setChargingOff """
        result = protocol.get_full_command("setChargingOff")
        expected = b'\xaaU\x90\xeb\x1d\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x9b'
        # print()
        # print("result", result)
        # print("expect", bytearray(expected))
        # for i, x in enumerate(result):
        #     print(i, hex(result[i]), hex(expected[i]), result[i]==expected[i])
        self.assertEqual(expected, result)

    def test_get_full_command_set_discharging_on(self):
        """ test for full command generation for setDischargingOn"""
        result = protocol.get_full_command("setDischargingOn")
        expected = b'\xaaU\x90\xeb\x1e\x04\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x9d'
        # print()
        # print("result", result)
        # print("expect", bytearray(expected))
        # for i, x in enumerate(result):
        #     print(i, hex(result[i]), hex(expected[i]), result[i]==expected[i])
        self.assertEqual(expected, result)

    def test_get_full_command_set_discharging_off(self):
        """ test for full command generation for setDishargingOff """
        result = protocol.get_full_command("setDischargingOff")
        expected = b'\xaaU\x90\xeb\x1e\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x9c'
        # print()
        # print("result", result)
        # print("expect", bytearray(expected))
        # for i, x in enumerate(result):
        #     print(i, hex(result[i]), hex(expected[i]), result[i]==expected[i])
        self.assertEqual(expected, result)

    # def test_checksum_pset(self):
    #     """ test for correct checksum for PSET command """
    #     command = 'PSET120103 56.3 54.6 43.8 42.6 040 020 2020 02 18 17 06 00'
    #     byte_cmd = bytes(command, "utf-8")
    #     result = protocol.get_chk(byte_cmd)
    #     expected = 0xf7  # note documentation has f6 but tests have shown this is incorrect
    #     # print(hex(result))
    #     # print(expected)
    #     self.assertEqual(expected, result)

    # def test_check_response_valid_qlith0(self):
    #     """ test for correctly validating valid qlith0 response """
    #     response = b'(052.5 000.0 000.0 032 036 000 070.0 007.0 057.0 004.6 0 5\x82\xe0\r'
    #     result = protocol.check_response_valid(response)[0]
    #     # print(result)
    #     self.assertTrue(result)

    # def test_decode_qlith0(self):
    #     """ test successful decode of QLITH0 response """
    #     expected = {'_command': 'QLITH0', '_command_description': 'Read lithium battery information', 'raw_response': ['(052.5 000.0 000.0 032 036 000 070.0 007.0 057.0 004.6 0 5\x82à\r', ''], 'Battery voltage from BMS': [52.5, 'V'], 'Battery charging current from BMS': [0.0, 'A'], 'Battery discharge current from BMS': [0.0, 'A'], 'Battery temperature': [32, '0.1°C'], 'Battery capacity from BMS': [36, '%'], 'Battery wearout': [0, '%'], 'Battery max charging current': [70.0, 'A'], 'Battery max discharge current': [7.0, 'A'], 'Battery max charge voltage': [57.0, 'V'], 'Battery min discharge voltage': [4.6, 'V'], 'Fault Code from BMS': ['No warning', ''], 'Warning Code fom BMS': ['Battery overcurrent', '']}
    #     response = b'(052.5 000.0 000.0 032 036 000 070.0 007.0 057.0 004.6 0 5\x82\xe0\r'
    #     result = protocol.decode(response, "QLITH0")
    #     # print(result)
    #     self.assertEqual(expected, result)

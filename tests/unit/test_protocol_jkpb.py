""" tests / unit / test_protocol_jkpb.py """
import unittest

from mppsolar.protocols.jkpb import jkpb as Proto

# import construct as cs
proto = Proto()


class TestProtocolJkpb(unittest.TestCase):
    """ exercise different functions in JKPB protocol """

    # def test_check_crc(self):
    #     """ test a for correct CRC validation """
    #     _result = proto.check_crc(response=b"(0 100 0 0 1 532 532 450 0000 0030\x0e\x5E\n", command_definition=proto.get_command_definition('QBMS'))
    #     # print(_result)
    #     self.assertTrue(_result)

    # def test_check_crc_incorrect(self):
    #     """ test an exception is raised if CRC validation fails """
    #     self.assertRaises(InvalidCRC, proto.check_crc, response=b"(0 100 0 0 1 532 532 450 0000 0030\x0e\x5D\n", command_definition=proto.get_command_definition('QBMS'))

    # def test_trim(self):
    #     """ test protocol does a correct trim operation """
    #     _result = proto.trim_response(response=b"(0 100 0 0 1 532 532 450 0000 0030\x0e\x5E\n", command_definition=proto.get_command_definition('QBMS'))
    #     expected = b'0 100 0 0 1 532 532 450 0000 0030'
    #     # print(_result)
    #     self.assertEqual(_result, expected)

    # def test_check_valid_ok(self):
    #     """ test protocol returns true for a correct response validation check """
    #     _result = proto.check_valid(response=b"(0 100 0 0 1 532 532 450 0000 0030\x0e\x5E\n")
    #     expected = True
    #     # print(_result)
    #     self.assertEqual(_result, expected)

    # def test_check_valid_none(self):
    #     """ test protocol returns false for a None response validation check """
    #     self.assertRaises(InvalidResponse, proto.check_valid, response=None)

    # def test_check_valid_short(self):
    #     """ test protocol returns false for a short response validation check """
    #     self.assertRaises(InvalidResponse, proto.check_valid, response=b"(0")

    # def test_check_valid_missing(self):
    #     """ test protocol returns false for a response missing start char validation check """
    #     self.assertRaises(InvalidResponse, proto.check_valid, response=b"0 100 0 0 1 532 532 450 0000 0030\x0e\x5E\n")


    def test_full_command_getBalancerData(self):
        """ test a for correct full command for getBalancerData """
        _result = proto.get_full_command(command="getBalancerData")
        expected = bytearray.fromhex('011016 1C 0001020000D3CD')
        # print()
        # print(expected)
        # print(_result)
        self.assertEqual(_result, expected)

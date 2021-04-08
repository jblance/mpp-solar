#!/usr/bin/env python3
import logging

from binascii import unhexlify
from struct import unpack

log = logging.getLogger("protocol_helpers")


def crc8(byteData):
    """
    Generate 8 bit CRC of supplied string
    """
    CRC = 0
    # for j in range(0, len(str),2):
    for b in byteData:
        # char = int(str[j:j+2], 16)
        # print(b)
        CRC = CRC + b
        CRC &= 0xFF
    return CRC


def vedHexChecksum(byteData):
    """
    Generate VE Direct HEX Checksum
     - sum of byteData + CS = 0x55
    """
    CS = 0x55
    for b in byteData:
        CS -= b
    CS = CS & 0xFF
    return CS


def decode2ByteHex(hexString):
    """
    Code a 2 byte hexString to volts as per jkbms approach (blackbox determined)
    - need to decode as 4 hex chars
    """
    log.debug(f"hexString: {hexString}")

    answer = 0.0

    # Make sure supplied String is the correct length
    if len(hexString) != 2:
        log.warning(f"Hex encoded value must be 2 bytes long. Was {len(hexString)} length")
        return 0

    # Use python tools for decode
    answer = unpack("<h", hexString)[0] / 1000
    log.info(f"Hex {hexString} 2 byte decoded to {answer}")

    return answer


def decode4ByteHex1000(hexToDecode):
    """
    Code a 4 byte hexString  per jkbms approach (blackbox determined)
    - need to decode as 8 hex chars
    """
    # hexString = bytes.fromhex(hexToDecode)
    hexString = hexToDecode
    log.debug(f"hexString: {hexString}")

    answer = 0.0

    # Make sure supplied String is long enough
    if len(hexString) != 4:
        log.warning(f"Hex encoded value must be 4 bytes long. Was {len(hexString)} length")
        return 0

    # 1st position
    pos1 = hexString[0] >> 4
    answer += pos1 * (2 ** 4 / 1000)
    log.debug(f"answer after pos1 {answer}")
    # 2nd position
    pos2 = hexString[0] & 0x0F
    answer += pos2 * (2 ** 0 / 1000)
    log.debug(f"answer after pos2 {answer}")
    # 3rd position
    pos3 = hexString[1] >> 4
    answer += pos3 * (2 ** 12 / 1000)
    log.debug(f"answer after pos3 {answer}")
    # 4th position
    pos4 = hexString[1] & 0x0F
    answer += pos4 * (2 ** 8 / 1000)
    # 5st position
    pos5 = hexString[2] >> 4
    answer += pos5 * (2 ** 20 / 1000)
    log.debug(f"answer after pos5 {answer}")
    # 6st position
    pos6 = hexString[2] & 0x0F
    answer += pos6 * (2 ** 16 / 1000)
    log.debug(f"answer after pos6 {answer}")
    # 7th position
    pos7 = hexString[3] >> 4
    answer += pos7 * (2 ** 28 / 1000)
    log.debug(f"answer after pos7 {answer}")
    # 8th position
    pos8 = hexString[3] & 0x0F
    answer += pos8 * (2 ** 24 / 1000)

    log.debug(f"answer after pos8 {answer}")
    log.info(f"Hex {hexString} 8 byte decoded to {answer}")

    return answer


def decode4ByteHex(hexToDecode):
    """
    Code a 4 byte hexString to volts as per jkbms approach (blackbox determined)
    """
    # hexString = decode2ByteHex
    hexString = hexToDecode
    log.debug(f"hexString: {hexString}")

    answer = 0.0

    # Make sure supplied String is long enough
    if len(hexString) != 4:
        log.warning(f"Hex encoded value must be 4 bytes long. Was {len(hexString)} length")
        return 0

    # Use python tools for decode
    answer = unpack("<f", hexString)[0]
    log.info(f"Hex {hexString} 4 byte decoded to {answer}")

    return answer


def crcPI(data_bytes):
    """
    Calculates CRC for supplied data_bytes
    """
    # assert type(byte_cmd) == bytes
    log.debug(f"Calculating CRC for {data_bytes}")

    crc = 0
    da = 0
    crc_ta = [
        0x0000,
        0x1021,
        0x2042,
        0x3063,
        0x4084,
        0x50A5,
        0x60C6,
        0x70E7,
        0x8108,
        0x9129,
        0xA14A,
        0xB16B,
        0xC18C,
        0xD1AD,
        0xE1CE,
        0xF1EF,
    ]

    for c in data_bytes:
        # log.debug('Encoding %s', c)
        if type(c) == str:
            c = ord(c)
        da = ((crc >> 8) & 0xFF) >> 4
        crc = (crc << 4) & 0xFFFF

        index = da ^ (c >> 4)
        crc ^= crc_ta[index]

        da = ((crc >> 8) & 0xFF) >> 4
        crc = (crc << 4) & 0xFFFF

        index = da ^ (c & 0x0F)
        crc ^= crc_ta[index]

    crc_low = crc & 0xFF
    crc_high = (crc >> 8) & 0xFF

    if crc_low == 0x28 or crc_low == 0x0D or crc_low == 0x0A:
        crc_low += 1
    if crc_high == 0x28 or crc_high == 0x0D or crc_high == 0x0A:
        crc_high += 1

    crc = crc_high << 8
    crc += crc_low

    log.debug(f"Generated CRC {crc_high:#04x} {crc_low:#04x} {crc:#06x}")
    return [crc_high, crc_low]

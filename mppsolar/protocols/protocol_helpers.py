#!/usr/bin/env python3
import logging

log = logging.getLogger("MPP-Solar")


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


def decode2ByteHex(hexToDecode):
    """
    Code a 2 byte hexString to volts as per jkbms approach (blackbox determined)
    - need to decode as 4 hex chars
    """
    # hexString = bytes.fromhex(hexToDecode)
    hexString = hexToDecode
    log.debug(f"hexString: {hexString}")

    answer = 0.0

    # Make sure supplied String is long enough
    if len(hexString) != 2:
        log.warning(f"Hex encoded value must be 2 bytes long. Was {len(hexString)} length")
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
    log.debug(f"answer after pos4 {answer}")
    log.info(f"Hex {hexString} 2 byte decoded to {answer}")

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

    # Process most significant byte (position 3)
    byte1 = hexString[3]
    if byte1 == 0x0:
        return 0
    byte1Low = byte1 - 0x40
    answer = (2 ** (byte1Low * 2)) * 2
    log.debug(f"After position 3: {answer}")
    step1 = answer / 8.0
    step2 = answer / 128.0
    step3 = answer / 2048.0
    step4 = answer / 32768.0
    step5 = answer / 524288.0
    step6 = answer / 8388608.0

    # position 2
    byte2 = hexString[2]
    byte2High = byte2 >> 4
    byte2Low = byte2 & 0xF
    if byte2High & 8:
        answer += ((byte2High - 8) * step1 * 2) + (8 * step1) + (byte2Low * step2)
    else:
        answer += (byte2High * step1) + (byte2Low * step2)
    log.debug(f"After position 2: {answer}")
    # position 1
    byte3 = hexString[1]
    byte3High = byte3 >> 4
    byte3Low = byte3 & 0xF
    answer += (byte3High * step3) + (byte3Low * step4)
    log.debug(f"After position 1: {answer}")
    # position 0
    byte4 = hexString[0]
    byte4High = byte4 >> 4
    byte4Low = byte4 & 0xF
    answer += (byte4High * step5) + (byte4Low * step6)
    log.debug(f"After position 0: {answer}")
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
        # todo fix response for older python
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

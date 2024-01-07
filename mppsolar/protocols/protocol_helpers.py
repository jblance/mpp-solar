#!/usr/bin/env python3
import logging
import math

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


def crc8P1(byteData):
    """
    Generate 8 bit CRC of supplied string + 1
    eg as used in REVO PI30 protocol
    """
    CRC = 0
    for b in byteData:
        CRC = CRC + b
    CRC += 1
    CRC &= 0xFF
    return CRC


def crcJK232(byteData):
    """
    Generate JK RS232 / RS485 CRC
    - 2 bytes, the verification field is "command code + length byte + data segment content",
    the verification method is thesum of the above fields and then the inverse plus 1, the high bit is in the front and the low bit is in the back.
    """
    CRC = 0
    for b in byteData:
        CRC += b
    crc_low = CRC & 0xFF
    crc_high = (CRC >> 8) & 0xFF
    return [crc_high, crc_low]    

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


def uptime(byteData):
    """
    Decode 3 hex bytes to a JKBMS uptime
    """
    # Make sure supplied String is the correct length
    log.debug("uptime defn")
    value = 0
    for x, b in enumerate(byteData):
        # b = byteData.pop(0)
        value += b * 256 ** x
        log.debug(f"Uptime int value {value} for pos {x}")
    daysFloat = value / (60 * 60 * 24)
    days = math.trunc(daysFloat)
    hoursFloat = (daysFloat - days) * 24
    hours = math.trunc(hoursFloat)
    minutesFloat = (hoursFloat - hours) * 60
    minutes = math.trunc(minutesFloat)
    secondsFloat = (minutesFloat - minutes) * 60
    seconds = round(secondsFloat)
    uptime = f"{days}D{hours}H{minutes}M{seconds}S"
    log.info(f"Uptime result {uptime}")
    return uptime


def Hex2Int(hexString):
    """
    Decode the first byte of a hexString to int
    """
    answer = hexString[0]
    log.debug(f"Hex {hexString} decoded to {answer}")

    return answer


def Hex2Str(hexString):
    """
    Return the hexString as ASCII representation of hex, ie 0x4a -> 4a
    """
    answer = ""
    for x in hexString:
        answer += f"{x:02x}"

    log.debug(f"Hex {hexString} decoded to {answer}")

    return answer


def Hex2Ascii(hexString):
    """
    Return the hexString as ASCII, ie 0x4a -> J
    """
    answer = ""
    for x in hexString:
        if x != 0:
            # Ignore 0x00 results
            answer += f"{x:c}"

    log.debug(f"Hex {hexString} decoded to {answer}")

    return answer


def LittleHex2Short(hexString):
    """
    Decode a 2 byte hexString to int (little endian coded)
    """
    # Make sure supplied String is the correct length
    if len(hexString) != 2:
        log.info(f"Hex encoded value must be 2 bytes long. Was {len(hexString)} length")
        return 0
    answer = unpack("<h", hexString)[0]
    log.debug(f"Hex {hexString} 2 byte decoded to {answer}")
    return answer


def BigHex2Short(hexString):
    """
    Decode a 2 byte hexString to int (big endian coded)
    """
    # Make sure supplied String is the correct length
    if len(hexString) != 2:
        log.info(f"Hex encoded value must be 2 bytes long. Was {len(hexString)} length")
        return 0
    answer = unpack(">h", hexString)[0]
    log.debug(f"Hex {hexString} 2 byte decoded to {answer}")
    return answer


def BigHex2Float(hexString):
    """
    Decode a 4 byte hexString to int (big endian coded)
    """
    # Make sure supplied String is the correct length
    if len(hexString) != 4:
        log.info(f"Hex encoded value must be 4 bytes long. Was {len(hexString)} length")
        return 0

    answer = unpack(">I", hexString)[0]
    # answer = int(hexString.hex(), 16)
    log.debug(f"Hex {hexString} 4 byte decoded to {answer}")
    return answer


def LittleHex2Float(hexString):
    """
    Decode a 4 byte hexString to int (little endian coded)
    """
    # Make sure supplied String is the correct length
    if len(hexString) != 4:
        log.info(f"Hex encoded value must be 4 bytes long. Was {len(hexString)} length")
        return 0

    answer = unpack("<f", hexString)[0]
    log.debug(f"Hex {hexString} 4 byte decoded to {answer}")
    return answer


def LittleHex2UInt(hexString):
    """
    Decode a 4 byte hexString to Uint (little endian coded)
    """
    # Make sure supplied String is the correct length
    if len(hexString) != 4:
        log.info(f"Hex encoded value must be 4 bytes long. Was {len(hexString)} length")
        return 0

    answer = unpack("<I", hexString)[0]
    log.debug(f"Hex {hexString} 4 byte decoded to {answer}")
    return answer


def LittleHex2Int(hexString):
    """
    Decode a 4 byte hexString to int (little endian coded)
    """
    # Make sure supplied String is the correct length
    if len(hexString) != 4:
        log.info(f"Hex encoded value must be 4 bytes long. Was {len(hexString)} length")
        return 0

    answer = unpack("<i", hexString)[0]
    log.debug(f"Hex {hexString} 4 byte decoded to {answer}")
    return answer


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
    log.debug(f"Hex {hexString} 2 byte decoded to {answer}")

    return answer


def _decode4ByteHex1000(hexToDecode):
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
    log.debug(f"Hex {hexString} 8 byte decoded to {answer}")

    return answer


def _decode4ByteHex(hexToDecode):
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
    log.debug(f"Hex {hexString} 4 byte decoded to {answer}")

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

    if crc_low == 0x28 or crc_low == 0x0D or crc_low == 0x0A or crc_low == 0x00:
        crc_low += 1
    if crc_high == 0x28 or crc_high == 0x0D or crc_high == 0x0A or crc_high == 0x00:
        crc_high += 1

    crc = crc_high << 8
    crc += crc_low

    log.debug(f"Generated CRC {crc_high:#04x} {crc_low:#04x} {crc:#06x}")
    return [crc_high, crc_low]


def get_value(_list, _index):
    """
    get the value from _list or return None if _index is out of bounds
    """
    # print(_list, len(_list))
    if _index >= len(_list):
        return None
    return _list[_index]


def get_resp_defn(key, defns):
    """
    look for a definition for the supplied key
    """
    # print(key, defns)
    if not key:
        return None
    if type(key) is bytes:
        try:
            key = key.decode("utf-8")
        except UnicodeDecodeError:
            log.info(f"key decode error for {key}")
    for defn in defns:
        if key == defn[0]:
            # print(key, defn)
            return defn
    # did not find definition for this key
    log.info(f"No defn found for {key} key")
    return [key, key, "", ""]

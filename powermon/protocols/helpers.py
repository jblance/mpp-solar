""" powermon / protocols / helpers.py """
import logging

log = logging.getLogger("protocol_helpers")


def crc_jk232(byte_data):
    """
    Generate JK RS232 / RS485 CRC
    - 2 bytes, the verification field is "command code + length byte + data segment content",
    the verification method is thesum of the above fields and then the inverse plus 1, the high bit is in the front and the low bit is in the back.
    """
    crc = 0
    for b in byte_data:
        crc += b
    crc_low = crc & 0xFF
    crc_high = (crc >> 8) & 0xFF
    return [crc_high, crc_low] 

def crc_pi30(data_bytes):
    """
    Calculates CRC for supplied data_bytes
    """
    # assert type(byte_cmd) == bytes
    log.debug("Calculating CRC for %s", data_bytes)

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
        if isinstance(c, str):
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

def victron_checksum(byte_data):
    """
    Generate VE Direct HEX Checksum
    - sum of byteData + checksum = 0x55
    """
    checksum = 0x55
    for b in byte_data:
        checksum -= b
    checksum = checksum & 0xFF
    return checksum

    

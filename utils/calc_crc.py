from mppsolar.protocols.protocol_helpers import crcPI as crc
from mppsolar.protocols.protocol_helpers import crc8 as chk

s = '(052.5 000.0 000.0 032 036 000 070.0 007.0 057.0 004.6 0 5'
s = "(048.8 000.0 000.9 250 024 000 052.5 010.0 053.5 004.4 0 2"
byte_s = bytes(s, "utf-8")
# calculate the CRC
crc_high, crc_low = crc(byte_s)
print(f"crc: {crc_high:0x} {crc_low:0x}")

_chk = chk(byte_s)
print(f"chk: {_chk:0x}")

from mppsolar.protocols.protocol_helpers import crcPI as crc

s = "QEY2023"
byte_s = bytes(s, "utf-8")
# calculate the CRC
crc_high, crc_low = crc(byte_s)
print(f"crc: {crc_high:0x} {crc_low:0x}")

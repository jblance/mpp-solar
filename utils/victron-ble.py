import asyncio
from enum import Enum
import sys
from bleak import BleakClient, BleakScanner
from construct import FixedSized, GreedyBytes, Int8sl, Int16ul, Struct, Int24sl
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.Padding import pad


class AuxMode(Enum):
    STARTER_VOLTAGE = 0
    MIDPOINT_VOLTAGE = 1
    TEMPERATURE = 2
    DISABLED = 3


def decrypt_data(raw_data=None, key=None):
    PARSER = Struct(
        "prefix" / FixedSized(2, GreedyBytes),
        # Model ID
        "model_id" / Int16ul,
        # Packet type
        "readout_type" / Int8sl,
        # IV for encryption
        "iv" / Int16ul,
        "encrypted_data" / GreedyBytes)

    data = bytes.fromhex(raw_data)
    advertisement_key = bytes.fromhex(key)
    container = PARSER.parse(data)
    # The first data byte is a key check byte
    if container.encrypted_data[0] != advertisement_key[0]:
        print("AdvertisementKeyMismatchError: Incorrect advertisement key")
        return

    ctr = Counter.new(128, initial_value=container.iv, little_endian=True)

    cipher = AES.new(
        advertisement_key,
        AES.MODE_CTR,
        counter=ctr,
    )
    dec = cipher.decrypt(pad(container.encrypted_data[1:], 16))

    PACKET = Struct(
        # Remaining time in minutes
        "remaining_mins" / Int16ul,
        # Voltage reading in 10mV increments
        "voltage" / Int16ul,
        # Alarm reason
        "alarm" / Int16ul,
        # Value of the auxillary input (millivolts or degrees)
        "aux" / Int16ul,
        # The upper 22 bits indicate the current in milliamps
        # The lower 2 bits identify the aux input mode:
        #   0 = Starter battery voltage
        #   1 = Midpoint voltage
        #   2 = Temperature
        #   3 = Disabled
        "current" / Int24sl,
        # Consumed Ah in 0.1Ah increments
        "consumed_ah" / Int16ul,
        # The lowest 4 bits are unknown
        # The next 8 bits indicate the state of charge in 0.1% increments
        # The upper 2 bits are unknown
        "soc" / Int16ul,
        # Throw away any extra bytes
        GreedyBytes,
    )
    pkt = PACKET.parse(dec)

    aux_mode = AuxMode(pkt.current & 0b11)

    parsed = {
        "remaining_mins": pkt.remaining_mins,
        "aux_mode": aux_mode,
        "current": (pkt.current >> 2) / 1000,
        "voltage": pkt.voltage / 100,
        "consumed_ah": pkt.consumed_ah / 10,
        "soc": ((pkt.soc & 0x3FFF) >> 4) / 10,
        "alarm": pkt.alarm,
    }

    for item, value in parsed.items():
        print(f"{item}: {value}")


async def main():
    address = 'C2:B0:0C:CC:7D:BC'

    # async with BleakClient(address) as client:
    #     if (not client.is_connected):
    #         raise Exception("client not connected")
    #     print(client)

    #     print('writing to keepalive')
    #     res = await client.write_gatt_char(42, bytearray(b'0\xff'))
    #     print(f"{res=}")

    #     print('reading soc')
    #     char = await client.read_gatt_char('65970fff-4bda-4c1e-af4b-551c4cf74769')
    #     print(f"{char=}")
    stop_event = asyncio.Event()

    # TODO: add something that calls stop_event.set()

    def callback(device, advertising_data):
        print(f"callback {device}: {advertising_data}")

    async with BleakScanner(callback) as scanner:
        scanner.find_device_by_address(address)

        # Important! Wait for an event to trigger stop, otherwise scanner
        # will stop immediately.
        await stop_event.wait()


if __name__ == "__main__":
    asyncio.run(main())
    # test_data = '10 02 89 a3 02 b2 b3 bb 79 5a 9c 40 4a b9 0f 16 2b 4e 58 9b 30 22 3b'
    # decrypt_data(raw_data=test_data, key=sys.argv[1])

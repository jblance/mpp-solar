import asyncio
# import sys
from bleak import BleakClient


async def main():
    address = 'C2:B0:0C:CC:7D:BC'

    async with BleakClient(address) as client:
        if (not client.is_connected):
            raise Exception("client not connected")
        print(client)

        print('writing to keepalive')
        res = await client.write_gatt_char('6597ffff-4bda-4c1e-af4b-551c4cf74769', 0x30ff)
        print(f"{res=}")

        print('reading soc')
        char = await client.read_gatt_char('65970fff-4bda-4c1e-af4b-551c4cf74769')
        print(f"{char=}")


if __name__ == "__main__":
    asyncio.run(main())

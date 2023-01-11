# JKBMS
# services...
# 0000ffe0-0000-1000-8000-00805f9b34fb (Handle: 8): Vendor specific
# characteristics
# 0000ffe3-0000-1000-8000-00805f9b34fb (Handle: 15): Vendor specific
# ['write-without-response', 'write']
# 0000ffe2-0000-1000-8000-00805f9b34fb (Handle: 12): Vendor specific
# ['write-without-response', 'write', 'notify']
# 0000ffe1-0000-1000-8000-00805f9b34fb (Handle: 9): Vendor specific
# ['write-without-response', 'write', 'notify']
# Connect to the notify service
# serviceNotifyUuid = "ffe0"
# serviceNotify = self._device.getServiceByUUID(serviceNotifyUuid)
# Get the handles that we need to talk to
# Read
# characteristicReadUuid = "ffe3"  #old version
# characteristicReadUuid = "ffe1"
# characteristicRead = serviceNotify.getCharacteristics(characteristicReadUuid)[0]
# handleRead = characteristicRead.getHandle()
# log.info("Read characteristic: {}, handle {:x}".format(characteristicRead, handleRead))

# # Need to dynamically find this handle....
# log.info("Enable 0x0b handle", self._device.writeCharacteristic(0x0B, b"\x01\x00"))      0x0b = 11
# log.info("Enable read handle", self._device.writeCharacteristic(handleRead, b"\x01\x00"),)
# log.info(Write getInfo to read handle", self._device.writeCharacteristic(handleRead, getInfo),)

# jkbms
# 1 service
# 3 characteristics

import asyncio
from bleak import BleakClient

address = "3C:A5:49:DB:5D:C0"
MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"
getInfo = (
    b"\xaa\x55\x90\xeb\x97\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11"
)

count = 0


def callback(sender: int, data: bytearray):
    global count
    count += 1
    print(f"{count} {sender}: {data}")


async def main(address):
    global count
    async with BleakClient(address) as client:
        # model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        # print("Model Number: {0}".format("".join(map(chr, model_number))))
        cl = client.services.get_characteristic("0000ffe1-0000-1000-8000-00805f9b34fb")
        print(cl)
        for c in client.services:
            print("services...")
            print(c)
            print("characteristics")
            for ch in c.characteristics:
                print(ch)
                print(ch.properties)
        # Enable read handle
        t = await client.write_gatt_char(cl, b"\x01\x00")
        # Send command
        t = await client.write_gatt_char(cl, getInfo)
        # Setup callback
        t = await client.start_notify(cl, callback)
        print(t)
        while True:
            await asyncio.sleep(1)
            if count >= 2:
                break
        print(client.is_connected)
        # ch1=client.services.get_characteristic(0x0b)
        # print(ch1)
    print(client.is_connected)


asyncio.run(main(address))

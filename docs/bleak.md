
Install bleak
`$ pip install bleak`


If get a permission error like `bleak.exc.BleakDBusError: [org.freedesktop.DBus.Error.AccessDenied] Rejected send message`
Add user to bluetooth group and restart dbus
```sh
$ usermod -a -G bluetooth

$ sudo systemctl restart dbus
```

Check by running a scan:

```python
import asyncio
from bleak import BleakScanner

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

asyncio.run(main())
```
eg on my test environment
```
3C:A5:49:DB:5D:C0: JK-B2A24S
CC:B6:83:AE:98:A0: SmartShunt HQ2041IA193
```


```python
"""
Service Explorer
----------------
An example showing how to access and print out the services, characteristics and
descriptors of a connected GATT server.
Created on 2019-03-25 by hbldh <henrik.blidh@nedomkull.com>
"""

import sys
import platform
import asyncio
import logging

from bleak import BleakClient

logger = logging.getLogger(__name__)

ADDRESS = (
    "3C:A5:49:DB:5D:C0"

)


async def main(address):
    async with BleakClient(address) as client:
        logger.info(f"Connected: {client.is_connected}")

        for service in client.services:
            logger.info(f"[Service] {service}")
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = bytes(await client.read_gatt_char(char.uuid))
                        logger.info(
                            f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}"
                        )
                    except Exception as e:
                        logger.error(
                            f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {e}"
                        )

                else:
                    value = None
                    logger.info(
                        f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}"
                    )

                for descriptor in char.descriptors:
                    try:
                        value = bytes(
                            await client.read_gatt_descriptor(descriptor.handle)
                        )
                        logger.info(f"\t\t[Descriptor] {descriptor}) | Value: {value}")
                    except Exception as e:
                        logger.error(f"\t\t[Descriptor] {descriptor}) | Value: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main(ADDRESS))
```


3C:A5:49:DB:5D:C0: JK-B2A24S
```
INFO:__main__:Connected: True
INFO:__main__:[Service] 0000ffe0-0000-1000-8000-00805f9b34fb (Handle: 8): Vendor specific
INFO:__main__:    [Characteristic] 0000ffe1-0000-1000-8000-00805f9b34fb (Handle: 9): Vendor specific (write-without-response,write,notify), Value: None
INFO:__main__:        [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 11): Client Characteristic Configuration) | Value: b'\x00\x00'
INFO:__main__:    [Characteristic] 0000ffe2-0000-1000-8000-00805f9b34fb (Handle: 12): Vendor specific (write-without-response,write,notify), Value: None
INFO:__main__:        [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 14): Client Characteristic Configuration) | Value: b'\x00\x00'
INFO:__main__:    [Characteristic] 0000ffe3-0000-1000-8000-00805f9b34fb (Handle: 15): Vendor specific (write-without-response,write), Value: None
INFO:__main__:        [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 17): Client Characteristic Configuration) | Value: b'\x00\x00'
```

get ffe0 service
get characteristics from ffe3 then get its handle (17 or 0x11
Enable 0x0b handle", self._device.writeCharacteristic(11 or 0x0B, b"\x01\x00"))
Enable read handle", self._device.writeCharacteristic(17 or 0x11, b"\x01\x00"))

Write getInfo to read handle", self._device.writeCharacteristic(handleRead, getInfo)

CC:B6:83:AE:98:A0: SmartShunt HQ2041IA193
```
INFO:__main__:Connected: True
INFO:__main__:[Service] 00001801-0000-1000-8000-00805f9b34fb (Handle: 10): Generic Attribute Profile
INFO:__main__:    [Characteristic] 00002a05-0000-1000-8000-00805f9b34fb (Handle: 11): Service Changed (indicate), Value: None
INFO:__main__:        [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 13): Client Characteristic Configuration) | Value: b'\x02\x00'
INFO:__main__:[Service] 68c10001-b17f-4d3a-a290-34ad6499937c (Handle: 14): Unknown
INFO:__main__:    [Characteristic] 68c10002-b17f-4d3a-a290-34ad6499937c (Handle: 15): Unknown (write,notify), Value: None
INFO:__main__:        [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 17): Client Characteristic Configuration) | Value: b'\x00\x00'
INFO:__main__:    [Characteristic] 68c10003-b17f-4d3a-a290-34ad6499937c (Handle: 18): Unknown (write-without-response), Value: None
INFO:__main__:[Service] 97580001-ddf1-48be-b73e-182664615d8e (Handle: 20): Unknown
INFO:__main__:    [Characteristic] 97580002-ddf1-48be-b73e-182664615d8e (Handle: 21): Unknown (read), Value: b'\xff\x12\x01\x00\xff0\x02\x00\x8c\x00\x96\xa1P\x00\xf2\xff\xff\xff\x00'
INFO:__main__:    [Characteristic] 97580003-ddf1-48be-b73e-182664615d8e (Handle: 23): Unknown (write,notify), Value: None
INFO:__main__:        [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 25): Client Characteristic Configuration) | Value: b'\x00\x00'
INFO:__main__:    [Characteristic] 97580004-ddf1-48be-b73e-182664615d8e (Handle: 26): Unknown (write), Value: None
INFO:__main__:    [Characteristic] 97580006-ddf1-48be-b73e-182664615d8e (Handle: 28): Unknown (read,write,notify), Value: b'\xe4\x01\xbe<\x939&\xe2'
INFO:__main__:        [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 30): Client Characteristic Configuration) | Value: b'\x00\x00'
INFO:__main__:[Service] 306b0001-b081-4037-83dc-e59fcc3cdfd0 (Handle: 31): Unknown
INFO:__main__:    [Characteristic] 306b0002-b081-4037-83dc-e59fcc3cdfd0 (Handle: 32): Unknown (read,write-without-response,notify), Value: b''
ERROR:__main__:        [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 34): Client Characteristic Configuration) | Value: Not connected
INFO:__main__:    [Characteristic] 306b0003-b081-4037-83dc-e59fcc3cdfd0 (Handle: 35): Unknown (write-without-response,notify), Value: None
ERROR:__main__:        [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 37): Client Characteristic Configuration) | Value: Not connected
INFO:__main__:    [Characteristic] 306b0004-b081-4037-83dc-e59fcc3cdfd0 (Handle: 38): Unknown (write-without-response,notify), Value: None
ERROR:__main__:        [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 40): Client Characteristic Configuration) | Value: Not connected
```



"""
Notifications
-------------
Example showing how to add notifications to a characteristic and handle the responses.
Updated on 2019-07-03 by hbldh <henrik.blidh@gmail.com>
"""


import asyncio


from bleak import BleakClient


# you can change these to match your device or override them from the command line
CHARACTERISTIC_UUID1 = "0000ffe1-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID2 = "ffe2"
CHARACTERISTIC_UUID3 = "ffe3"
ADDRESS = ("3C:A5:49:DB:5D:C0")


def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    print("{0}: {1}".format(sender, data))


async def main(address):
    async with BleakClient(address) as client:
        char_uuid=CHARACTERISTIC_UUID1
        print(f"Connected: {client.is_connected}")

        await client.start_notify(char_uuid, notification_handler)
        await asyncio.sleep(5.0)
        await client.stop_notify(char_uuid)


if __name__ == "__main__":
    asyncio.run(
        main(ADDRESS
        )
    )





    0000ffe1-0000-1000-8000-00805f9b34fb
    """
UART Service
-------------

An example showing how to write a simple program using the Nordic Semiconductor
(nRF) UART service.

"""

import asyncio
import sys

from bleak import BleakScanner, BleakClient
from bleak.backends.scanner import AdvertisementData
from bleak.backends.device import BLEDevice

UART_SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"
UART_RX_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
UART_TX_CHAR_UUID = "0000ffe3-0000-1000-8000-00805f9b34fb"
ADDRESS = ("3C:A5:49:DB:5D:C0")

# All BLE devices have MTU of at least 23. Subtracting 3 bytes overhead, we can
# safely send 20 bytes at a time to any device supporting this service.
UART_SAFE_SIZE = 20


async def uart_terminal():
    """This is a simple "terminal" program that uses the Nordic Semiconductor
    (nRF) UART service. It reads from stdin and sends each line of data to the
    remote device. Any data received from the device is printed to stdout.
    """

    def match_nus_uuid(device: BLEDevice, adv: AdvertisementData):
        # This assumes that the device includes the UART service UUID in the
        # advertising data. This test may need to be adjusted depending on the
        # actual advertising data supplied by the device.
        if UART_SERVICE_UUID.lower() in adv.service_uuids:
            return True

        return False

    device = await BleakScanner(ADDRESS)

    def handle_disconnect(_: BleakClient):
        print("Device was disconnected, goodbye.")
        # cancelling all tasks effectively ends the program
        for task in asyncio.all_tasks():
            task.cancel()

    def handle_rx(_: int, data: bytearray):
        print("received1:", data)

    def handle_rx2(_: int, data: bytearray):
        print("received2:", data)

    async with BleakClient(device, disconnected_callback=handle_disconnect) as client:
        await client.start_notify(UART_TX_CHAR_UUID, handle_rx)
        await client.start_notify(UART_RX_CHAR_UUID, handle_rx2)

        print("Connected...")

        loop = asyncio.get_running_loop()

        while True:

            # some devices, like devices running MicroPython, expect Windows
            # line endings (uncomment line below if needed)
            # data = data.replace(b"\n", b"\r\n")
            data=b"\xaa\x55\x90\xeb\x97\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11"

            await client.write_gatt_char(UART_TX_CHAR_UUID, data)
            print("sent:", data)
            asyncio.sleep(30)


if __name__ == "__main__":
    try:
        asyncio.run(uart_terminal())
    except asyncio.CancelledError:
        # task is cancelled on disconnect, so we ignore this error
        pass
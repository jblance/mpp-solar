from bluepy import btle
import logging


from .baseio import BaseIO
from .jkbledelegate import jkBleDelegate

log = logging.getLogger("MPP-Solar")

getInfo = b"\xaa\x55\x90\xeb\x97\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11"


class JkBleIO(BaseIO):
    def __init__(self, device_path) -> None:
        self._device = None
        self._device_path = device_path
        self.maxConnectionAttempts = 3
        self.record = None
        self._test_data = bytes.fromhex(
            "55aaeb9002ff5b566240e34e62406e6a62404a506240acd7624011d26240bddd62409ad1624044c86240cedc6240ccc7624079e1624057dc624073a262405f80624088c46240000000000000000000000000000000000000000000000000000000000000000013315c3d0636143d26e0113d8021f03c1153363d8980123d7e7c033dac41233d1ad83c3d9d6f4f3d8eb51e3d6a2c293deb28653d189c523da3724e3deb94493d9ab2c23d00000000000000000000000000000000000000000000000000000000000000001aad62400084053c00000000ffff00000b000000000000000000000000000036a3554c40000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000be0b54001456a43fb876a43f00a2"
        )

    def send_and_receive(self, command, show_raw=False, protocol=None) -> dict:
        full_command = protocol.get_full_command(command)
        log.info(f"full command {full_command} for command {command}")
        # Send the full command via the communications port
        command_defn = protocol.get_command_defn(command)
        record_type = command_defn["record_type"]
        log.debug(f"expected record type {record_type} for command {command}")

        # Need to get response here
        # response = self._test_data

        # Connect to BLE device
        if self.ble_connect(self._device_path, protocol):
            response = self.ble_get_data(full_command, record_type)
            self.ble_disconnect()
        else:
            print(f"Failed to connect to {self._device_path}")
            response = None
        # End of BLE device connection
        log.debug(f"Raw response {response}")
        decoded_response = protocol.decode(response, show_raw, command)
        log.debug(f"Decoded response {decoded_response}")
        log.info(f"Decoded response {decoded_response}")
        return decoded_response

    def ble_connect(self, mac=None, protocol=None):
        """
        Connect to a BLE device with 'mac' address
        """
        self._device = None
        # Intialise BLE device
        self._device = btle.Peripheral(None)
        self._device.withDelegate(jkBleDelegate(self, protocol, record_type))
        # Connect to BLE Device
        connected = False
        attempts = 0
        log.info(f"Attempting to connect to {mac}")
        while not connected:
            attempts += 1
            if attempts > self.maxConnectionAttempts:
                log.warning(f"Cannot connect to mac {mac} - exceeded {attempts - 1} attempts")
                return connected
            try:
                self._device.connect(mac)
                connected = True
            except Exception:
                continue
        return connected

    def ble_disconnect(self):
        log.info("Disconnecting BLE Device...")
        self._device.disconnect()
        self._device = None
        return

    def ble_get_data(self, command=None):
        self.record = None

        if command is None:
            return self.record

        # Get the device name
        serviceId = self._device.getServiceByUUID(btle.AssignedNumbers.genericAccess)
        deviceName = serviceId.getCharacteristics(btle.AssignedNumbers.deviceName)[0]
        log.info("Connected to {}".format(deviceName.read()))

        # Connect to the notify service
        serviceNotifyUuid = "ffe0"
        serviceNotify = self._device.getServiceByUUID(serviceNotifyUuid)

        # Get the handles that we need to talk to
        # Read
        characteristicReadUuid = "ffe3"
        characteristicRead = serviceNotify.getCharacteristics(characteristicReadUuid)[0]
        handleRead = characteristicRead.getHandle()
        log.info("Read characteristic: {}, handle {:x}".format(characteristicRead, handleRead))

        # ## TODO sort below
        # Need to dynamically find this handle....
        log.info("Enable 0x0b handle", self._device.writeCharacteristic(0x0B, b"\x01\x00"))
        log.info("Enable read handle", self._device.writeCharacteristic(handleRead, b"\x01\x00"))
        log.info(
            "Write getInfo to read handle", self._device.writeCharacteristic(handleRead, getInfo)
        )
        secs = 0
        while True:
            if self._device.waitForNotifications(1.0):
                continue
            secs += 1
            if secs > 5:
                break

        log.info(
            "Write command to read handle",
            self._device.writeCharacteristic(handleRead, command),
        )
        loops = 0
        recordsToGrab = 1
        log.info("Grabbing {} records (after inital response)".format(recordsToGrab))

        while True:
            loops += 1
            if loops > recordsToGrab * 15 + 16:
                print("Got {} records".format(recordsToGrab))
                break
            if self._device.waitForNotifications(1.0):
                continue

        log.debug(f"Record now {self.record} len {len(self.record)}")
        # response = self._test_data
        return self.record[-300:]

""" mppsolar / inout / jkbleio.py """
import logging

try:
    from bluepy import btle
except ImportError:
    print("You are missing dependencies in order to be able to use that output.")
    print("To install them, use that command:")
    print("    python -m pip install 'mppsolar[ble]'")

from .baseio import BaseIO
from ..helpers import get_kwargs
from .jkbledelegate import jkBleDelegate

log = logging.getLogger("JkBleIO")

getInfo = (
    b"\xaa\x55\x90\xeb\x97\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11"
)
# getInfo = b"\xaa\x55\x90\xeb\x97\x00\xdf\x52\x88\x67\x9d\x0a\x09\x6b\x9a\xf6\x70\x9a\x17\xfd"


class JkBleIO(BaseIO):
    def __init__(self, device_path) -> None:
        self._device = None
        self._device_path = device_path
        self.maxConnectionAttempts = 3
        self.record = None

    def send_and_receive(self, *args, **kwargs) -> dict:
        # Send the full command via the communications port
        command = get_kwargs(kwargs, "command")
        protocol = get_kwargs(kwargs, "protocol")
        full_command = protocol.get_full_command(command)
        log.info(f"full command {full_command} for command {command}")

        command_defn = protocol.get_command_defn(command)
        record_type = command_defn["record_type"]
        log.debug(f"expected record type {record_type} for command {command}")

        # Connect to BLE device
        if self.ble_connect(self._device_path, protocol, record_type):
            response = self.ble_get_data(full_command)
            self.ble_disconnect()
        else:
            log.error(f"Failed to connect to {self._device_path}")
            response = None
        # End of BLE device connection
        log.debug(f"Raw response {response}")
        return response

    def ble_connect(self, mac=None, protocol=None, record_type=0x02):
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
                log.warning(
                    f"Cannot connect to mac {mac} - exceeded {attempts - 1} attempts"
                )
                return connected
            try:
                self._device.connect(mac)
                self._device.setMTU(330)
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

        log.debug(f"Command: {command}")

        if command is None:
            return self.record

        # Get the device name
        try:
            serviceId = self._device.getServiceByUUID(btle.AssignedNumbers.genericAccess)
            deviceName = serviceId.getCharacteristics(btle.AssignedNumbers.deviceName)[0]
            log.info("Connected to {}".format(deviceName.read()))
        except btle.BTLEGattError as e:
            log.warning(f"Error getting device name: {e}")

        # Connect to the notify service
        serviceNotifyUuid = "ffe0"
        serviceNotify = self._device.getServiceByUUID(serviceNotifyUuid)

        # Get the handles that we need to talk to
        # Read
        # characteristicReadUuid = "ffe3"  #old version
        characteristicReadUuid = (
            "ffe1"  # TODO: need to validate this works for older bms
        )
        characteristicRead = serviceNotify.getCharacteristics(characteristicReadUuid)[0]
        handleRead = characteristicRead.getHandle()
        log.info(
            "Read characteristic: {}, handle {:x}".format(
                characteristicRead, handleRead
            )
        )

        # ## TODO sort below
        # Need to dynamically find this handle....
        log.info(
            "Enable 0x0b handle %s", self._device.writeCharacteristic(0x0B, b"\x01\x00")
        )
        log.info(
            "Enable read handle %s",
            self._device.writeCharacteristic(handleRead, b"\x01\x00")
        )
        log.info(
            "Write getInfo to read handle %s",
            self._device.writeCharacteristic(handleRead, getInfo)
        )
        secs = 0
        while True:
            if self._device.waitForNotifications(1.0):
                continue
            secs += 1
            if secs > 5:
                break

        if command == "getInfo":
            return self.record[:300]

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
                log.info("jkbleio: ble_get_dataa: Got {} records".format(recordsToGrab))
                break
            if self._device.waitForNotifications(1.0):
                continue

        log.debug(f"Record now {self.record} len {len(self.record)}")
        return self.record[:300]

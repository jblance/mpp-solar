from powermon.ports import getPortFromConfig
from mppsolar.protocols import get_protocol
# A device is a port with a protocol
# also contains the name, model and id of the device
class Device:
    def __init__(self, name, id, model, manufacturer, port, protocol):
        self.name = name
        self.id = id
        self.model = model
        self.manufacturer = manufacturer
        self.port = port
        self.protocol = protocol

    @classmethod
    def fromConfig(cls, config):
        name = config.get("name", "mppsolar")
        id = config.get("id", "mppsolar")
        model = config.get("model", "mppsolar")
        manufacturer = config.get("manufacturer", "mppsolar")
        portConfig = config.get("port", None)
        port = getPortFromConfig(portConfig)
        protocol = get_protocol(portConfig.get("protocol", None))
        return cls(name, id, model, manufacturer, port, protocol)

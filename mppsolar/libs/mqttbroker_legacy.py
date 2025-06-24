import logging
from typing import Optional, Dict, Any, List
from .mqtt_manager import mqtt_manager, BrokerConfig, DeviceConfig

log = logging.getLogger("mqttbroker_legacy")


class MqttBroker:
    """Legacy wrapper for the new threaded MQTT manager"""

    def __str__(self):
        if self.enabled:
            return f"MqttBroker name: {self.name}, port: {self.port}, user: {self.username}"
        else:
            return "MqttBroker DISABLED"

    def __init__(self, config=None):
        self.config = config or {}
        log.debug(f"mqttbroker config: {config}")

        self.name = self.config.get("name")

        try:
            _port = self.config.get("port", 1883)
            self.port = int(_port)
        except ValueError:
            log.info(f"Unable to process port: '{_port}', defaulting to 1883")
            self.port = 1883

        self.username = self.config.get("user")
        self.password = self.config.get("pass")
        self.results_topic = None

        # Legacy compatibility
        self._isConnected = False
        self.enabled = self.name is not None

        # Internal tracking
        self._device_name = None
        self._connection = None

    def set(self, variable, value):
        """Set attribute value"""
        setattr(self, variable, value)

    def update(self, variable, value):
        """Update attribute only if value is not None"""
        if value is None:
            return
        setattr(self, variable, value)

    def connect(self):
        """Legacy connect method - now handled automatically by manager"""
        if not self.enabled:
            log.info(f"MQTT broker not enabled, was a broker name defined? '{self.name}'")
            return

        log.debug(f"Legacy connect called for {self.name}:{self.port}")
        # Connection is now managed automatically by the manager

    def start(self):
        """Legacy start method"""
        pass  # Handled by manager

    def stop(self):
        """Legacy stop method"""
        pass  # Handled by manager

    def subscribe(self, topic, callback):
        """Legacy subscribe method - not implemented in threaded version"""
        log.warning("Legacy subscribe method called - use command callbacks instead")

    def _ensure_connection(self, device_name: str = None, allowed_commands: List[str] = None,
                          command_callback = None) -> bool:
        """Ensure we have a connection set up for this broker/device combo"""
        if not self.enabled:
            return False

        if device_name is None:
            device_name = getattr(self, '_device_name', 'default')

        # Check if we already have a connection for this device
        connection = mqtt_manager.get_connection_for_device(device_name)
        if connection:
            self._connection = connection
            return True

        # Create broker and device config
        broker_config = BrokerConfig(
            name=self.name,
            port=self.port,
            username=self.username,
            password=self.password
        )

        device_config = DeviceConfig(
            device_name=device_name,
            section_name=device_name,
            broker_config=broker_config,
            results_topic=self.results_topic,
            allowed_commands=allowed_commands or [],
            command_callback=command_callback
        )

        # Add to manager
        self._connection = mqtt_manager.add_device(device_config)
        self._device_name = device_name
        return True

    def publish(self, topic: str, payload: str, qos: int = 0, retain: bool = False,
                device_name: str = None):
        """Publish a single message"""
        if self.name == "screen":
            print(f"mqtt debug output only as broker name is 'screen' - topic: '{topic}', payload: '{payload}'")
            return

        if not self._ensure_connection(device_name):
            log.warning("Cannot publish - no connection available")
            return

        self._connection.publish(topic, payload, qos, retain)

    def publishMultiple(self, data: List[Dict[str, Any]], device_name: str = None):
        """Publish multiple messages"""
        if self.name == "screen":
            for msg in data:
                print(f"mqtt debug output only as broker name is 'screen' - topic: '{msg['topic']}', payload: '{msg['payload']}'")
            return

        if not self._ensure_connection(device_name):
            log.warning("Cannot publish multiple - no connection available")
            return

        self._connection.publish_multiple(data)

    def setup_device_commands(self, device_name: str, allowed_commands: List[str],
                            command_callback = None):
        """Set up command handling for a specific device"""
        self._ensure_connection(device_name, allowed_commands, command_callback)


# Legacy compatibility - maintain the old interface
class MqttBrokerC(MqttBroker):
    """Alias for backwards compatibility"""
    pass

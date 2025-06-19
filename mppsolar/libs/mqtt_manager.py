import logging
import threading
import hashlib
import time
import re
import socket
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from queue import Queue, Empty
import json

import paho.mqtt.client as mqtt_client

log = logging.getLogger("mqtt_manager")


@dataclass
class BrokerConfig:
    """Configuration for a single MQTT broker"""
    name: str
    port: int = 1883
    username: Optional[str] = None
    password: Optional[str] = None
    keepalive: int = 60
    clean_session: bool = False

    def __hash__(self):
        return hash((self.name, self.port, self.username))


@dataclass
class DeviceConfig:
    """Configuration for a device section"""
    device_name: str
    section_name: str
    broker_config: BrokerConfig
    results_topic: Optional[str] = None
    allowed_commands: List[str] = field(default_factory=list)
    command_callback: Optional[Callable] = None

    def __post_init__(self):
        # Compile regex patterns for allowed commands
        self.allowed_cmd_patterns = []
        for cmd in self.allowed_commands:
            try:
                self.allowed_cmd_patterns.append(re.compile(cmd))
            except re.error as e:
                log.warning(f"Invalid regex pattern '{cmd}': {e}")


class MqttConnection:
    """Manages a single MQTT broker connection with threading support"""

    def __init__(self, broker_config: BrokerConfig):
        self.config = broker_config
#         self.client = mqtt_client.Client(clean_session=broker_config.clean_session)
        client_id = self._generate_client_id()
        self.client = mqtt_client.Client(
            client_id=client_id,
            clean_session=broker_config.clean_session
        )
        self.connected = False
        self.reconnect_delay = 5
        self.max_reconnect_delay = 300
        self.current_reconnect_delay = self.reconnect_delay
        self.should_stop = threading.Event()
        self.connection_thread = None
        self.publish_queue = Queue()
        self.publish_thread = None
        self.devices = {}  # device_name -> DeviceConfig

        # Setup client callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        self.client.on_publish = self._on_publish

        # Setup authentication if provided
        if broker_config.username:
            self.client.username_pw_set(broker_config.username, broker_config.password)

    def _generate_client_id(self) -> str:
        """Generate a consistent client ID based on broker config and hostname"""
        hostname = self._get_hostname()

        # Create a string that uniquely identifies this connection
        connection_string = f"{hostname}:{self.config.name}:{self.config.port}"
        if self.config.username:
            connection_string += f":{self.config.username}"

        # Generate a hash for consistency
        hash_obj = hashlib.md5(connection_string.encode('utf-8'))
        hash_hex = hash_obj.hexdigest()[:8]  # Use first 8 chars for brevity

        # Create client ID with hostname prefix for readability
        client_id = f"mppsolar_{hostname}_{hash_hex}"

        log.debug(f"Generated client ID: {client_id} for connection: {connection_string}")
        return client_id


    def _get_hostname(self) -> str:
        """Get short hostname for topic structure"""
        try:
            return socket.gethostname().split('.')[0]
        except:
            return "mppsolar"

    def add_device(self, device_config: DeviceConfig):
        """Add a device configuration to this connection"""
        self.devices[device_config.device_name] = device_config
        if self.connected and device_config.allowed_commands:
            self._subscribe_to_commands(device_config)

    def _subscribe_to_commands(self, device_config: DeviceConfig):
        """Subscribe to command topics for a device"""
        if not device_config.allowed_commands:
            return

        hostname = self._get_hostname()
        cmd_topic = f"{hostname}/{device_config.device_name}/cmd"
        log.info(f"Subscribing to command topic: {cmd_topic}")
        self.client.subscribe(cmd_topic, qos=1)

    def _on_connect(self, client, userdata, flags, rc):
        """Callback for when client connects to broker"""
        connection_results = {
            0: "Connection successful",
            1: "Connection refused - incorrect protocol version",
            2: "Connection refused - invalid client identifier",
            3: "Connection refused - server unavailable",
            4: "Connection refused - bad username or password",
            5: "Connection refused - not authorised"
        }

        result_msg = connection_results.get(rc, f"Unknown result code: {rc}")
        log.info(f"MQTT connection to {self.config.name}:{self.config.port} - {result_msg}")

        if rc == 0:
            self.connected = True
            self.current_reconnect_delay = self.reconnect_delay

            # Subscribe to command topics for all devices
            for device_config in self.devices.values():
                self._subscribe_to_commands(device_config)
        else:
            self.connected = False

    def _on_disconnect(self, client, userdata, rc):
        """Callback for when client disconnects from broker"""
        self.connected = False
        if rc != 0:
            log.warning(f"Unexpected MQTT disconnection from {self.config.name}. RC: {rc}")

    def _on_message(self, client, userdata, msg):
        """Handle incoming MQTT messages"""
        try:
            topic_parts = msg.topic.split('/')
            if len(topic_parts) >= 3 and topic_parts[-1] == 'cmd':
                hostname = topic_parts[0]
                device_name = topic_parts[1]

                # Find matching device
                device_config = self.devices.get(device_name)
                if not device_config:
                    log.warning(f"Received command for unknown device: {device_name}")
                    return

                command = msg.payload.decode('utf-8').strip()
                log.info(f"Received command '{command}' for device '{device_name}'")

                # Check if command is allowed
                if not self._is_command_allowed(command, device_config):
                    log.warning(f"Command '{command}' not allowed for device '{device_name}'")
                    error_response = {
                        "error": "Command not allowed",
                        "command": command,
                        "timestamp": time.time()
                    }
                    self._send_command_response(hostname, device_name, error_response)
                    return

                # Execute command if callback is available
                if device_config.command_callback:
                    try:
                        result = device_config.command_callback(device_name, command)
                        self._send_command_response(hostname, device_name, result)
                    except Exception as e:
                        log.error(f"Error executing command '{command}': {e}")
                        error_response = {
                            "error": str(e),
                            "command": command,
                            "timestamp": time.time()
                        }
                        self._send_command_response(hostname, device_name, error_response)
        except Exception as e:
            log.error(f"Error processing message: {e}")

    def _is_command_allowed(self, command: str, device_config: DeviceConfig) -> bool:
        """Check if command matches any allowed patterns"""
        if not device_config.allowed_cmd_patterns:
            return False

        for pattern in device_config.allowed_cmd_patterns:
            if pattern.match(command):
                return True
        return False

    def _send_command_response(self, hostname: str, device_name: str, response: Any):
        """Send command response to the response topic"""
        response_topic = f"{hostname}/{device_name}/cmd_response"

        if isinstance(response, dict):
            payload = json.dumps(response)
        else:
            payload = str(response)
        log.debug(f"Sending command response with QoS=1, retain=True to topic: {response_topic}")
        self.publish(response_topic, payload, qos=1, retain=True)

    def _on_publish(self, client, userdata, mid):
        """Callback for when message is published"""
        log.debug(f"Message {mid} published successfully")

    def start(self):
        """Start the connection and background threads"""
        if self.connection_thread and self.connection_thread.is_alive():
            return

        self.should_stop.clear()
        self.connection_thread = threading.Thread(target=self._connection_loop, daemon=True)
        self.connection_thread.start()
        self.publish_thread = threading.Thread(target=self._publish_loop, daemon=True)
        self.publish_thread.start()
        log.info(f"Started MQTT connection manager for {self.config.name}:{self.config.port}")

    def stop(self):
        """Stop the connection and all background threads"""
        log.info(f"Stopping MQTT connection to {self.config.name}:{self.config.port}")
        self.should_stop.set()

        if self.connected:
            self.client.disconnect()

        if self.connection_thread and self.connection_thread.is_alive():
            self.connection_thread.join(timeout=5)

        if self.publish_thread and self.publish_thread.is_alive():
            self.publish_thread.join(timeout=5)

    def _connection_loop(self):
        """Main connection management loop"""
        while not self.should_stop.is_set():
            if not self.connected:
                try:
                    log.info(f"Attempting to connect to {self.config.name}:{self.config.port}")
                    self.client.connect(self.config.name, self.config.port, self.config.keepalive)
                    self.client.loop_start()

                    # Wait for connection or timeout
                    start_time = time.time()
                    while not self.connected and (time.time() - start_time) < 10:
                        if self.should_stop.is_set():
                            return
                        time.sleep(0.1)

                    if not self.connected:
                        log.warning(f"Connection timeout to {self.config.name}:{self.config.port}")
                        self._handle_connection_failure()

                except Exception as e:
                    log.error(f"Connection error to {self.config.name}:{self.config.port}: {e}")
                    self._handle_connection_failure()
            else:
                # Keep connection alive
                time.sleep(1)

    def _handle_connection_failure(self):
        """Handle connection failure with exponential backoff"""
        log.warning(f"Waiting {self.current_reconnect_delay}s before reconnecting to {self.config.name}")
        time.sleep(self.current_reconnect_delay)

        self.current_reconnect_delay = min(self.current_reconnect_delay * 2, self.max_reconnect_delay)

    def _publish_loop(self):
        """Background thread for publishing queued messages"""
        while not self.should_stop.is_set():
            try:
                # Get message from queue with timeout
                msg_data = self.publish_queue.get(timeout=1)

                if self.connected:
                    topic = msg_data['topic']
                    payload = msg_data['payload']
                    # FIXED: Use direct dictionary access instead of .get() with defaults
                    # This preserves the QoS and retain values that were explicitly set
                    qos = msg_data['qos']
                    retain = msg_data['retain']

                    log.debug(f"Publishing to {topic} with QoS={qos}, retain={retain}")
                    result = self.client.publish(topic, payload, qos=qos, retain=retain)
                    if result.rc != mqtt_client.MQTT_ERR_SUCCESS:
                        log.warning(f"Failed to publish to {topic}: {result.rc}")
                    else:
                        if isinstance(payload, (bytes, str)):
                            preview = payload[:100]
                        else:
                            preview = str(payload)[:100]
                        log.debug(f"Published to {topic}: {preview}… (QoS={qos}, retain={retain})")
                else:
                    log.warning(f"Cannot publish to {msg_data['topic']} - not connected")

            except Empty:
                continue
            except KeyError as e:
                log.error(f"Missing required key in message data: {e}")
            except Exception as e:
                log.error(f"Error in publish loop: {e}")

    def publish(self, topic: str, payload: str, qos: int = 0, retain: bool = False):
        """Queue a message for publishing"""
        msg_data = {
            'topic': topic,
            'payload': payload,
            'qos': qos,
            'retain': retain
        }
        log.debug(f"Queuing message for {topic} with QoS={qos}, retain={retain}")
        self.publish_queue.put(msg_data)

    def publish_multiple(self, messages: List[Dict[str, Any]]):
        """Queue multiple messages for publishing"""
        for msg in messages:
            topic = msg['topic']
            payload = msg['payload']
            qos = msg.get('qos', 0)
            retain = msg.get('retain', False)
            self.publish(topic, payload, qos, retain)


class MqttManager:
    """Central manager for all MQTT connections and devices"""

    def __init__(self):
        self.connections: Dict[str, MqttConnection] = {}
        self.device_to_connection: Dict[str, MqttConnection] = {}
        self.running = False

    def _get_broker_key(self, broker_config: BrokerConfig) -> str:
        """Generate unique key for broker configuration"""
        return f"{broker_config.name}:{broker_config.port}:{broker_config.username or 'anonymous'}"

    def add_device(self, device_config: DeviceConfig) -> MqttConnection:
        """Add a device and return the associated connection"""
        broker_key = self._get_broker_key(device_config.broker_config)

        # Create connection if it doesn't exist
        if broker_key not in self.connections:
            connection = MqttConnection(device_config.broker_config)
            self.connections[broker_key] = connection
            if self.running:
                connection.start()

        connection = self.connections[broker_key]
        connection.add_device(device_config)
        self.device_to_connection[device_config.device_name] = connection

        return connection

    def get_connection_for_device(self, device_name: str) -> Optional[MqttConnection]:
        """Get the MQTT connection for a specific device"""
        return self.device_to_connection.get(device_name)

    def start_all(self):
        """Start all MQTT connections"""
        self.running = True
        for connection in self.connections.values():
            connection.start()
        log.info(f"Started {len(self.connections)} MQTT connections")

    def stop_all(self):
        """Stop all MQTT connections"""
        self.running = False
        for connection in self.connections.values():
            connection.stop()
        log.info("Stopped all MQTT connections")

    def publish_to_device(self, device_name: str, topic: str, payload: str, qos: int = 0, retain: bool = False):
        """Publish message using the connection for a specific device"""
        connection = self.get_connection_for_device(device_name)
        if connection:
            connection.publish(topic, payload, qos, retain)
        else:
            log.warning(f"No MQTT connection found for device: {device_name}")

    def publish_multiple_to_device(self, device_name: str, messages: List[Dict[str, Any]]):
        """Publish multiple messages using the connection for a specific device"""
        connection = self.get_connection_for_device(device_name)
        if connection:
            connection.publish_multiple(messages)
        else:
            log.warning(f"No MQTT connection found for device: {device_name}")


# Global instance
mqtt_manager = MqttManager()

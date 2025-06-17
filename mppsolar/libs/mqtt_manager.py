import logging
import socket
import threading
import time
import re
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from queue import Queue, Empty
import paho.mqtt.client as mqtt_client

log = logging.getLogger("mqtt_manager")


@dataclass
class BrokerConfig:
    """Configuration for a single MQTT broker"""
    name: str
    port: int = 1883
    username: Optional[str] = None
    password: Optional[str] = None
    enabled: bool = True
    
    def __post_init__(self):
        if not self.name or self.name.lower() in ['none', 'null', '']:
            self.enabled = False


@dataclass
class SectionConfig:
    """Configuration for a device section"""
    section_name: str
    broker_config: BrokerConfig
    device_name: str
    mqtt_allowed_cmds: List[str] = field(default_factory=list)
    command_callback: Optional[Callable] = None
    
    def is_command_allowed(self, command: str) -> bool:
        """Check if a command is allowed based on regex patterns"""
        if not self.mqtt_allowed_cmds:
            return False
        
        for pattern in self.mqtt_allowed_cmds:
            try:
                if re.match(pattern, command):
                    return True
            except re.error as e:
                log.warning(f"Invalid regex pattern '{pattern}': {e}")
        return False


class MqttConnection:
    """Manages a single MQTT broker connection"""
    
    def __init__(self, broker_config: BrokerConfig):
        self.broker_config = broker_config
        self.client = None
        self.connected = False
        self.reconnect_thread = None
        self.shutdown_requested = False
        self.hostname = socket.gethostname().split('.')[0]  # Short hostname
        self.subscriptions = {}  # topic -> callback mapping
        self.lock = threading.Lock()
        
        # Connection parameters
        self.keepalive = 60
        self.connect_timeout = 30
        self.reconnect_delay = 5
        self.max_reconnect_delay = 300
        self.current_reconnect_delay = self.reconnect_delay
        
        self._setup_client()
    
    def _setup_client(self):
        """Initialize the MQTT client"""
        if not self.broker_config.enabled:
            log.info(f"MQTT broker '{self.broker_config.name}' is disabled")
            return
            
        self.client = mqtt_client.Client(clean_session=False)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        
        if self.broker_config.username:
            password_display = "********" if self.broker_config.password else "None"
            log.info(f"Using MQTT authentication for {self.broker_config.name}, "
                    f"username: {self.broker_config.username}, password: {password_display}")
            self.client.username_pw_set(self.broker_config.username, self.broker_config.password)
    
    def _on_connect(self, client, userdata, flags, rc):
        """Handle connection events"""
        connection_results = {
            0: "Connection successful",
            1: "Connection refused - incorrect protocol version",
            2: "Connection refused - invalid client identifier", 
            3: "Connection refused - server unavailable",
            4: "Connection refused - bad username or password",
            5: "Connection refused - not authorised"
        }
        
        result_msg = connection_results.get(rc, f"Unknown error code: {rc}")
        log.info(f"MQTT connection to {self.broker_config.name}: {result_msg}")
        
        if rc == 0:
            self.connected = True
            self.current_reconnect_delay = self.reconnect_delay
            # Resubscribe to all topics
            with self.lock:
                for topic in self.subscriptions:
                    log.debug(f"Resubscribing to {topic}")
                    self.client.subscribe(topic, qos=1)
        else:
            self.connected = False
    
    def _on_disconnect(self, client, userdata, rc):
        """Handle disconnection events"""
        log.warning(f"MQTT disconnected from {self.broker_config.name} (code: {rc})")
        self.connected = False
        
        if not self.shutdown_requested and rc != 0:
            # Start reconnection thread if not already running
            if not self.reconnect_thread or not self.reconnect_thread.is_alive():
                self.reconnect_thread = threading.Thread(target=self._reconnect_loop)
                self.reconnect_thread.daemon = True
                self.reconnect_thread.start()
    
    def _on_message(self, client, userdata, msg):
        """Handle incoming messages"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            log.debug(f"Received message on {topic}: {payload}")
            
            # Find matching subscription callback
            with self.lock:
                for subscribed_topic, callback in self.subscriptions.items():
                    if self._topic_matches(subscribed_topic, topic):
                        if callback:
                            try:
                                callback(topic, payload)
                            except Exception as e:
                                log.error(f"Error in message callback for {topic}: {e}")
                        break
        except Exception as e:
            log.error(f"Error processing message: {e}")
    
    def _topic_matches(self, subscription: str, topic: str) -> bool:
        """Check if a topic matches a subscription (supports MQTT wildcards)"""
        # Convert MQTT wildcards to regex
        pattern = subscription.replace('+', '[^/]+').replace('#', '.*')
        pattern = f"^{pattern}$"
        return bool(re.match(pattern, topic))
    
    def _reconnect_loop(self):
        """Continuous reconnection loop"""
        while not self.shutdown_requested and not self.connected:
            try:
                log.info(f"Attempting to reconnect to {self.broker_config.name}...")
                self.client.connect(self.broker_config.name, self.broker_config.port, self.keepalive)
                self.client.loop_start()
                
                # Wait a bit to see if connection succeeds
                time.sleep(2)
                if self.connected:
                    log.info(f"Successfully reconnected to {self.broker_config.name}")
                    break
                    
            except Exception as e:
                log.warning(f"Reconnection failed to {self.broker_config.name}: {e}")
            
            # Exponential backoff
            time.sleep(self.current_reconnect_delay)
            self.current_reconnect_delay = min(self.current_reconnect_delay * 2, self.max_reconnect_delay)
    
    def connect(self) -> bool:
        """Connect to the MQTT broker"""
        if not self.broker_config.enabled:
            return False
            
        if self.broker_config.name == "screen":
            log.info("Screen mode enabled for MQTT debugging")
            return True
            
        try:
            log.info(f"Connecting to MQTT broker {self.broker_config.name}:{self.broker_config.port}")
            self.client.connect(self.broker_config.name, self.broker_config.port, self.keepalive)
            self.client.loop_start()
            
            # Wait for connection
            timeout = time.time() + self.connect_timeout
            while time.time() < timeout and not self.connected:
                time.sleep(0.1)
                
            return self.connected
            
        except Exception as e:
            log.error(f"Failed to connect to {self.broker_config.name}: {e}")
            return False
    
    def subscribe(self, topic: str, callback: Callable = None):
        """Subscribe to a topic"""
        if not self.broker_config.enabled:
            return
            
        with self.lock:
            self.subscriptions[topic] = callback
            
        if self.connected and self.client:
            log.info(f"Subscribing to {topic}")
            self.client.subscribe(topic, qos=1)
        else:
            log.info(f"Queued subscription to {topic} (not connected)")
    
    def publish(self, topic: str, payload: str, retain: bool = False, qos: int = 0) -> bool:
        """Publish a message"""
        if not self.broker_config.enabled:
            return False
            
        if self.broker_config.name == "screen":
            print(f"MQTT DEBUG: topic='{topic}', payload='{payload}', retain={retain}, qos={qos}")
            return True
            
        if not self.connected:
            log.warning(f"Cannot publish to {topic}: not connected to {self.broker_config.name}")
            return False
            
        try:
            log.debug(f"Publishing to {topic}: {payload}")
            info = self.client.publish(topic, payload, qos=qos, retain=retain)
            if qos > 0:
                info.wait_for_publish(timeout=10)
            return True
        except Exception as e:
            log.error(f"Failed to publish to {topic}: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the broker"""
        self.shutdown_requested = True
        if self.client and self.connected:
            log.info(f"Disconnecting from {self.broker_config.name}")
            self.client.loop_stop()
            self.client.disconnect()
        self.connected = False


class MqttManager:
    """Manages multiple MQTT connections and command handling"""
    
    def __init__(self):
        self.connections: Dict[str, MqttConnection] = {}
        self.section_configs: Dict[str, SectionConfig] = {}
        self.default_broker_config: Optional[BrokerConfig] = None
        self.hostname = socket.gethostname().split('.')[0]
        self.shutdown_requested = False
        
    def set_default_broker(self, config: Dict[str, Any]):
        """Set the default broker configuration from SETUP section"""
        name = config.get("name") or config.get("mqtt_broker")
        if name:
            self.default_broker_config = BrokerConfig(
                name=name,
                port=int(config.get("port", config.get("mqtt_port", 1883))),
                username=config.get("user", config.get("mqtt_user")),
                password=config.get("pass", config.get("mqtt_pass"))
            )
            log.info(f"Default MQTT broker set: {self.default_broker_config.name}")
    
    def add_section(self, section_name: str, device_name: str, config: Dict[str, Any], 
                   command_callback: Callable = None):
        """Add a device section configuration"""
        # Determine broker config for this section
        broker_name = config.get("mqtt_broker")
        if broker_name:
            # Section-specific broker
            broker_config = BrokerConfig(
                name=broker_name,
                port=int(config.get("mqtt_port", 1883)),
                username=config.get("mqtt_user"),
                password=config.get("mqtt_pass")
            )
        elif self.default_broker_config:
            # Use default broker
            broker_config = self.default_broker_config
        else:
            log.warning(f"No MQTT broker configured for section {section_name}")
            return
        
        # Parse allowed commands
        allowed_cmds = []
        mqtt_allowed_cmds = config.get("mqtt_allowed_cmds", "")
        if mqtt_allowed_cmds:
            allowed_cmds = [cmd.strip() for cmd in mqtt_allowed_cmds.split(",")]
        
        section_config = SectionConfig(
            section_name=section_name,
            broker_config=broker_config,
            device_name=device_name,
            mqtt_allowed_cmds=allowed_cmds,
            command_callback=command_callback
        )
        
        self.section_configs[section_name] = section_config
        
        # Create or get connection for this broker
        broker_key = f"{broker_config.name}:{broker_config.port}"
        if broker_key not in self.connections:
            self.connections[broker_key] = MqttConnection(broker_config)
        
        # Subscribe to command topic if commands are allowed
        if allowed_cmds and command_callback:
            cmd_topic = f"{self.hostname}/{device_name}/cmd"
            self.connections[broker_key].subscribe(
                cmd_topic, 
                lambda topic, payload: self._handle_command(section_name, topic, payload)
            )
            log.info(f"Subscribed to commands for {device_name} on topic: {cmd_topic}")
    
    def _handle_command(self, section_name: str, topic: str, payload: str):
        """Handle incoming MQTT commands"""
        try:
            section_config = self.section_configs.get(section_name)
            if not section_config:
                log.error(f"Unknown section: {section_name}")
                return
            
            command = payload.strip()
            log.info(f"Received command for {section_name}: {command}")
            
            # Check if command is allowed
            if not section_config.is_command_allowed(command):
                log.warning(f"Command '{command}' not allowed for {section_name}")
                error_response = f"Command '{command}' not allowed"
                self._send_command_response(section_config, error_response, error=True)
                return
            
            # Execute command
            if section_config.command_callback:
                try:
                    result = section_config.command_callback(command)
                    self._send_command_response(section_config, result)
                except Exception as e:
                    log.error(f"Error executing command '{command}': {e}")
                    self._send_command_response(section_config, str(e), error=True)
            else:
                log.error(f"No command callback registered for {section_name}")
                
        except Exception as e:
            log.error(f"Error handling command: {e}")
    
    def _send_command_response(self, section_config: SectionConfig, response: Any, error: bool = False):
        """Send command response back via MQTT"""
        broker_key = f"{section_config.broker_config.name}:{section_config.broker_config.port}"
        connection = self.connections.get(broker_key)
        
        if not connection:
            log.error(f"No connection available for response")
            return
        
        response_topic = f"{self.hostname}/{section_config.device_name}/cmd_response"
        
        # Format response
        if error:
            response_payload = f"ERROR: {response}"
        else:
            response_payload = str(response)
        
        # Send with QoS 1 and retain
        success = connection.publish(response_topic, response_payload, retain=True, qos=1)
        if success:
            log.info(f"Sent response to {response_topic}")
        else:
            log.error(f"Failed to send response to {response_topic}")
    
    def connect_all(self):
        """Connect to all configured brokers"""
        for broker_key, connection in self.connections.items():
            connection.connect()
    
    def publish(self, topic: str, payload: str, retain: bool = False, qos: int = 0, 
               broker_name: str = None) -> bool:
        """Publish to a specific broker or default broker"""
        if broker_name:
            # Find connection by broker name
            connection = None
            for key, conn in self.connections.items():
                if conn.broker_config.name == broker_name:
                    connection = conn
                    break
        else:
            # Use first available connection
            connection = next(iter(self.connections.values())) if self.connections else None
        
        if connection:
            return connection.publish(topic, payload, retain, qos)
        else:
            log.error(f"No connection available for publishing to {broker_name or 'default broker'}")
            return False
    
    def publishMultiple(self, data: List[Dict[str, Any]], broker_name: str = None):
        """Publish multiple messages (legacy compatibility)"""
        if not data or self.shutdown_requested:
            return
            
        for msg in data:
            topic = msg.get("topic")
            payload = msg.get("payload")
            retain = msg.get("retain", False)
            qos = msg.get("qos", 0)
            
            if topic and payload is not None:
                self.publish(topic, payload, retain, qos, broker_name)
            else:
                log.warning(f"Skipping invalid message: {msg}")
    
    def disconnect_all(self):
        """Disconnect from all brokers"""
        self.shutdown_requested = True
        for connection in self.connections.values():
            connection.disconnect()
        self.connections.clear()
        self.section_configs.clear()


# Legacy compatibility - create a global instance
_mqtt_manager = None

def get_mqtt_manager() -> MqttManager:
    """Get the global MQTT manager instance"""
    global _mqtt_manager
    if _mqtt_manager is None:
        _mqtt_manager = MqttManager()
    return _mqtt_manager


# Legacy MqttBroker class for backward compatibility
class MqttBroker:
    """Legacy compatibility wrapper"""
    
    def __init__(self, config=None):
        self.manager = get_mqtt_manager()
        self.config = config or {}
        
        # Extract broker config
        broker_config = {
            "name": self.config.get("name"),
            "port": self.config.get("port", 1883),
            "user": self.config.get("user"),
            "pass": self.config.get("pass")
        }
        
        if broker_config["name"]:
            self.manager.set_default_broker(broker_config)
    
    def __str__(self):
        if self.config.get("name"):
            return f"MqttBroker name: {self.config.get('name')}, port: {self.config.get('port', 1883)}"
        else:
            return "MqttBroker DISABLED"
    
    def set(self, variable, value):
        """Legacy compatibility"""
        self.config[variable] = value
    
    def update(self, variable, value):
        """Legacy compatibility"""
        if value is not None:
            self.config[variable] = value
    
    def publishMultiple(self, data: List[Dict[str, Any]]):
        """Legacy compatibility"""
        self.manager.publishMultiple(data)
    
    def publish(self, topic: str, payload: str, retain: bool = False):
        """Legacy compatibility"""
        return self.manager.publish(topic, payload, retain)


if __name__ == "__main__":
    # Test the manager
    manager = MqttManager()
    
    # Set default broker
    manager.set_default_broker({
        "name": "localhost",
        "port": 1883,
        "user": None,
        "pass": None
    })
    
    # Add a test section
    def test_command_handler(command):
        return f"Executed: {command}"
    
    manager.add_section(
        "test_inverter",
        "inverter1", 
        {"mqtt_allowed_cmds": "QPIGS,QDI,Q.*"},
        test_command_handler
    )
    
    # Connect and test
    manager.connect_all()
    time.sleep(2)
    
    print("MQTT Manager initialized and ready for testing")

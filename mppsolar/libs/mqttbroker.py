import logging
from dataclasses import dataclass
from typing import Optional

import paho.mqtt.client as mqtt_client

# Set-up logger
log = logging.getLogger("mqttbroker")


@dataclass
class MqttBroker:
    name: str
    port: int = 1883
    username: Optional[str] = None
    password: Optional[str] = None
    results_topic: Optional[str] = None
    mqttc: mqtt_client.Client = mqtt_client.Client()
    _isConnected: bool = False

    # def __init__(self,):
    #     self.mqtt_broker = args.mqttbroker
    #     self.mqtt_port = args.mqttport
    #     # mqtt_topic = args.mqtttopic
    #     # if mqtt_topic is None:
    #     #     mqtt_topic = prog_name
    #     self.mqtt_user = args.mqttuser
    #     self.mqtt_pass = args.mqttpass

    def on_connect(self, client, userdata, flags, rc):
        # 0: Connection successful
        # 1: Connection refused - incorrect protocol version
        # 2: Connection refused - invalid client identifier
        # 3: Connection refused - server unavailable
        # 4: Connection refused - bad username or password
        # 5: Connection refused - not authorised
        # 6-255: Currently unused.
        connection_result = [
            "Connection successful",
            "Connection refused - incorrect protocol version",
            "Connection refused - invalid client identifier",
            "Connection refused - server unavailable",
            "Connection refused - bad username or password",
            "Connection refused - not authorised",
        ]
        log.debug(
            f"MqttBroker connection returned result: {rc} {connection_result[rc]}"
        )
        if rc == 0:
            self._isConnected = True
            return
        self._isConnected = False

    def on_disconnect(self, client, userdata, rc):
        log.error(f"Disconnection returned result: {rc}")
        self._isConnected = False

    def connect(self):

        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_disconnect = self.on_disconnect
        # if a name is supplied, connect
        if self.name:
            self.mqttc.connect(self.name, self.port, keepalive=60)

    def start(self):
        if self._isConnected:
            self.mqttc.loop_start()

    def stop(self):
        if self.name:
            self.mqttc.loop_stop()
            if self._isConnected:
                self.mqttc.disconnect

    def set(self, variable, value):
        setattr(self, variable, value)

    def update(self, variable, value):
        # only override if value is not None
        if value is None:
            return
        setattr(self, variable, value)

    def subscribe(self, topic, callback):
        # subscribe to mqtt topic
        if not self.name:
            return
        # check if connected, connect if not
        if not self._isConnected:
            log.debug("Not connected, connecting")
            self.connect
        # Register callback
        self.mqttc.on_message = callback
        if self._isConnected:
            # Subscribe to command topic
            self.mqttc.subscribe(topic, qos=0)


class MqttBrokerC:
    # name: str
    # port: int = 1883
    # username: Optional[str] = None
    # password: Optional[str] = None
    # results_topic: Optional[str] = None
    # mqttc: mqtt_client.Client = mqtt_client.Client()
    # _isConnected: bool = False
    def __str__(self):
        return (
            f"MqttBrokerC name: {self.name}, port: {self.port}, user: {self.username}"
        )

    def __init__(self, *args, **kwargs):

        # mqttbroker:
        #     name: localhost
        #     port: 1883
        #     user: null
        #     pass: null
        #     adhoc_commands:
        #     topic: test/command_topic

        config = kwargs["config"]
        if config is None:
            config = {}
        self.name = config.get("name")
        self.port = config.get("port", 1883)
        self.username = config.get("user")
        self.password = config.get("pass")
        self.mqttc = mqtt_client.Client()
        self._isConnected = False

    def on_connect(self, client, userdata, flags, rc):
        # 0: Connection successful
        # 1: Connection refused - incorrect protocol version
        # 2: Connection refused - invalid client identifier
        # 3: Connection refused - server unavailable
        # 4: Connection refused - bad username or password
        # 5: Connection refused - not authorised
        # 6-255: Currently unused.
        connection_result = [
            "Connection successful",
            "Connection refused - incorrect protocol version",
            "Connection refused - invalid client identifier",
            "Connection refused - server unavailable",
            "Connection refused - bad username or password",
            "Connection refused - not authorised",
        ]
        log.debug(
            f"MqttBroker connection returned result: {rc} {connection_result[rc]}"
        )
        if rc == 0:
            self._isConnected = True
            return
        self._isConnected = False

    def on_disconnect(self, client, userdata, rc):
        print(f"Disconnection returned result: {rc}")
        self._isConnected = False

    def connect(self):
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_disconnect = self.on_disconnect
        # if a name is supplied, connect
        if self.name:
            log.debug(f"Connecting to {self.name} on port {self.port}")
            try:
                self.mqttc.connect(self.name, self.port, keepalive=60)
            except ConnectionRefusedError as exc:
                log.warn(f"{self.name} refused connection '{exc}'")
        else:
            log.debug(f"Did not connect as no broker name '{self.name}'")

    def start(self):
        if self._isConnected:
            self.mqttc.loop_start()

    def stop(self):
        if self.name:
            self.mqttc.loop_stop()
            if self._isConnected:
                self.mqttc.disconnect

    def set(self, variable, value):
        setattr(self, variable, value)

    def update(self, variable, value):
        # only override if value is not None
        if value is None:
            return
        setattr(self, variable, value)

    def subscribe(self, topic, callback):
        # subscribe to mqtt topic
        if not self.name:
            return
        # check if connected, connect if not
        if not self._isConnected:
            log.debug("Not connected, connecting")
            self.connect()
        # Register callback
        self.mqttc.on_message = callback
        if self._isConnected:
            # Subscribe to command topic
            log.debug(f"Subscribing to topic {topic}")
            self.mqttc.subscribe(topic, qos=0)
        else:
            log.warn(f"Did not subscribe to topic {topic} as not connected to broker")

    def setAdhocCommands(self, adhoc_commands={}, callback=None):
        # sub to command topic if defined
        adhoc_commands_topic = adhoc_commands.get("topic")
        if adhoc_commands_topic is not None:
            log.info(f"Setting adhoc commands topic to {adhoc_commands_topic}")
            self.subscribe(adhoc_commands_topic, callback)


if __name__ == "__main__":
    broker = MqttBroker("brokername")
    print(broker)
    broker.name = "test1"
    print(broker)

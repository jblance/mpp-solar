import logging
from dataclasses import dataclass
from typing import Optional

import paho.mqtt.client as mqtt_client

# Set-up logger
log = logging.getLogger("")


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

    # 0: Connection successful
    # 1: Connection refused - incorrect protocol version
    # 2: Connection refused - invalid client identifier
    # 3: Connection refused - server unavailable
    # 4: Connection refused - bad username or password
    # 5: Connection refused - not authorised
    # 6-255: Currently unused.
    def on_connect(self, client, userdata, flags, rc):
        log.debug(f"MqttBroker connection returned result: {rc}")
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


if __name__ == "__main__":
    broker = MqttBroker("brokername")
    print(broker)
    broker.name = "test1"
    print(broker)

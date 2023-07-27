import logging
from time import sleep

import paho.mqtt.client as mqtt_client

# Set-up logger
log = logging.getLogger("mqttbroker")


class MqttBroker:
    def __str__(self):
        if self.disabled:
            return "MqttBroker DISABLED"
        else:
            return f"MqttBroker name: {self.name}, port: {self.port}, user: {self.username}"

    @classmethod
    def fromConfig(cls, config={}):
        log.debug(f"mqttbroker config: {config}")

        if config:
            name = config.get("name")
            port = config.get("port", 1883)
            username = config.get("username")
            password = config.get("password")
        else:
            name = None
            port = None
            username = None
            password = None

        return cls(name=name, port=port, username=username, password=password)

    def __init__(self, name, port=None, username=None, password=None):

        self.name = name
        self.port = port
        self.username = username
        self.password = password
        self._isConnected = False

        if self.name is None:
            self.disabled = True
        else:
            self.disabled = False
            self.mqttc = mqtt_client.Client()

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
        log.debug(f"MqttBroker connection returned result: {rc} {connection_result[rc]}")
        if rc == 0:
            self._isConnected = True
            return
        self._isConnected = False

    def on_disconnect(self, client, userdata, rc):
        print(f"Disconnection returned result: {rc}")
        self._isConnected = False

    def connect(self):
        if self.disabled:
            log.info(f"MQTT broker not enabled, was a broker name defined? '{self.name}'")
            return
        if not self.name:
            log.info(f"MQTT could not connect as no broker name '{self.name}'")
            return
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_disconnect = self.on_disconnect
        # if name is screen just return without connecting
        if self.name == "screen":
            # allows checking of message formats
            return
        try:
            log.debug(f"Connecting to {self.name} on port {self.port}")
            if self.username:
                # auth = {"username": mqtt_user, "password": mqtt_pass}
                _password = "********" if self.password is not None else "None"
                log.info(f"Using mqtt authentication, username: {self.username}, password: {_password}")
                self.mqttc.username_pw_set(self.username, password=self.password)
            else:
                log.debug("No mqtt authentication used")
                # auth = None
            self.mqttc.connect(self.name, port=self.port, keepalive=60)
            self.mqttc.loop_start()
            sleep(1)
        except ConnectionRefusedError as exc:
            log.warn(f"{self.name} refused connection '{exc}'")

    def start(self):
        if self.disabled:
            return
        if self._isConnected:
            self.mqttc.loop_start()

    def stop(self):
        log.debug("Stopping mqttbroker connection")
        if self.disabled:
            return
        if self.name:
            self.mqttc.loop_stop()
            if self._isConnected:
                log.debug("Disconnecting from mqtt broker")
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
        if self.disabled:
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

    def publishMultiple(self, data):
        if self.disabled:
            log.debug("Cannot publish msgs as mqttbroker disabled")
            return
        for msg in data:
            self.publish(msg["topic"], msg["payload"])

    def publish(self, topic, payload):
        if self.disabled:
            log.debug("Cannot publish msg as mqttbroker disabled")
            return
        log.debug(f"Publishing '{payload}' to '{topic}'")
        if self.name == "screen":
            print(f"mqtt debug output only as broker name is 'screen' - topic: '{topic}', payload: '{payload}'")
            return
        # check if connected, connect if not
        if not self._isConnected:
            log.debug("Not connected, connecting")
            self.connect()
            sleep(1)
            if not self._isConnected:
                log.warn("mqtt broker did not connect")
                return
        try:
            infot = self.mqttc.publish(topic, payload)
            infot.wait_for_publish()
        except Exception as e:
            log.warning(str(e))

    def setAdhocCommands(self, config={}, callback=None):
        if not config:
            return
        if self.disabled:
            log.debug("Cannot setAdhocCommands as mqttbroker disabled")
            return

        adhoc_commands = config.get("adhoc_commands")
        # sub to command topic if defined
        adhoc_commands_topic = adhoc_commands.get("topic")
        if adhoc_commands_topic is not None:
            log.info(f"Setting adhoc commands topic to {adhoc_commands_topic}")
            self.subscribe(adhoc_commands_topic, callback)

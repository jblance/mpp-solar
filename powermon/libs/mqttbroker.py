""" powermon / libs / mqttbroker.py """
import logging
from time import sleep

import paho.mqtt.client as mqtt_client

# Set-up logger
log = logging.getLogger("mqttbroker")


class MqttBroker:
    """ Wrapper for mqtt broker connectivity and message proccessing """
    def __str__(self):
        if self.disabled:
            return "MqttBroker DISABLED"
        else:
            return f"MqttBroker name: {self.name}, port: {self.port}, user: {self.username}"

    @classmethod
    def from_config(cls, config=None) -> 'MqttBroker':
        """ build the mqtt broker object from a config dict """
        log.debug("mqttbroker config: %s", config)

        if config:
            name = config.get("name")
            port = config.get("port", 1883)
            username = config.get("username")
            password = config.get("password")
            mqtt_broker = cls(name=name, port=port, username=username, password=password)
            mqtt_broker.adhoc_topic = config.get("adhoc_topic")
            return mqtt_broker
        else:
            return cls(name=None)

    def __init__(self, name, port=None, username=None, password=None):
        self.name = name
        self.port = port
        self.username = username
        self.password = password
        self.is_connected = False

        if self.name is None:
            self.disabled = True
        else:
            self.disabled = False
            self.mqttc = mqtt_client.Client()

    def on_connect(self, client, userdata, flags, rc):
        """ callback for connect """
        # 0: Connection successful
        # 1: Connection refused - incorrect protocol version
        # 2: Connection refused - invalid client identifier
        # 3: Connection refused - server unavailable
        # 4: Connection refused - bad username or password
        # 5: Connection refused - not authorised
        # 6-255: Currently unused.
        log.debug("on_connect called - client: %s, userdata: %s, flags: %s", client, userdata, flags)
        connection_result = [
            "Connection successful",
            "Connection refused - incorrect protocol version",
            "Connection refused - invalid client identifier",
            "Connection refused - server unavailable",
            "Connection refused - bad username or password",
            "Connection refused - not authorised",
        ]
        log.debug("MqttBroker connection returned result: %s %s", rc, connection_result[rc])
        if rc == 0:
            self.is_connected = True
            return
        self.is_connected = False

    def on_disconnect(self, client, userdata, rc):
        """ callback for disconnect """
        log.debug("on_disconnect called - client: %s, userdata: %s, rc: %s", client, userdata, rc)
        self.is_connected = False

    def connect(self):
        """ connect to mqtt broker """
        if self.disabled:
            log.info("MQTT broker not enabled, was a broker name defined? '%s'", self.name)
            return
        if not self.name:
            log.info("MQTT could not connect as no broker name")
            return
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_disconnect = self.on_disconnect
        # if name is screen just return without connecting
        if self.name == "screen":
            # allows checking of message formats
            return
        try:
            log.debug("Connecting to %s on port %s", self.name, self.port)
            if self.username:
                # auth = {"username": mqtt_user, "password": mqtt_pass}
                _password = "********" if self.password is not None else "None"
                log.info("Using mqtt authentication, username: %s, password: %s", self.username, _password)
                self.mqttc.username_pw_set(self.username, password=self.password)
            else:
                log.debug("No mqtt authentication used")
                # auth = None
            self.mqttc.connect(self.name, port=self.port, keepalive=60)
            self.mqttc.loop_start()
            sleep(1)
        except ConnectionRefusedError as ex:
            log.warning("%s refused connection with error: '%s'", self.name, ex)

    def start(self):
        """ start mqtt broker """
        if self.disabled:
            return
        if self.is_connected:
            self.mqttc.loop_start()

    def stop(self):
        """ stop mqtt broker """
        log.debug("Stopping mqttbroker connection")
        if self.disabled:
            return
        self.mqttc.loop_stop()

    # def set(self, variable, value):
    #     setattr(self, variable, value)

    # def update(self, variable, value):
    #     # only override if value is not None
    #     if value is None:
    #         return
    #     setattr(self, variable, value)

    def subscribe(self, topic, callback):
        """ subscribe to a mqtt topic """
        if not self.name:
            return
        if self.disabled:
            return
        # check if connected, connect if not
        if not self.is_connected:
            log.debug("Not connected, connecting")
            self.connect()
        # Register callback
        self.mqttc.on_message = callback
        if self.is_connected:
            # Subscribe to command topic
            log.debug("Subscribing to topic: %s", topic)
            self.mqttc.subscribe(topic, qos=0)
        else:
            log.warning("Did not subscribe to topic: %s as not connected to broker", topic)

    def publish(self, topic: str = None, payload: str = None):
        """ function to publish messages to mqtt broker """
        if self.disabled:
            log.debug("Cannot publish msg as mqttbroker disabled")
            return
        # log.debug("Publishing '%s' to '%s'", payload, topic)
        if self.name == "screen":
            print(f"mqtt debug - topic: '{topic}', payload: '{payload}'")
            return
        # check if connected, connect if not
        if not self.is_connected:
            log.debug("Not connected, connecting")
            self.connect()
            sleep(1)
            if not self.is_connected:
                log.warning("mqtt broker did not connect")
                return
        if isinstance(topic, bytes):
            topic = topic.decode('utf-8')
        if isinstance(payload, bytes):
            payload = payload.decode('utf-8')
        try:
            infot = self.mqttc.publish(topic, payload)
            infot.wait_for_publish(5)
        except Exception as e:
            log.warning(str(e))

    @property
    def adhoc_topic(self) -> str:
        """ return the adhoc command topic """
        return getattr(self, "_adhoc_topic", None)

    @adhoc_topic.setter
    def adhoc_topic(self, value):
        log.debug("setting adhoc topic to: %s", value)
        self._adhoc_topic = value

    # def setAdhocCommands(self, config={}, callback=None):
    #     if not config:
    #         return
    #     if self.disabled:
    #         log.debug("Cannot setAdhocCommands as mqttbroker disabled")
    #         return

    #     adhoc_commands = config.get("adhoc_commands")
    #     # sub to command topic if defined
    #     adhoc_commands_topic = adhoc_commands.get("topic")
    #     if adhoc_commands_topic is not None:
    #         log.info("Setting adhoc commands topic to %s", adhoc_commands_topic)
    #         self.subscribe(adhoc_commands_topic, callback)

import logging
from time import sleep

import paho.mqtt.client as mqtt_client

# Set-up logger
log = logging.getLogger("mqttbroker")


class MqttBroker:
    def __str__(self):
        if self.enabled:
            return f"MqttBroker name: {self.name}, port: {self.port}, user: {self.username}"
        else:
            return "MqttBroker DISABLED"

    def __init__(self, config=None):

        # mqttbroker:
        #     name: localhost
        #     port: 1883
        #     user: null
        #     pass: null
        #     adhoc_commands:
        #     topic: test/command_topic
        self.config = config
        if config is None:
            config = {}
        log.debug(f"mqttbroker config: {config}")
        self.name = config.get("name")
        try:
            _port = config.get("port", 1883)
            self.port = int(_port)
        except ValueError:
            log.info(f"Unable to process port: '{_port}', defaulting to 1883")
            self.port = 1883

        self.username = config.get("user")
        self.password = config.get("pass")
        self._isConnected = False
        if self.name is None:
            self.enabled = False
        else:
            self.mqttc = mqtt_client.Client()
            self.enabled = True
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
        log.debug(f"MqttBroker connection returned result: {rc} {connection_result[rc]}")
        if rc == 0:
            self._isConnected = True
            return
        self._isConnected = False

    def on_disconnect(self, client, userdata, rc):
        print(f"Disconnection returned result: {rc}")
        self._isConnected = False

    def connect(self):
        if not self.enabled:
            log.info(f"MQTT broker not enabled, was a broker name defined? '{self.name}'")
            return
        if not self.name:
            log.info(f"MQTT did not connect as no broker name '{self.name}'")
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
        if self._isConnected:
            self.mqttc.loop_start()

    def stop(self):
        log.debug("Stopping mqttbroker connection")
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
        for msg in data:
            self.publish(msg["topic"], msg["payload"])

    def publish(self, topic, payload):
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



# print("Connecting to "+args.host+" port: "+str(port))
# mqttc.connect(args.host, port, args.keepalive)

# mqttc.loop_start()

# for x in range (0, args.nummsgs):
#     msg_txt = '{"msgnum": "'+str(x)+'"}'
#     print("Publishing: "+msg_txt)
#     infot = mqttc.publish(args.topic, msg_txt, qos=args.qos)
#     infot.wait_for_publish()

#     time.sleep(args.delay)

# mqttc.disconnect()


if __name__ == "__main__":
    broker = MqttBroker("brokername")
    print(broker)
    broker.name = "test1"
    print(broker)

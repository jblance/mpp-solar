import binascii
import json as js
import logging
import time

import paho.mqtt.client as mqttc

from ..helpers import get_kwargs
from .baseio import BaseIO

log = logging.getLogger("MqttIO")


class MqttIO(BaseIO):
    def __init__(self, *args, **kwargs) -> None:
        # self._serial_port = device_path
        # self._serial_baud = serial_baud
        self.mqtt_broker = get_kwargs(kwargs, "mqtt_broker", "localhost")
        self.mqtt_port = self.mqtt_broker.port
        self.mqtt_user = self.mqtt_broker.username
        self.mqtt_pass = self.mqtt_broker.password
        # self.mqtt_port = get_kwargs(kwargs, "mqtt_port", 1883)
        # self.mqtt_user = get_kwargs(kwargs, "mqtt_user")
        # self.mqtt_pass = get_kwargs(kwargs, "mqtt_pass")
        self.client_id = get_kwargs(kwargs, "client_id")
        log.info(
            f"__init__: client_id: {self.client_id}, mqtt_broker: {self.mqtt_broker}, port: {self.mqtt_port}, user: {self.mqtt_user}, pass: {self.mqtt_pass}"
        )
        self._msg = None

    def sub_cb(self, client, userdata, message):
        log.debug(f"Mqttio sub_cb got msg, topic: {message.topic}, payload: {message.payload}")
        self._msg = message

    def send_and_receive(self, *args, **kwargs) -> dict:
        full_command = get_kwargs(kwargs, "full_command")
        command = get_kwargs(kwargs, "command")
        client_id = self.client_id

        wait_time = 5
        # response_line = None
        command_topic = f"{client_id}/command"
        result_topic = f"{client_id}/result"
        # print(self.mqtt_broker)
        # Create mqtt client
        # Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")
        mqtt_client = mqttc.Client()
        # mqtt_client.on_connect = on_connect

        if self.mqtt_user is not None and self.mqtt_pass is not None:
            # auth = {"username": self.mqtt_user, "password": self.mqtt_pass}
            log.info(
                f"Using mqtt authentication, username: {self.mqtt_user}, password: [supplied]"
            )
            mqtt_client.username_pw_set(self.mqtt_user, password=self.mqtt_pass)
        else:
            log.debug("No mqtt authentication used")
            # auth = None

        mqtt_client.connect(self.mqtt_broker, port=self.mqtt_port)

        command_hex = binascii.hexlify(full_command)
        payload = {"command": command, "command_hex": command_hex.decode()}
        payload = js.dumps(payload)

        log.debug(f"Publishing {payload} to topic: {command_topic}")

        mqtt_client.publish(command_topic, payload=payload)

        mqtt_client.on_message = self.sub_cb
        mqtt_client.subscribe(result_topic)
        mqtt_client.loop_start()
        time.sleep(wait_time)
        mqtt_client.loop_stop(force=False)

        if self._msg is None:
            # Didnt get a result
            return {
                "ERROR": [
                    f"Mqtt result message not received on topic {result_topic} after {wait_time}sec",
                    "",
                ]
            }
        else:
            msg_topic = self._msg.topic
            # decode the payload
            # payload should be a json dumped byte string
            # payload: b'{"command_hex": "515049beac0d", "result": "", "command": "QPI"}'
            log.debug(
                f"mqtt raw response on {self._msg.topic} was: {self._msg.payload}, payload type: {type(self._msg.payload)}"
            )
            # Return the byte-string to a dict
            payload_dict = js.loads(self._msg.payload)
            # Get 'results', and convert back to bytes
            result = binascii.unhexlify(payload_dict["result"])
            # TODO: Currently ignoring this - might want to update return types at some point
            cmd = payload_dict["command"]
            self._msg = None
            log.debug(f"mqtt response on {msg_topic} for command {cmd} was: {result}")
            return result

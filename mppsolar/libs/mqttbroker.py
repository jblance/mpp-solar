from dataclasses import dataclass
from typing import Optional

import paho.mqtt.client as mqtt_client


@dataclass
class MqttBroker:
    name: str
    port: int = 1883
    username: Optional[str] = None
    password: Optional[str] = None
    results_topic: Optional[str] = None

    # def __init__(self,):
    #     self.mqtt_broker = args.mqttbroker
    #     self.mqtt_port = args.mqttport
    #     # mqtt_topic = args.mqtttopic
    #     # if mqtt_topic is None:
    #     #     mqtt_topic = prog_name
    #     self.mqtt_user = args.mqttuser
    #     self.mqtt_pass = args.mqttpass

    def connect(self):
        mqttc = mqtt_client.Client()
        mqttc.connect(self.name, self.port, keepalive=60)

    def set(self, variable, value):
        setattr(self, variable, value)

    def update(self, variable, value):
        # only override if value is not None
        if value is None:
            return
        setattr(self, variable, value)

    def subscribe(self, topic, callback):
        # subscribe to mqtt topic
        # check if connected, connect if not
        # subscribe
        # register callback
        pass
        callback("client", "userdata", "msg")


if __name__ == "__main__":
    broker = MqttBroker("brokername")
    print(broker)
    broker.name = "test1"
    print(broker)

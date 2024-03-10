import paho.mqtt.publish as publish
import time


def _cb(client, userdata, msg):
    print(f"{msg.topic=}\n{msg.payload=}\n")


topic = "powermon2/adhoc_commands"
payload = "F50"

while True:
    print('loop')
    publish.single(topic, payload, hostname="localhost")
    time.sleep(15)

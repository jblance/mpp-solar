import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import time


def _cb(client, userdata, msg):
    print(f"{msg.topic=}\n{msg.payload=}\n")


topic = "powermon2/adhoc_commands"
result_topic = "powermon2/#"
adhoc_result_topic = "powermon2/adhoc_commands_results"
payload = "F50"
publish.single(topic, payload, hostname="localhost")

# subscribe.callback(_cb, result_topic, hostname="localhost")
#subscribe.callback(_cb, adhoc_result_topic, hostname="localhost")

while True:
    time.sleep(15)
    print('loop')
    publish.single(topic, payload, hostname="localhost")

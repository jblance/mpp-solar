import paho.mqtt.subscribe as subscribe


def _cb(client, userdata, msg):
    print(f"{msg.topic=}\n{msg.payload=}\n")


adhoc_result_topic = "powermon2/#"
subscribe.callback(_cb, adhoc_result_topic, hostname="localhost")

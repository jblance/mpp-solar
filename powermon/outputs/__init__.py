from powermon.formats import getFormatfromConfig
from .abstractoutput import OutputType
from powermon.libs.device import Device
from powermon.libs.mqttbroker import MqttBroker

def getOutputFromConfig(outputConfig: dict, topic: str, schedule_name: str, device: Device, mqtt_broker: MqttBroker):
    outputType = outputConfig["type"]

    formatConfig = outputConfig["format"]
    topic_override = outputConfig.get("topic_override", None)
    #use topic override from the config
    if(topic_override is not None):
        topic = topic_override

    format = getFormatfromConfig(formatConfig, device, topic)

    output_class = None
    #Only import the required class
    if outputType == OutputType.SCREEN:
        from .screen import Screen
        output_class = Screen(outputConfig, format)
    elif outputType == OutputType.MQTT:
        from .mqtt import MQTT
        output_class = MQTT(outputConfig, topic, mqtt_broker, format)
    elif outputType == OutputType.API_MQTT:
        from .api_mqtt import API_MQTT
        output_class = API_MQTT(outputConfig, topic, schedule_name, mqtt_broker, format)
        

    return output_class
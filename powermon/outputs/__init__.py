from powermon.formats import getFormatfromConfig
from .abstractoutput import OutputType

def getOutputFromConfig(outputConfig, device, mqtt_broker):
    outputType = outputConfig["type"]

    formatConfig = outputConfig["format"]
    topic = outputConfig.get("topic", None)
    tag = outputConfig.get("tag", None)
    format = getFormatfromConfig(formatConfig, device, topic, tag)

    output_class = None
    #Only import the required class
    if outputType == OutputType.SCREEN:
        from .screen import Screen
        output_class = Screen(outputConfig, format)
    elif outputType == OutputType.MQTT:
        from .mqtt import MQTT
        output_class = MQTT(outputConfig, mqtt_broker, format)
        

    return output_class
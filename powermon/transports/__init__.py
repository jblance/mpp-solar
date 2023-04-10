import logging
from powermon.transports.screen import Screen
from powermon.transports.mqtt import MQTT
from powermon.transports.mqtt_html import MQTT_HTML
from enum import StrEnum, auto

class OutputType(StrEnum):
    SCREEN = auto()
    MQTT = auto()
    MQTT_JSON = auto()
    MQTT_HTML = auto()

log = logging.getLogger("sender")

#TODO: replace with a abstract class with a factory method
def get_output(outputType, mqtt_broker, topic, tag):
    output_class = None
    log.debug(f"outputType: {outputType}")
    if outputType == OutputType.SCREEN:
        output_class = Screen()
    elif outputType == OutputType.MQTT:
        output_class = MQTT(mqtt_broker, topic, tag)
#    elif outputType == OutputType.MQTT_JSON:
#        output_class = MQTT_JSON(mqtt_broker, 'test', None)
    elif outputType == OutputType.MQTT_HTML:
        output_class = MQTT_HTML(mqtt_broker, topic, tag)
        
    log.debug(f"output_class: {output_class}")

    return output_class


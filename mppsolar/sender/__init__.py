import logging
from mppsolar.sender.screen import Screen
from mppsolar.sender.mqtt import MQTT
from mppsolar.sender.mqtt_html import MQTT_HTML
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


#def output_results(results, command, mqtt_broker, fullconfig={}):
    # "normal command definition"
    # - command: QPIGS
    #   outputs:
    #   - name: screen
    #     format: raw
    #     tag: Test_Inverter
    #     filter: ^serial|^work|^charger|^fault
    #   - name: mqtt
    #     results_topic: results/qpigs
    #
    # or "adhoc_commands"
    #  topic: test/command_topic
    #  outputs:
    #  - name: screen

    # Check if an outputs section was supplied
#    if "outputs" in command:
#        outputs = command["outputs"]
    # if not default to screen
#    else:
#        outputs["name"] = "screen"
#    for op in outputs:
#        # filter = config.get("CONFIG", "filter")
#        # log.debug(f"Using output filter: {filter}")
#        if "name" in op:
#            output = get_output(op["name"])
#        else:
#            output = get_output("screen")
#        output.output(
#            data=dict(results),
#            config=op,
#            mqtt_broker=mqtt_broker,
#            fullconfig=fullconfig,
#        )

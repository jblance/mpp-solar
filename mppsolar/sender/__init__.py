import logging
from mppsolar.sender.screen import Screen
from mppsolar.sender.mqtt import MQTT
from enum import StrEnum, auto

class OutputType(StrEnum):
    SCREEN = auto()
    MQTT = auto()

log = logging.getLogger("sender")


def get_output(output):

    output_class = None

    if output == OutputType.SCREEN:
        output_class = Screen()
    elif output == OutputType.MQTT:
        output_class = MQTT()

    return output_class


def output_results(results, command, mqtt_broker, fullconfig={}):
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
    if "outputs" in command:
        outputs = command["outputs"]
    # if not default to screen
    else:
        outputs["name"] = "screen"
    for op in outputs:
        # filter = config.get("CONFIG", "filter")
        # log.debug(f"Using output filter: {filter}")
        if "name" in op:
            output = get_output(op["name"])
        else:
            output = get_output("screen")
        output.output(
            data=dict(results),
            config=op,
            mqtt_broker=mqtt_broker,
            fullconfig=fullconfig,
        )

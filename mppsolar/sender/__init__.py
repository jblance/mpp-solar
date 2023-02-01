import logging
import importlib

# import pkgutil
# import re

# from ..helpers import key_wanted, get_kwargs

log = logging.getLogger("sender")


def get_output(output):
    """
    Take an output name
    attempt to find and instantiate the corresponding module
    """
    log.info(f"attempting to create output processor: {output}")
    try:
        output_module = importlib.import_module("mppsolar.sender." + output, ".")
        output_class = getattr(output_module, output)
        return output_class()
    except ModuleNotFoundError as e:
        # perhaps raise a Powermon exception here??
        # maybe warn and keep going, only error if no outputs found?
        log.critical(f"No module found for output processor {output} Error: {e}")
    return None


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

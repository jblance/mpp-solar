import logging
import importlib
import pkgutil
import re

from ..helpers import key_wanted, get_kwargs

log = logging.getLogger("helpers")


def list_outputs():
    # print("outputs list outputs")
    pkgpath = __file__
    pkgpath = pkgpath[: pkgpath.rfind("/")]
    pkgpath += "/../outputs"
    # print(pkgpath)
    result = {}
    result["_command"] = "outputs help"
    result["_command_description"] = "List available output modules"
    for _, name, _ in pkgutil.iter_modules([pkgpath]):
        # print(name)
        try:
            _module_class = importlib.import_module("mppsolar.outputs." + name, ".")
            _module = getattr(_module_class, name)
            result[name] = (str(_module()), "", "")
        except ModuleNotFoundError as e:
            # log.error(f"Error in module {name}: {e}")
            result[f"{name}*"] = (f"ERROR: {e}", "", "")
        # print(_module())

    # print(result)
    return result


def get_output(output):
    """
    Take an output name
    attempt to find and instantiate the corresponding module
    """
    log.info(f"attempting to create output processor: {output}")
    try:
        output_module = importlib.import_module("mppsolar.outputs." + output, ".")
        output_class = getattr(output_module, output)
        return output_class()
    except ModuleNotFoundError as e:
        # perhaps raise a Powermon exception here??
        # maybe warn and keep going, only error if no outputs found?
        log.critical(f"No module found for output processor {output} Error: {e}")
    return None


def get_outputs(output_list):
    """
    Take a comma separated list of output names
    attempt to find and instantiate the corresponding module
    return array of modules
    """
    ops = []
    outputs = output_list.split(",")
    for output in outputs:
        op = get_output(output)
        if op is not None:
            ops.append(op)
    return ops


def output_results(results, command, mqtt_broker, fullconfig={}):
    # "normal command definition"
    # - command: QPIGS
    #   outputs:
    #   - name: screen
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
        output = get_output(op.get("name", "screen"))
        output.output(
            data=dict(results),
            config=op,
            mqtt_broker=mqtt_broker,
            fullconfig=fullconfig,
        )


def to_json(data, keep_case, excl_filter, filter):
    output = {}
    # Loop through responses
    for key, value in data.items():
        log.debug(f"value: {value}")
        if isinstance(value, list):
            value = value[0]
        # unit = value[1]
        # remove spaces
        key = key.replace(" ", "_")
        if not keep_case:
            # make lowercase
            key = key.lower()
        if key_wanted(key, filter, excl_filter):
            output[key] = value
    return output


def to_json_units(data, keep_case, excl_filter, filter):
    output = {}
    # Loop through responses
    for key, value in data.items():
        unit = None
        log.debug(f"value: {value}")
        if isinstance(value, list):
            unit = value[1]
            value = value[0]
        # remove spaces
        key = key.replace(" ", "_")
        if not keep_case:
            # make lowercase
            key = key.lower()
        if key_wanted(key, filter, excl_filter):
            if unit is None:
                output[key] = value
            else:
                # { "ac_output_voltage": { "value": 220, "unit": "V" }, ... }
                output[key] = {"value": value, "unit": unit}
    return output


def get_common_params(kwargs):
    data = get_kwargs(kwargs, "data")
    tag = get_kwargs(kwargs, "tag")
    keep_case = get_kwargs(kwargs, "keep_case")
    filter_ = get_kwargs(kwargs, "filter")
    if filter_ is not None:
        filter_ = re.compile(filter_)
    excl_filter = get_kwargs(kwargs, "excl_filter")
    if excl_filter is not None:
        excl_filter = re.compile(excl_filter)
    return data, tag, keep_case, filter_, excl_filter

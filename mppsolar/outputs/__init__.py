import logging
import importlib
import pkgutil
import re

from ..helpers import key_wanted, get_kwargs

log = logging.getLogger("helpers")


def list_outputs():
    print("outputs list outputs")
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
        except ModuleNotFoundError as e:
            log.error(f"Error in module {name}: {e}")
        # print(_module())
        result[name] = (str(_module()), "", "")
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


def output_results(results, outputs, mqtt_broker):
    print(outputs)

    for op in outputs:
        # maybe include the command and what the command is im the output
        # eg QDI run, Display Inverter Default Settings
        # filter = config.get("CONFIG", "filter")
        # log.debug(f"Using output filter: {filter}")
        output = get_output(op["name"])
        output.output(
            data=dict(results),
            # tag=config.get("CONFIG", "tag"),
            mqtt_broker=mqtt_broker,
            # filter=filter,
            # excl_filter=excl_filter,
            # keep_case=keep_case,
        )


def to_json(data, keep_case, excl_filter, filter):
    output = {}
    # Loop through responses
    for key in data:
        value = data[key]
        log.debug(f"value: {value}")
        if isinstance(value, list):
            value = data[key][0]
        # unit = data[key][1]
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
    for key in data:
        value = data[key]
        unit = None
        log.debug(f"value: {value}")
        if isinstance(value, list):
            value = data[key][0]
            unit = data[key][1]
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

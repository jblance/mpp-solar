import logging
import importlib
import pkgutil

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
        _module_class = importlib.import_module("mppsolar.outputs." + name, ".")
        _module = getattr(_module_class, name)
        # print(_module())
        result[name] = (str(_module()), "", "")
    # print(result)
    return result


def get_outputs(output_list):
    """
    Take a comma separated list of output names
    attempt to find and instantiate the corresponding module
    return array of modules
    """
    ops = []
    outputs = output_list.split(",")
    for output in outputs:
        log.info(f"attempting to create output processor: {output}")
        try:
            output_module = importlib.import_module("mppsolar.outputs." + output, ".")
            output_class = getattr(output_module, output)
            ops.append(output_class())
        except ModuleNotFoundError:
            # perhaps raise a Powermon exception here??
            # maybe warn and keep going, only error if no outputs found?
            log.critical(f"No module found for output processor {output}")
    return ops


def output_results(results, config, mqtt_broker):
    outputs = get_outputs(config["outputs"])
    for op in outputs:
        # maybe include the command and what the command is im the output
        # eg QDI run, Display Inverter Default Settings
        filter = config.get("CONFIG", "filter")
        log.debug(f"Using output filter: {filter}")
        op.output(
            data=dict(results),
            tag=config.get("CONFIG", "tag"),
            mqtt_broker=mqtt_broker,
            # filter=filter,
            # excl_filter=excl_filter,
            # keep_case=keep_case,
        )

#!/usr/bin/env python3
import logging
import importlib

log = logging.getLogger("helpers")


def get_kwargs(kwargs, key, default=None):
    if key not in kwargs or not kwargs[key]:
        return default
    return kwargs[key]


def key_wanted(key, filter=None, excl_filter=None):
    # remove any specifically excluded keys
    if excl_filter is not None and excl_filter.search(key):
        # log.debug(f"key_wanted: key {key} matches excl_filter {excl_filter} so key excluded")
        return False
    if filter is None:
        # log.debug(
        #    f"key_wanted: No filter and key {key} not excluded by excl_filter {excl_filter} so key wanted"
        # )
        return True
    elif filter.search(key):
        # log.debug(
        #    f"key_wanted: key {key} matches filter {filter} and not excl_filter {excl_filter} so key wanted"
        # )
        return True
    else:
        # log.debug(f"key_wanted: key {key} does not match filter {filter} so key excluded")
        return False


def get_resp_defn(key, defns):
    """
    look for a definition for the supplied key
    """
    # print(key, defns)
    if not key:
        return None
    if type(key) is bytes:
        try:
            key = key.decode("utf-8")
        except UnicodeDecodeError:
            log.info(f"key decode error for {key}")
    for defn in defns:
        if key == defn[0]:
            # print(key, defn)
            return defn
    # did not find definition for this key
    log.info(f"No defn found for {key} key")
    return [key, key, "", ""]


# def get_outputs(output_list):
#     """
#     Take a comma separated list of output names
#     attempt to find and instantiate the corresponding module
#     return array of modules
#     """
#     ops = []
#     outputs = output_list.split(",")
#     for output in outputs:
#         log.info(f"attempting to create output processor: {output}")
#         try:
#             output_module = importlib.import_module("mppsolar.outputs." + output, ".")
#             output_class = getattr(output_module, output)
#             ops.append(output_class())
#         except ModuleNotFoundError:
#             # perhaps raise a Powermon exception here??
#             # maybe warn and keep going, only error if no outputs found?
#             log.critical(f"No module found for output processor {output}")
#     return ops


def get_device_class(device_type=None):
    """
    Take a device type string
    attempt to find and instantiate the corresponding module
    return class if found, otherwise return None
    """
    if device_type is None:
        return None
    device_type = device_type.lower()
    try:
        device_module = importlib.import_module("mppsolar.devices." + device_type, ".")
    except ModuleNotFoundError as e:
        # perhaps raise a mppsolar exception here??
        log.critical(f"Error loading device {device_type}: {e}")
        return None
    device_class = getattr(device_module, device_type)
    return device_class

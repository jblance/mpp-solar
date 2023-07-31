import logging
import re

from .baseoutput import baseoutput
from ..helpers import get_kwargs, key_wanted

log = logging.getLogger("prom")


class prom(baseoutput):
    def __str__(self):
        return "outputs Node exporter prometheus format to standard out"

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.value __init__ kwargs {kwargs}")

    def printHeader(command, description):
        pass

    def output(self, *args, **kwargs):
        log.info("Using output processor: value")
        log.debug(f"kwargs {kwargs}")
        dev = get_kwargs(kwargs, "dev")
        data = get_kwargs(kwargs, "data")
        name = get_kwargs(kwargs, "name")
        if data is None:
            return

        # check if config supplied
        config = get_kwargs(kwargs, "config")
        if config is not None:
            log.debug(f"config: {config}")
            # get formatting info
            remove_spaces = config.get("remove_spaces", True)
            keep_case = config.get("keep_case", False)
            filter = config.get("filter", None)
            excl_filter = config.get("excl_filter", None)
            name = config.get("name", "mpp_solar")
            dev = config.get("dev", "None")
        else:
            # get formatting info
            remove_spaces = True
            keep_case = get_kwargs(kwargs, "keep_case")
            filter = get_kwargs(kwargs, "filter")
            excl_filter = get_kwargs(kwargs, "excl_filter")
            name = get_kwargs(kwargs, "name")

        if filter is not None:
            filter = re.compile(filter)
        if excl_filter is not None:
            excl_filter = re.compile(excl_filter)
        if name == "unnamed":
            name = "mpp_solar"
        # remove raw response
        if "raw_response" in data:
            data.pop("raw_response")

        cmd = data.pop("_command", None)

        # build header
        if "_command_description" in data:
            data.pop("_command_description")

        # build data to display
        displayData = {}
        for key in data:
            _values = data[key]
            # remove spaces
            if remove_spaces:
                key = key.replace(" ", "_")
            if not keep_case:
                # make lowercase
                key = key.lower()
            if key_wanted(key, filter, excl_filter):
                displayData[key] = _values
        log.debug(f"displayData: {displayData}")

        # print data
        print(f'machine_role{{role="mpp_solar"}} 1')
        for key in displayData:
            value = displayData[key][0]
            if isinstance(value, str):
                print(f'mpp_solar_{key}{{inverter="{name}",device="{dev}",cmd="{cmd}",myStr="{value}"}} 1')
            else:
                print(f'mpp_solar_{key}{{inverter="{name}",device="{dev}",cmd="{cmd}"}} {value}')

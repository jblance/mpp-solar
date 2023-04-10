import logging
import re

from mppsolar.helpers import get_kwargs, key_wanted

log = logging.getLogger("simple")


class simple:
    def output(*args, **kwargs):
        log.info("Using output formatter: simple")
        log.debug(f"kwargs {kwargs}")
        data = get_kwargs(kwargs, "data")

        _result = []
        if data is None:
            return _result

        # check if config supplied
        config = get_kwargs(kwargs, "config")
        if config is not None:
            log.debug(f"config: {config}")
            # get formatting info
            remove_spaces = config.get("remove_spaces", True)
            keep_case = config.get("keep_case", False)
            extra_info = config.get("extra_info", False)
            filter = config.get("filter", None)
            excl_filter = config.get("excl_filter", None)

        _filter = None
        _excl_filter = None

        if filter is not None:
            _filter = re.compile(filter)

        if excl_filter is not None:
            _excl_filter = re.compile(excl_filter)

        # remove raw response
        if "raw_response" in data:
            data.pop("raw_response")

        # remove command details
        if "_command" in data:
            data.pop("_command")
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
            if key_wanted(key, _filter, _excl_filter):
                displayData[key] = _values
        log.debug(f"displayData: {displayData}")

        # build data
        for key in displayData:
            value = displayData[key][0]
            unit = displayData[key][1]
            if len(displayData[key]) > 2 and displayData[key][2] and extra_info:
                extra = displayData[key][2]
                _result.append(f"{key}={value}{unit} {extra}")
            else:
                _result.append(f"{key}={value}{unit}")
        return _result

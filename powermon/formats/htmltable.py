import logging
import re

from mppsolar.helpers import get_kwargs, key_wanted

log = logging.getLogger("htmltable")


class htmltable:
    def output(*args, **kwargs):
        log.info("Using output formatter: htmltable")
        log.debug(f"kwargs {kwargs}")
        data = get_kwargs(kwargs, "data")

        _result = ""
        if data is None:
            return _result

        # check if config supplied
        config = get_kwargs(kwargs, "config")
        if config is not None:
            log.debug(f"config: {config}")
            # get formatting info
            remove_spaces = config.get("remove_spaces", True)
            keep_case = config.get("keep_case", False)
            # extra_info = config.get("extra_info", False)
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

        # build header
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

        # build header
        # _result.append(f"Command: {command} - {description}")
        # if filter or excl_filter:
        #     _result.append(
        #         f"Using filter: '{filter}' and excl_filter: '{excl_filter}'. {len(displayData)} results retained from {len(data)} in total"
        #     )
        # _result.append("-" * 80)

        # build data
        # maxP = getMaxLen(displayData)
        # if maxP < 9:
        #     maxP = 9
        # maxV = getMaxLen(data.values())
        _result += "<table><tr><th>Parameter</th><th>Value</th><th>Unit</th></tr>"
        for key in displayData:
            value = displayData[key][0]
            unit = displayData[key][1]
            _result += f"<tr><td>{key}</td><td>{value}</td><td>{unit}</td></tr>"
        _result += "</table>"
        return _result

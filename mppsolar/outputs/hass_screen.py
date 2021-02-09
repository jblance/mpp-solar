import logging
import re


from .hass_mqtt import hass_mqtt
from ..helpers import get_kwargs
from ..helpers import key_wanted

log = logging.getLogger("MPP-Solar")


class hass_screen(hass_mqtt):
    def __str__(self):
        return """outputs the to the screen (ie used to debug hass_mqtt) in hass format: eg "homeassistant/sensor/mpp_{tag}_{key}/state" """

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.hass_screen __init__ kwargs {kwargs}")

    def output(self, *args, **kwargs):
        log.info("Using output processor: hass_screen")
        log.debug(f"processor.hass_screen.output kwargs {kwargs}")
        data = get_kwargs(kwargs, "data")
        if data is None:
            return

        filter = get_kwargs(kwargs, "filter")
        if filter is not None:
            filter = re.compile(filter)
        excl_filter = get_kwargs(kwargs, "excl_filter")
        if excl_filter is not None:
            excl_filter = re.compile(excl_filter)

        msgs = self.build_msgs(**kwargs)
        log.debug(f"hass_screen.output msgs {msgs}")
        if msgs:
            for msg in msgs:
                print(msg)
        else:
            log.warn("MQTT build_msgs returned no messages")

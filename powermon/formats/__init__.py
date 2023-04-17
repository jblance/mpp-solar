from .htmltable import htmltable
from .hass import hass
from .abstractformat import FormatterType


def getFormatfromConfig(formatConfig, device):
    #Get values from config
    #Type is required
    formatType = formatConfig["type"]

    #Optional format values
    remove_spaces = formatConfig.get("remove_spaces", True)
    keep_case = formatConfig.get("keep_case", False)
    filter = formatConfig.get("filter", None)
    excl_filter = formatConfig.get("excl_filter", None)

    if formatType == FormatterType.HTMLTABLE:
        formatter = htmltable(remove_spaces, keep_case, filter, excl_filter)
    elif formatType == FormatterType.HASS:
        discovery_prefix = formatConfig.get("discovery_prefix", "homeassistant")
        entity_id_prefix = formatConfig.get("entity_id_prefix", "mpp")
        formatter = hass(remove_spaces, keep_case, filter, excl_filter, discovery_prefix, entity_id_prefix, device.name, device.id, device.model, device.manufacturer)
    #elif formatType == FormatterType.SIMPLE:
        #formatter = simple(mqtt_broker, topic, tag)

    return formatter
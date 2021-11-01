import importlib
import logging

log = logging.getLogger("protocols")


def get_protocol(protocol):
    """
    Get the protocol based on the protocol name
    """

    log.debug(f"Protocol {protocol}")
    if protocol is None:
        return None
    protocol_id = protocol.lower()
    # Try to import the protocol module with the supplied name (may not exist)
    try:
        proto_module = importlib.import_module("mppsolar.protocols." + protocol_id, ".")
    except ModuleNotFoundError:
        log.error(f"No module found for protocol {protocol_id}")
        return None
    # Find the protocol class - classname must be the same as the protocol_id
    try:
        protocol_class = getattr(proto_module, protocol_id)
    except AttributeError:
        log.error(f"Module {proto_module} has no attribute {protocol_id}")
        return None
    # Return the instantiated class
    return protocol_class()

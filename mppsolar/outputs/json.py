import logging

log = logging.getLogger("MPP-Solar")


class json:
    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.json __init__ kwargs {kwargs}")

    def output(self, data=None, tag=None, mqtt_broker="localhost", mqtt_user=None, mqtt_pass=None):
        log.info("Using output processor: json")
        output = {}
        for key in data:
            value = data[key][0]
            # unit = data[key][1]
            output[key] = value
        print(output)

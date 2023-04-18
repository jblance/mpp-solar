# Description: Output format for mqtt as individual topics
import logging
from powermon.formats.abstractformat import AbstractFormat

log = logging.getLogger("Topics")


class Topics(AbstractFormat):
    def __init__(self, formatConfig):
        super().__init__(formatConfig)
        self.results_topic = formatConfig.get("topic", None)
        self.tag = formatConfig.get("tag", None)


    def format(self, data):
        log.info("Using output formatter: Topics")
        

        # build topic prefix
        if self.results_topic is not None:
            topic_prefix = self.results_topic + "/" + self.tag
        else:
            topic_prefix = f"{self.tag}/status"


        _data = self.formatAndFilterData(data)

        # Build array of mqtt messages
        msgs = []
        # Loop through responses build topics and messages
        for key in _data:
            value = _data[key][0]
            unit = _data[key][1]
            log.debug(
                f"build_msgs: prefix {topic_prefix}, key {key}, value {value}, unit {unit}"
            )
            msg = {"topic": f"{topic_prefix}/{key}/value", "payload": value}
            msgs.append(msg)
            if unit:
                msg = {"topic": f"{topic_prefix}/{key}/unit", "payload": unit}
                msgs.append(msg)
        log.debug(f"build_msgs: {msgs}")
        return msgs
# Description: Output format for mqtt as individual topics
import logging
from powermon.formats.abstractformat import AbstractFormat

log = logging.getLogger("Topics")


class Topics(AbstractFormat):
    def __init__(self, formatConfig, topic):
        super().__init__(formatConfig)
        self.name = "topics"
        self.results_topic = topic

    def sendsMultipleMessages(self) -> bool:
        return True

    def format(self, result):
        log.info("Using output formatter: %s" % self.name)

        _result = []
        data = result.decoded_responses
        if data is None:
            return _result

        displayData = self.formatAndFilterData(data)
        log.debug(f"displayData: {displayData}")

        # Build array of mqtt messages
        msgs = []
        # Loop through responses build topics and messages
        for key in data:
            value = data[key][0]
            unit = data[key][1]
            log.debug(f"build_msgs: prefix {self.results_topic}, key {key}, value {value}, unit {unit}")
            msg = {"topic": f"{self.results_topic}/{key}/value", "payload": value}
            msgs.append(msg)
            if unit:
                msg = {"topic": f"{self.results_topic}/{key}/unit", "payload": unit}
                msgs.append(msg)
        log.debug(f"build_msgs: {msgs}")
        return msgs

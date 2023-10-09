# Description: Output format for mqtt as individual topics
import logging
from powermon.formats.abstractformat import AbstractFormat
from powermon.commands.result import Result

log = logging.getLogger("Topics")


class Topics(AbstractFormat):
    def __init__(self, formatConfig, topic):
        super().__init__(formatConfig)
        self.name = "topics"
        self.results_topic = topic

    def sendsMultipleMessages(self) -> bool:
        return True

    def format(self, result: Result):
        log.info("Using output formatter: %s" % self.name)

        _result = []
        
        if len(result.get_responses()) == 0:
            return _result

        display_data = self.format_and_filter_data(result)
        log.debug(f"displayData: {display_data}")

        # Build array of mqtt messages
        msgs = []
        # Loop through responses build topics and messages
        for response in result.get_responses():
            value = response.get_data_value()
            unit = response.get_data_unit()
            name = response.get_data_name()
            log.debug(f"build_msgs: prefix {self.results_topic}, key {key}, value {value}, unit {unit}")
            msg = {"topic": f"{self.results_topic}/{name}/value", "payload": value}
            msgs.append(msg)
            if unit:
                msg = {"topic": f"{self.results_topic}/{name}/unit", "payload": unit}
                msgs.append(msg)
        log.debug(f"build_msgs: {msgs}")
        return msgs

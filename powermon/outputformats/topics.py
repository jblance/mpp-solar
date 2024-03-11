# Description: Output format for mqtt as individual topics
import logging
from powermon.outputformats.abstractformat import AbstractFormat
from powermon.commands.result import Result

log = logging.getLogger("Topics")


class Topics(AbstractFormat):
    def __init__(self, config, topic):
        super().__init__(config)
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
            value = response.data_value
            unit = response.data_unit
            name = response.data_name
            log.debug(f"build_msgs: prefix {self.results_topic}, key {key}, value {value}, unit {unit}")
            msg = {"topic": f"{self.results_topic}/{name}/value", "payload": value}
            msgs.append(msg)
            if unit:
                msg = {"topic": f"{self.results_topic}/{name}/unit", "payload": unit}
                msgs.append(msg)
        log.debug(f"build_msgs: {msgs}")
        return msgs

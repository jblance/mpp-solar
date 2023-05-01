import yaml
import logging
import json
from powermon.libs.schedule import Schedule

log = logging.getLogger("APICoordinator")
class ApiCoordinator:
    def __init__(self, config, device, mqtt_broker, schedule : Schedule):
        self.device = device
        self.mqtt_broker = mqtt_broker
        self.schedule = schedule
        self.count = 0
        self.adhocTopic = config.get("adhoc_topic", "powermon/adhoc")
        self.announceTopic = config.get("announce_topic", "powermon/announce")

        self.announceDevice()
        mqtt_broker.subscribe(self.adhocTopic, self.adhocCallback)

        #mqtt_broker.publish(self.announceTopic, self.schedule.getScheduleConfigAsJSON())

    def adhocCallback(self, client, userdata, msg):
        log.info(f"Received `{msg.payload}` on topic `{msg.topic}`")
        yamlString = msg.payload.decode("utf-8")
        log.debug(f"Yaml string: {yamlString}")
        try:
            _command_config = yaml.safe_load(yamlString)
        except yaml.YAMLError as exc:
            log.error(f"Error processing config file: {exc}")

        for command in _command_config["commands"]:
            log.debug(f"command: {command}")
            log.debug(f"self: {self}")
            self.schedule.addOneTimeCommandFromConfig(command)

    def run(self):
        if(self.count > 20):
            log.info("Starting APICoordinator")
            self.announceDevice()
            self.count = 0

        self.count += 1

    def announceDevice(self):
        scheduleDTO = self.schedule.toDTO()
        self.mqtt_broker.publish(self.announceTopic, scheduleDTO.json())
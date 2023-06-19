import logging
from time import time

import yaml

from powermon.scheduling.scheduleController import ScheduleController

log = logging.getLogger("APICoordinator")


class ApiCoordinator:
    def __str__(self):
        if not self.enabled:
            return "ApiCoordinator DISABLED"
        return f"ApiCoordinator: adhocTopic: {self.adhocTopic}, announceTopic: {self.announceTopic}, schedule: {self.schedule}"

    def __init__(self, config, device, mqtt_broker, schedule: ScheduleController):
        log.debug(f"ApiCoordinator config: {config}")
        self.device = device
        self.mqtt_broker = mqtt_broker
        self.schedule = schedule
        self.last_run = None
        if not config:
            self.enabled = False
            return
        self.adhocTopic = config.get("adhoc_topic", "powermon/adhoc")
        self.announceTopic = config.get("announce_topic", "powermon/announce")
        self.enabled = config.get("enabled", True)  # default to enabled if not specified

        if self.mqtt_broker is None or self.mqtt_broker.disabled:
            # no use having api running if no mqtt broker
            log.warn("No mqttbroker (or it is disabled) so disabling ApiCoordinator")
            self.enabled = False
            return

        self.announce_device()
        mqtt_broker.subscribe(self.adhocTopic, self.adhocCallback)

        # mqtt_broker.publish(self.announceTopic, self.schedule.getScheduleConfigAsJSON())

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
        if not self.enabled:
            return
        if not self.last_run or time() - self.last_run > 60:
            log.info("Starting APICoordinator")
            self.announce_device()
            self.last_run = time()

    def announce_device(self):
        """Announce the device on the announce topic"""
        schedule_dto = self.schedule.to_dto()
        self.mqtt_broker.publish(self.announceTopic, schedule_dto.json())

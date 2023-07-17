import logging
from time import time

import yaml

log = logging.getLogger("APICoordinator")


class ApiCoordinator:
    def __str__(self):
        if not self.enabled:
            return "ApiCoordinator DISABLED"
        return f"ApiCoordinator: adhocTopic: {self.adhocTopic}, announceTopic: {self.announceTopic}"

    @classmethod
    def fromConfig(cls, config=None, device=None, mqtt_broker=None):
        log.debug(f"ApiCoordinator config: {config}")
        if not config:
            log.info("No api definition in config")
            adhocTopic = "powermon/adhoc"
            announceTopic = "powermon/announce"
            enabled = False
        else:
            adhocTopic = config.get("adhoc_topic", "powermon/adhoc")
            announceTopic = config.get("announce_topic", "powermon/announce")
            enabled = config.get("enabled", True)  # default to enabled if not specified

        return cls(adhocTopic=adhocTopic, announceTopic=announceTopic, enabled=enabled, device=device, mqtt_broker=mqtt_broker)

    def __init__(self, adhocTopic : str, announceTopic: str, enabled: bool, device=None, mqtt_broker=None):
        self.device = device
        self.mqtt_broker = mqtt_broker
        self.last_run = None
        self.adhocTopic = adhocTopic
        self.announceTopic = announceTopic
        self.enabled = enabled

        if self.mqtt_broker is None or self.mqtt_broker.disabled:
            # no use having api running if no mqtt broker
            log.debug(self.mqtt_broker)
            log.debug("No mqttbroker (or it is disabled) so disabling ApiCoordinator")
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
            # self.schedule.addOneTimeCommandFromConfig(command)

    def run(self):
        if not self.enabled:
            return
        if not self.last_run or time() - self.last_run > 60:
            log.info("APICoordinator running")
            self.announce_device()
            self.last_run = time()

    def announce_device(self):
        device_dto = self.device.toDTO()
        self.mqtt_broker.publish(self.announceTopic, device_dto.json())

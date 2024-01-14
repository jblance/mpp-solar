""" apicoordinator.py """
import logging
from time import time

from powermon.commands.command import Command
from powermon.commands.trigger import Trigger
from powermon.device import Device
from powermon.dto.commandDTO import CommandDTO
from powermon.dto.apicoordinatorDTO import ApicoordinatorDTO
from powermon.formats.simple import SimpleFormat
from powermon.outputs.api_mqtt import ApiMqtt

log = logging.getLogger("APICoordinator")


class ApiCoordinator:
    """ apicoordinator coordinates the api / mqtt interface """
    def __str__(self):
        if not self.enabled:
            return "ApiCoordinator DISABLED"
        return f"ApiCoordinator: adhocTopic: {self.adhoc_topic_format}, announceTopic: {self.announce_topic}"

    def to_dto(self):
        """ convert object to data transfer object """
        dto = ApicoordinatorDTO(name="ApiCoordinator", description="api coordinator to_dto is todo")
        return dto

    @classmethod
    def from_config(cls, config=None):
        """ build apicoordinator object from config dict """
        log.debug("ApiCoordinator config: %s", config)
        if not config:
            log.info("No api definition in config")
            refresh_interval = 300
            enabled = False
            announce_topic = "powermon/announce"
            adhoc_topic_format = "powermon/{device_id}/addcommand"
        else:
            refresh_interval = config.get("refresh_interval", 300)
            enabled = config.get("enabled", True)  # default to enabled if not specified
            announce_topic = config.get("announce_topic", "powermon/announce")
            adhoc_topic_format = config.get("adhoc_topic_format", "powermon/{device_id}/addcommand")

        return cls(adhoc_topic_format=adhoc_topic_format, announce_topic=announce_topic, enabled=enabled, refresh_interval=refresh_interval)

    def __init__(self, adhoc_topic_format: str, announce_topic: str, enabled: bool, refresh_interval: int):
        self.device = None
        self.mqtt_broker = None
        self.last_run = None
        self.adhoc_topic_format = adhoc_topic_format
        self.announce_topic = announce_topic
        self.refresh_interval = refresh_interval
        self.enabled = enabled

    def set_device(self, device: Device):
        """ store the device in the apicoordinator """
        self.device = device
        # self.announce(self.device)

    def set_mqtt_broker(self, mqtt_broker):
        """ store the mqtt broker in the apicoordinator """
        log.debug("setting mqtt_broker to %s", mqtt_broker)
        self.mqtt_broker = mqtt_broker

        if self.mqtt_broker is None or self.mqtt_broker.disabled:
            # no use having api running if no mqtt broker
            log.debug(self.mqtt_broker)
            log.debug("No mqttbroker (or it is disabled) so disabling ApiCoordinator")
            self.enabled = False
            return

        mqtt_broker.subscribe(self.get_addcommand_topic(), self.addcommand_callback)
        # mqtt_broker.publish(self.announceTopic, self.schedule.getScheduleConfigAsJSON())

    def get_addcommand_topic(self):
        """ get the adhoc topic """
        return self.adhoc_topic_format.format(device_id=self.device.device_id)

    def addcommand_callback(self, client, userdata, msg):
        """ add a callback """
        log.info("Client: %s, with userdata: %s, received `%s` on topic `%s`", client, userdata,msg.payload, msg.topic)
        json_string = msg.payload.decode("utf-8")
        log.debug("Yaml string: %s ", json_string)

        dto = CommandDTO.parse_raw(json_string)

        trigger = Trigger.from_dto(dto.trigger)
        command = Command.from_dto(dto)
        Command(code=dto.command_code, commandtype="basic", outputs=[], trigger=trigger)
        outputs = []

        output = ApiMqtt()
        output.set_formatter(SimpleFormat({}))
        outputs.append(output)

        command.outputs = outputs
        command.mqtt_broker = self.mqtt_broker

        self.device.add_command(command)

        return command

    def run(self):
        """ regular processing function, ensures that the announce isnt too frequent """
        if not self.enabled:
            return
        if not self.last_run or time() - self.last_run > self.refresh_interval:
            log.info("APICoordinator running")
            self.announce(self.device)
            self.last_run = time()

    def initialize(self):
        """ initialize the apicoordinator """
        if not self.enabled:
            return
        self.announce(self)

    def announce(self, obj):
        """ Announce jsonised obj dto to api """
        obj_dto = obj.to_dto()
        if not self.enabled:
            log.debug("Not announcing obj: %s as api DISABLED", obj_dto)
            return
        log.debug("Announcing obj: %s to api on topic: %s", obj_dto, self.announce_topic)
        self.mqtt_broker.publish(self.announce_topic, obj_dto.json())

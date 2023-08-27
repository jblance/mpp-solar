import logging
from time import time

from powermon.device import Device
from powermon.commands.command import Command
from powermon.commands.trigger import Trigger
from powermon.dto.commandDTO import CommandDTO
from powermon.formats.simple import SimpleFormat
from powermon.outputs.api_mqtt import API_MQTT

log = logging.getLogger("APICoordinator")



class ApiCoordinator:
    def __str__(self):
        if not self.enabled:
            return "ApiCoordinator DISABLED"
        return f"ApiCoordinator: adhocTopic: {self.adhoc_topic_format}, announceTopic: {self.announce_topic}"

    @classmethod
    def from_config(cls, config=None, device=None, mqtt_broker=None):
        log.debug(f"ApiCoordinator config: {config}")
        if not config:
            log.info("No api definition in config")
            refresh_interval = 60
            enabled = False
        else:
            refresh_interval = config.get("refresh_interval", 60)
            enabled = config.get("enabled", True)  # default to enabled if not specified

        adhoc_topic_format = "powermon/{device_id}/addcommand"
        announce_topic = "powermon/announce"

        return cls(adhoc_topic_format=adhoc_topic_format, announce_topic=announce_topic, enabled=enabled, refresh_interval=refresh_interval, device=device, mqtt_broker=mqtt_broker)

    def __init__(self, adhoc_topic_format : str, announce_topic: str, enabled: bool, refresh_interval: int, device: Device, mqtt_broker=None):
        self.device : Device = device
        self.mqtt_broker = mqtt_broker
        self.last_run = None
        self.adhoc_topic_format = adhoc_topic_format
        self.announce_topic = announce_topic
        self.refresh_interval = refresh_interval
        self.enabled = enabled

        if self.mqtt_broker is None or self.mqtt_broker.disabled:
            # no use having api running if no mqtt broker
            log.debug(self.mqtt_broker)
            log.debug("No mqttbroker (or it is disabled) so disabling ApiCoordinator")
            self.enabled = False
            return

        self.announce_device()
        mqtt_broker.subscribe(self.get_addcommand_topic(), self.addcommand_callback)  # QUESTION: why subscribe here?

        # mqtt_broker.publish(self.announceTopic, self.schedule.getScheduleConfigAsJSON())

    def get_addcommand_topic(self):
        return self.adhoc_topic_format.format(device_id=self.device.identifier)

    def addcommand_callback(self, client, userdata, msg):
        log.info(f"Received `{msg.payload}` on topic `{msg.topic}`")
        jsonString = msg.payload.decode("utf-8")
        log.debug(f"Yaml string: {jsonString}")

        dto = CommandDTO.parse_raw(jsonString)
        
        trigger = Trigger.from_DTO(dto.trigger)    
        command = Command.from_DTO(dto)
        Command(code=dto.command_code, commandtype="basic", outputs=[], trigger=trigger)
        outputs = []
        
        
        output = API_MQTT(formatter=SimpleFormat({}))
        outputs.append(output)
            
        command.set_outputs(outputs=outputs)
        command.set_mqtt_broker(self.mqtt_broker)
        
        self.device.add_command(command)

        #self.announce_device()
        
        return command
            

    def run(self):
        # QUESTION: do we need a run?
        if not self.enabled:
            return
        if not self.last_run or time() - self.last_run > self.refresh_interval:
            log.info("APICoordinator running")
            self.announce_device()  # QUESTION: what are we announcing here?
            self.last_run = time()

    def initialize(self):
        if not self.enabled:
            return
        self.announce(self)

    def announce_device(self):
        device_dto = self.device.toDTO()
        if not self.enabled:
            return
        self.mqtt_broker.publish(self.announce_topic, device_dto.json())

    def announce(self, obj):
        if not self.enabled:
            return
        self.mqtt_broker.publish(self.announce_topic, obj)  # QUESTION: obj or obj.toDTO or obj.????

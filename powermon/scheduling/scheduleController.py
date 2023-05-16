import logging
from time import sleep, time

from powermon.device import Device
from powermon.dto.powermonDTO import PowermonDTO
from powermon.dto.scheduleDTO import ScheduleDTO
# from powermon.scheduling.schedules.loopSchedule import LoopSchedule
from powermon.libs.mqttbroker import MqttBroker
from powermon.scheduling.schedules.abstractSchedule import AbstractSchedule
# from powermon.scheduling.schedules.abstractSchedule import ScheduleType
from powermon.scheduling.schedules.onetimeSchedule import OneTimeSchedule

log = logging.getLogger("ScheduleController")


class ScheduleController:
    def __init__(self, name, schedules: list[AbstractSchedule], loop_duration: int, mqtt_broker: MqttBroker, device: Device):
        if not name:
            name = "default"
        self._name = name
        self._schedules = schedules
        self._loop_duration = loop_duration
        self.inDelay = False
        self.mqtt_broker = mqtt_broker
        self.device = device
        self.delayRemaining = loop_duration

    def __str__(self):
        return f"Schedule: {self._schedules}, loop duration: {self._loop_duration}"

    def toDTO(self) -> PowermonDTO:
        schedule_dtos = []
        for scheduledCommand in self._schedules:
            schedule_dtos.append(scheduledCommand.toDTO())
        log.debug(f"name={self._name}, loop_duration={self._loop_duration}, device={self.device.toDTO()}, schedules={schedule_dtos}")
        dto = PowermonDTO(name=self._name, loop_duration=self._loop_duration, device=self.device.toDTO(), schedules=schedule_dtos)
        return dto

    def addOneTimeCommandFromConfig(self, scheduleConfig):
        schedule = ScheduleDTO(scheduleConfig)
        command = self.parseCommandConfig(scheduleConfig["command"], self.mqtt_broker, self.device)
        self._schedules.append(OneTimeSchedule(schedule.name, {command}))

    # The hook for the port to connect before the main loops starts
    def beforeLoop(self):
        self.device.port.connect()

    def runLoop(self) -> bool:
        start_time = time()
        if self.inDelay is False:
            for scheduledCommand in self._schedules:
                if scheduledCommand.is_due():
                    scheduledCommand.runCommands()

        # Small pause to ....
        sleep(0.5)
        elapsed_time = time() - start_time
        self.delayRemaining = self.delayRemaining - elapsed_time
        if self.delayRemaining > 0 and not self.inDelay:
            log.debug(f"delaying for {self._loop_duration}sec, delayRemaining: {self.delayRemaining}")
            self.inDelay = True
        if self.delayRemaining < 0:
            log.debug(f"Next loop: {self._loop_duration}, {self.delayRemaining}")
            self.inDelay = False
            self.delayRemaining = self._loop_duration

        # If loopDuration is 0, then we only want to run once
        if self._loop_duration == 0:
            log.debug("loopDuration is once, returning False")
            return False
        else:
            return True

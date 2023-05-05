import logging
from time import sleep, time

from powermon.model.dto.powermonDTO import PowermonDTO
from powermon.model.dto.scheduleDTO import ScheduleDTO

from .commandSchedule import OneTimeCommandSchedule, LoopCommandSchedule, InformalScheduledCommandInterface, CommandScheduleType
from .mqttbroker import MqttBroker
from .device import Device
from .command import Command

log = logging.getLogger("ScheduleController")


class PowermonController:
    def __init__(self, name, scheduledCommands: list[InformalScheduledCommandInterface], loopDuration: int, mqtt_broker: MqttBroker, device: Device):
        self.name = name
        self.scheduledCommands = scheduledCommands
        self.loopDuration = loopDuration
        self.inDelay = False
        self.mqtt_broker = mqtt_broker
        self.device = device
        self.delayRemaining = loopDuration

    def __str__(self):
        return f"Schedule: {self.scheduledCommands}, {self.loopDuration}"
    
    def toDTO(self) -> PowermonDTO:
        commandSchedules = []
        for scheduledCommand in self.scheduledCommands:
            commandSchedules.append(scheduledCommand.toDTO())
        dto = PowermonDTO(name=self.name, loopDuration=self.loopDuration, device=self.device.toDTO(), schedulesCommands=commandSchedules)
        return dto

    
    def addOneTimeCommandFromConfig(self, scheduleConfig):
        schedule = ScheduleDTO(scheduleConfig)
        command = self.parseCommandConfig(scheduleConfig["command"], self.mqtt_broker, self.device)
        self.scheduledCommands.append(OneTimeCommandSchedule(schedule.name, {command}))


    #The hook for the port to connect before the main loops starts
    def beforeLoop(self):
        self.device.port.connect()
    
    def runLoop(self) -> bool:
        start_time = time()
        if(self.inDelay is False):
            for scheduledCommand in self.scheduledCommands:
                if scheduledCommand.is_due():
                    scheduledCommand.command.run()
                    
        # Small pause to ....
        sleep(0.5)
        elapsed_time = time() - start_time
        self.delayRemaining = self.delayRemaining - elapsed_time
        if self.delayRemaining > 0 and not self.inDelay:
            log.debug(f"delaying for {self.loopDuration}sec, delayRemaining: {self.delayRemaining}")
            self.inDelay = True
        if self.delayRemaining < 0:
            log.debug(f"Next loop: {self.loopDuration}, {self.delayRemaining}")
            self.inDelay = False
            self.delayRemaining = self.loopDuration

        #If loopDuration is 0, then we only want to run once
        if self.loopDuration == 0:
            log.debug("loopDuration is once, returning False")
            return False
        else:
            return True



    #TODO: this should follow the same pattern as the other parsers
    @classmethod
    def parseControllerConfig(cls, config, device, mqtt_broker):
        logging.debug("parseCoordinatorConfig")
        logging.debug(f"config: {config}")
        _name = config["name"]
        _loopDuration = config["loop"]
        if(_loopDuration == "once"):
            _loopDuration = 0

        _schedules = []
        for schedule in config["schedules"]:
            _scheduleType = schedule["type"]
            _scheduleName = schedule["name"]
            if _scheduleType == CommandScheduleType.LOOP:
                _loopCount = schedule["loopCount"]
            elif _scheduleType == CommandScheduleType.TIME:
                _runTime = schedule["runTime"]

            computed_topic = f"powermon/{_name}/results/{_scheduleName}/"

            command_config = schedule["command"]
            _command = (Command.parseCommandConfig(command_config,computed_topic, _scheduleName, mqtt_broker, device))
            
            if _scheduleType == CommandScheduleType.LOOP:
                _schedules.append(LoopCommandSchedule(_scheduleName, _loopCount, _command))
            elif _scheduleType == CommandScheduleType.ONCE:
                _schedules.append(OneTimeCommandSchedule(_scheduleName, _command))
            else:
                raise KeyError(f"Undefined schedule type: {_scheduleType}")

        schedule = PowermonController(_name, _schedules, _loopDuration, mqtt_broker, device)
        return schedule


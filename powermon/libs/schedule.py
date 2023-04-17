from enum import StrEnum, auto
from time import sleep, time
import yaml
import logging
from powermon.outputs import getOutputFromConfig

log = logging.getLogger("Schedule")

class Schedule:
    def __init__(self, scheduledCommands, loopDuration, mqtt_broker, device, adhocCommandsTopic=None):
        self.scheduledCommands = scheduledCommands
        self.loopDuration = loopDuration
        self.inDelay = False
        self.delayRemaining = loopDuration
        self.mqtt_broker = mqtt_broker
        self.device = device
        self.adhocCommandsTopic = adhocCommandsTopic

        if adhocCommandsTopic is not None:
            mqtt_broker.subscribe(adhocCommandsTopic, self.adhocCallback)

    def __str__(self):
        return f"Schedule: {self.scheduledCommands}, {self.loopDuration}, {self.adhocCommandsTopic}"
    
    def adhocCallback(self, client, userdata, msg):
        log.info(f"Received `{msg.payload}` on topic `{msg.topic}`")
        yamlString = msg.payload.decode("utf-8")
        log.debug(f"Yaml string: {yamlString}")
        try:
            _command_config = yaml.safe_load(yamlString)
        except yaml.YAMLError as exc:
            self.log.error(f"Error processing config file: {exc}")

        for command in _command_config["commands"]:
            self.log.debug(f"command: {command}")
            self.log.debug(f"self: {self}")
            self.addOneTimeCommandFromConfig(command)

    
    def addOneTimeCommandFromConfig(self, commandConfig):
        command = self.parseCommandConfig(commandConfig, self.mqtt_broker, self.device)
        self.scheduledCommands.append(OneTimeCommandSchedule(command))

    def beforeLoop(self):
        self.device.port.connect()
    
    def runLoop(self):
        log.debug("runloop")
        start_time = time()
        if(self.inDelay is False):
            for scheduledCommand in self.scheduledCommands:
                if scheduledCommand.is_due():
                    for command in scheduledCommand.commands:
                        command.run()
                    
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

    @classmethod
    def parseCommandConfig(cls, command, mqtt_broker, device):
        
        _command = command["command"]
        _commandType = command["type"]
        _outputs = []
        for outputConfig in command["outputs"]:
            logging.debug(f"command: {command}")
            _output = getOutputFromConfig(outputConfig,device, mqtt_broker)
            logging.debug(f"output: {_output}")
            _outputs.append(_output)

        return Command(_command, _commandType, _outputs, device.port)

    @classmethod
    def parseScheduleConfig(cls, config, device, mqtt_broker):
        logging.debug("parseScheduleConfig")
        _loopDuration = config["loop"]
        _adhocCommandsTopic = config["adhoc_command_topic"]

        _schedules = []
        for schedule in config["schedules"]:
            _scheduleType = schedule["type"]
            if _scheduleType == CommandScheduleType.LOOP:
                _loopCount = schedule["loopCount"]
            elif _scheduleType == CommandScheduleType.TIME:
                _runTime = schedule["runTime"]

            _commands = []
            for command in schedule["commands"]:
                _commands.append(cls.parseCommandConfig(command, mqtt_broker, device))
            
            if _scheduleType == CommandScheduleType.LOOP:
                _schedules.append(LoopCommandSchedule(_loopCount, _commands))
            else:
                raise KeyError(f"Undefined schedule type: {_scheduleType}")

        schedule = Schedule(_schedules, _loopDuration, mqtt_broker, device, _adhocCommandsTopic)
        return schedule


class CommandScheduleType(StrEnum):
    LOOP = auto()
    TIME = auto()
    ONCE = auto()

class InformalScheduledCommandInterface:
    def is_due(self):
        raise NotImplementedError

class LoopCommandSchedule(InformalScheduledCommandInterface):
    def __init__(self, loopCount, commands):
        self.scheduleType = CommandScheduleType.LOOP
        self.loopCount = loopCount
        self.commands = commands

        self.currentLoopCount = loopCount # Set to loopCount so that the first loop will run

    def __str__(self):
        return f"ScheduleType: {self.scheduleType}, LoopCount: {self.loopCount}, Commands: {self.commands}"

    def is_due(self):
        if self.currentLoopCount < self.loopCount:
            self.currentLoopCount += 1
            return False
        else:
            self.currentLoopCount = 1
            return True
        

class OneTimeCommandSchedule(InformalScheduledCommandInterface):
    def __init__(self, command):
        self.scheduleType = CommandScheduleType.ONCE
        self.commands = [command]
        self.has_run = False
    
    def __str__(self):
        return f"ScheduleType: {self.scheduleType}, Commands: {self.commands}"
    
    def is_due(self):
        if self.has_run:
            log.debug("One time command has already run")
            return False
        else:
            log.debug("One time command is due to run")
            self.has_run = True
            return True


class Command:
    def __init__(self, command, commandType, outputs, port):
        self.command = command
        self.commandType = commandType
        self.outputs = outputs
        self.port = port

    def __str__(self):
        return f"Command: {self.command}, CommandType: {self.commandType}, Outputs: {self.outputs}"
    
    def run(self):
        log.debug(f"Running command: {self.command}")
        results = self.port.process_command(command=self.command)
        for output in self.outputs:
            log.debug(f"Output: {output}")
            output.output(data=results)
    
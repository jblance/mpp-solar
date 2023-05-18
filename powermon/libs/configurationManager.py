import logging

from powermon.commands.abstractCommand import CommandType
from powermon.commands.pollCommand import PollCommand
from powermon.device import Device
from powermon.libs.mqttbroker import MqttBroker
from powermon.outputs import parseOutputConfig
from powermon.scheduling.scheduleController import ScheduleController
from powermon.scheduling.schedules.abstractSchedule import AbstractSchedule, ScheduleType
from powermon.scheduling.schedules.loopSchedule import LoopSchedule
from powermon.scheduling.schedules.onetimeSchedule import OneTimeSchedule

log = logging.getLogger("ConfigurationManager")


class ConfigurationManager:
    @staticmethod
    def parseSchedulesConfig(config) -> list[AbstractSchedule]:
        schedules = []
        schedule_config = config.get("schedules", None)
        log.debug("schedules: %s", schedule_config)
        if schedule_config is not None:
            for schedule in schedule_config:
                log.debug("schedule: %s", schedule)
                if schedule["type"] == ScheduleType.LOOP:
                    schedules.append(LoopSchedule(schedule["name"], schedule["loop_count"]))
                elif schedule["type"] == "once":
                    schedules.append(OneTimeSchedule(schedule["name"]))
                else:
                    raise Exception(f"Unknown schedule type: {schedule['type']}")
        return schedules

    @staticmethod
    def parseCommandConfig(command_config: dict, topic_prefix: str, mqtt_broker: MqttBroker, device: Device):
        _command_query = command_config.get("command_query")
        if not _command_query:
            log.info(f"No command_query for config: {command_config}")
            return None
        _commandType = command_config.get("type")
        _schedule_name = command_config.get("schedule_name")
        results_topic = topic_prefix + _schedule_name + "/results/" + _command_query

        _outputs = []
        for outputConfig in command_config.get("outputs"):
            _output = parseOutputConfig(outputConfig, results_topic, _schedule_name, device, mqtt_broker)
            logging.debug(f"output type: {_output}")
            _outputs.append(_output)

        _command = None
        if _commandType == CommandType.POLL:
            _command = PollCommand(
                _command_query,
                _commandType,
                _schedule_name,
                _outputs,
                device.get_port(),
            )

        return _command

    @staticmethod
    def parseControllerConfig(config: dict, device: Device, mqtt_broker: MqttBroker) -> ScheduleController:
        logging.debug("parseCoordinatorConfig")
        logging.debug(f"config: {config}")
        _name = config.get("name")
        _loopDuration = config.get("loop_duration", 0)
        if _loopDuration == "once":
            _loopDuration = 0

        _commands = []
        topic_prefix = f"powermon/{_name}/results/"
        for command_config in config.get("commands", {}):
            _commands.append(ConfigurationManager.parseCommandConfig(command_config, topic_prefix, mqtt_broker, device))

        _schedules = []
        for schedule in config.get("schedules", [{"type": "once"}]):
            _schedule_type = schedule.get("type")
            _schedule_name = schedule.get("name", "default")
            if _schedule_type == ScheduleType.LOOP:
                _loopCount = schedule["loop_count"]
            elif _schedule_type == ScheduleType.TIME:
                _runTime = schedule["runTime"]  # noqa: F841

            if _schedule_type == ScheduleType.LOOP:
                _schedule = LoopSchedule(_schedule_name, _loopCount)
            elif _schedule_type == ScheduleType.ONCE:
                _schedule = OneTimeSchedule(_schedule_name)
            else:
                raise KeyError(f"Undefined schedule type: {_schedule_type}")

            for command in _commands:
                if command and command.schedule_name == _schedule_name:
                    log.info("Adding command: %s" % command)
                    _schedule.add_command(command)

            _schedules.append(_schedule)

        controller = ScheduleController(_name, _schedules, _loopDuration, mqtt_broker, device)
        return controller

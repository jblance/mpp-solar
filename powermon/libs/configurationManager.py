import logging

from powermon.scheduling.scheduleController import ScheduleController
from powermon.scheduling.schedules.abstractSchedule import AbstractSchedule
from powermon.scheduling.schedules.abstractSchedule import ScheduleType
from powermon.scheduling.schedules.loopSchedule import LoopSchedule
from powermon.scheduling.schedules.onetimeSchedule import OneTimeSchedule
from powermon.commands.abstractCommand import CommandType
from powermon.commands.pollCommand import PollCommand

from powermon.libs.mqttbroker import MqttBroker

from powermon.formats.abstractformat import AbstractFormat
from powermon.formats.abstractformat import FormatterType

from powermon.outputs.abstractoutput import AbstractOutput
from powermon.outputs.abstractoutput import OutputType

from powermon.device import Device


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
    def getFormatfromConfig(formatConfig, device, topic) -> AbstractFormat:
        # Get values from config
        # Type is required
        formatType = formatConfig["type"]

        formatter = None
        if formatType == FormatterType.HTMLTABLE:
            from powermon.formats.htmltable import htmltable

            formatter = htmltable(formatConfig)
        elif formatType == FormatterType.HASS:
            from powermon.formats.hass import hass

            formatter = hass(formatConfig, device)
        elif formatType == FormatterType.TOPICS:
            from powermon.formats.topics import Topics

            formatter = Topics(formatConfig, topic)
        elif formatType == FormatterType.SIMPLE:
            from powermon.formats.simple import simple

            formatter = simple(formatConfig)
        elif formatType == FormatterType.TABLE:
            from powermon.formats.table import table

            formatter = table(formatConfig)

        else:
            log.warning("No formatter found for: %s" % formatType)
            formatter = None

        return formatter

    @staticmethod
    def parseOutputConfig(
        outputConfig: dict,
        topic: str,
        schedule_name: str,
        device: Device,
        mqtt_broker: MqttBroker,
    ) -> AbstractOutput:
        outputType = outputConfig["type"]

        formatConfig = outputConfig["format"]
        topic_override = outputConfig.get("topic_override", None)
        # use topic override from the config
        if topic_override is not None:
            topic = topic_override

        format = ConfigurationManager.getFormatfromConfig(formatConfig, device, topic)

        output_class = None
        # Only import the required class
        if outputType == OutputType.SCREEN:
            from powermon.outputs.screen import Screen

            output_class = Screen(outputConfig, format)
        elif outputType == OutputType.MQTT:
            from powermon.outputs.mqtt import MQTT

            output_class = MQTT(outputConfig, topic, mqtt_broker, format)
        elif outputType == OutputType.API_MQTT:
            from powermon.outputs.api_mqtt import API_MQTT

            output_class = API_MQTT(outputConfig, topic, schedule_name, mqtt_broker, format)

        return output_class

    @staticmethod
    def parseCommandConfig(command_config: dict, topic_prefix: str, mqtt_broker: MqttBroker, device: Device):
        _command_query = command_config["command_query"]
        _commandType = command_config["type"]
        _schedule_name = command_config["schedule_name"]
        results_topic = topic_prefix + _schedule_name + "/results/" + _command_query

        _outputs = []
        for outputConfig in command_config["outputs"]:
            _output = ConfigurationManager.parseOutputConfig(outputConfig, results_topic, _schedule_name, device, mqtt_broker)
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
        _loopDuration = config.get("loop_duration", 60)
        if _loopDuration == "once":
            _loopDuration = 0

        _commands = []
        topic_prefix = f"powermon/{_name}/results/"
        for command_config in config["commands"]:
            _commands.append(ConfigurationManager.parseCommandConfig(command_config, topic_prefix, mqtt_broker, device))

        _schedules = []
        for schedule in config["schedules"]:
            _schedule_type = schedule["type"]
            _schedule_name = schedule["name"]
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
                if command.schedule_name == _schedule_name:
                    log.info("Adding command: %s" % command)
                    _schedule.add_command(command)

            _schedules.append(_schedule)

        controller = ScheduleController(_name, _schedules, _loopDuration, mqtt_broker, device)
        return controller

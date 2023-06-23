import logging
from time import localtime, strftime, time
from powermon.commands.trigger import Trigger
from powermon.outputs import getOutputs

log = logging.getLogger("Command")


class Command:
    def __str__(self):
        if self.name is None:
            return "empty command object"
        if self.last_run is None:
            last_run = "Not yet run"
        else:
            last_run = strftime("%d %b %Y %H:%M:%S", localtime(self.last_run))
        if self.next_run is None:
            next_run = "unknown"
        else:
            next_run = strftime("%d %b %Y %H:%M:%S", localtime(self.next_run))

        _outs = ""
        for output in self.outputs:
            _outs += str(output)

        return f"Command: {self.name=} {self.full_command=}, {self.type=}, [{_outs=}], {last_run=}, {next_run=}, {str(self.trigger)}, {self.command_defn=}"

    @classmethod
    def fromConfig(cls, config=None):
        # need to have a config defined
        # minimum is
        # - command: QPI
        if not config:
            log.warning("Invalid command config")
            raise TypeError("Invalid command config")
            # return None

        name = config.get("command")
        if name is None:
            log.info("command must be defined")
            raise TypeError("command must be defined")
        commandtype = config.get("type", "basic")
        outputs = getOutputs(config.get("outputs", ""))
        trigger = Trigger.fromConfig(config=config.get("trigger"))
        return cls(name=name, commandtype=commandtype, outputs=outputs, trigger=trigger)

    def __init__(self, name : str, commandtype: str, outputs: list, trigger : Trigger):

        self.name = name
        self.type = commandtype
        self.outputs = outputs
        self.trigger = trigger

        self.last_run = None
        self.next_run = self.trigger.nextRun(command=self)
        self.full_command = None
        self.command_defn = None
        log.debug(self)

    def dueToRun(self):
        return self.trigger.isDue(command=self)

    def touch(self):
        # store run time (as secs since epoch)
        self.last_run = time()
        # update next run time
        self.next_run = self.trigger.nextRun(command=self)

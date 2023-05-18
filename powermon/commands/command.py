import logging
from time import localtime, time, strftime
from powermon.commands.trigger import Trigger
from powermon.outputs import getOutputs

log = logging.getLogger("Command")


class Command:
    def __str__(self):
        if self.command is None:
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

        return f"Command: {self.command}, type: {self.type}, outputs: [{_outs}] last run: {last_run}, next run: {next_run}, {self.trigger}"

    def __init__(self, config):
        # need to have a config defined
        # minimum is
        # - command: QPI

        if not config:
            log.warning("Invalid command config")
            raise TypeError("Invalid command config")
            # return None

        self.command = config.get("command")
        if self.command is None:
            log.info("command must be defined")
            raise TypeError("command must be defined")
        self.type = config.get("type", "basic")
        self.outputs = getOutputs(config.get("outputs", ""))
        self.last_run = None
        self.trigger = Trigger(config=config.get("trigger"))
        self.next_run = self.trigger.nextRun(command=self)
        log.debug(self)

    def dueToRun(self):
        return self.trigger.isDue(command=self)

    def run(self, device):
        # store run time (as secs since epoch)
        self.last_run = time()
        # update next run time
        self.next_run = self.trigger.nextRun(command=self)
        # print(f"TODO: running command {self}")
        results = device.port.process_command(command=self.command)
        for output in self.outputs:
            log.debug(f"Using Output: {output}")
            output.output(data=results)

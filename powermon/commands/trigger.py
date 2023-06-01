import logging
import time
import datetime
from strenum import LowercaseStrEnum
from enum import auto


log = logging.getLogger("Trigger")


class TriggerType(LowercaseStrEnum):
    EVERY = auto()
    LOOPS = auto()
    AT = auto()
    DISABLED = auto()


class Trigger:
    def __str__(self):
        return f"trigger: {self.trigger} {self.value} loops togo: {self.togo}"

    @classmethod
    def fromConfig(cls, config=None):
        if not config:
            # no trigger defined, default to every 60 seconds
            trigger = TriggerType.EVERY
            value = 60
        elif TriggerType.EVERY in config:
            trigger = TriggerType.EVERY
            value = config.get(TriggerType.EVERY, 61)
        elif TriggerType.LOOPS in config:
            trigger = TriggerType.LOOPS
            value = config.get(TriggerType.LOOPS, 101)
        elif TriggerType.AT in config:
            trigger = TriggerType.AT
            value = config.get(TriggerType.AT, "12:01")
        else:
            trigger = TriggerType.DISABLED
            value = None
        return cls(trigger=trigger, value=value)

    def __init__(self, trigger, value=None):
        self.trigger = trigger
        self.value = value
        self.togo = 0

    def isDue(self, command):
        # Store the time now
        now = time.time()
        if self.trigger == TriggerType.DISABLED:
            return False
        elif self.trigger == TriggerType.EVERY:
            if command.last_run is None:
                return True  # if hasnt run, run now
            if command.next_run <= now:
                return True
            return False
        elif self.trigger == TriggerType.LOOPS:
            if self.togo <= 0:
                self.togo = self.value
                return True
            else:
                self.togo -= 1
                return False
        elif self.trigger == TriggerType.AT:
            if command.next_run is None:
                log.warn("at type trigger failed to set next run for %s" % command)
                return False
            if command.next_run <= now:
                return True
            return False
        log.warn("no isDue set for %s" % command)
        return False

    def nextRun(self, command):
        if self.trigger == TriggerType.EVERY:
            # triggers every xx seconds
            # if hasnt run, run now
            if command.last_run is None:
                return time.time()
            return command.last_run + self.value
        elif self.trigger == TriggerType.AT:
            # triggers at specific time each day
            dt_today = datetime.datetime.now()
            dt_now = dt_today.time()
            at_time = datetime.time.fromisoformat(self.value)
            if dt_now < at_time:
                # needs to run today at at_time
                next_run = dt_today.replace(hour=at_time.hour, minute=at_time.minute, second=at_time.second, microsecond=0).timestamp()
            else:
                # needs to run tomorrow at at_time
                next_run = (dt_today.replace(hour=at_time.hour, minute=at_time.minute, second=at_time.second, microsecond=0) + datetime.timedelta(days=1)).timestamp()
            return next_run
        else:
            return None

""" commands / trigger/py """
import datetime
import logging
import time
from enum import auto

from strenum import LowercaseStrEnum

from powermon.dto.triggerDTO import TriggerDTO

log = logging.getLogger("Trigger")


class TriggerType(LowercaseStrEnum):
    """ enum of valid types of triggers """
    EVERY = auto()
    LOOPS = auto()
    AT = auto()
    ONCE = auto()
    DISABLED = auto()


class Trigger:
    """ the trigger class """
    DATE_FORMAT = "%d %b %Y %H:%M:%S"

    def __init__(self, trigger_type, value=None):
        self.trigger_type = trigger_type
        self.value = value
        self.togo = 0
        self.last_run : float | None = None
        self.next_run : float = self.determine_next_run()

    def __str__(self):
        return f"trigger: {self.trigger_type} {self.value} loops togo: {self.togo}"

    @classmethod
    def from_config(cls, config=None):
        """ build trigger object from config dict """
        if not config:
            # no trigger defined, default to every 60 seconds
            trigger_type = TriggerType.EVERY
            value = 60
        elif TriggerType.EVERY in config:
            trigger_type = TriggerType.EVERY
            value = config.get(TriggerType.EVERY, 61)
        elif TriggerType.LOOPS in config:
            trigger_type = TriggerType.LOOPS
            value = config.get(TriggerType.LOOPS, 101)
        elif TriggerType.AT in config:
            trigger_type = TriggerType.AT
            value = config.get(TriggerType.AT, "12:01")
        elif TriggerType.ONCE in config:
            trigger_type = TriggerType.ONCE
            value = config.get(TriggerType.ONCE, 0)
        else:
            trigger_type = TriggerType.DISABLED
            value = None
        return cls(trigger_type=trigger_type, value=value)

    @classmethod
    def from_dto(cls, dto: TriggerDTO) -> "Trigger":
        return cls(trigger_type=dto.trigger_type, value=dto.value)    

    def touch(self):
        """ update last and next run times """
        # store run time (as secs since epoch)
        self.last_run = time.time()
        # update next run time
        self.next_run = self.determine_next_run()

    def get_last_run(self) -> str:
        last_run_str = "Not yet run"
        if self.last_run is not None:
            last_run_str = time.strftime(Trigger.DATE_FORMAT, time.localtime(self.last_run))
        return last_run_str

    def get_next_run(self) -> str:
        next_run_str = "unknown"
        if self.next_run is not None:
            next_run_str = time.strftime(Trigger.DATE_FORMAT, time.localtime(self.next_run))
        return next_run_str

    def is_due(self) -> bool:
        # Store the time now
        now = time.time()
        if self.trigger_type == TriggerType.DISABLED:
            return False
        elif self.trigger_type == TriggerType.EVERY:
            if self.last_run is None:
                return True  # if hasnt run, run now
            if self.next_run <= now:
                return True
            return False
        elif self.trigger_type == TriggerType.LOOPS:
            if self.togo <= 0:
                self.togo = self.value
                return True
            else:
                self.togo -= 1
                return False
        elif self.trigger_type == TriggerType.AT:
            if self.next_run is None:
                #log.warning("at type trigger failed to set next run for %s" % command)
                return False
            if self.next_run <= now:
                return True
            return False
        elif self.trigger_type == TriggerType.ONCE:
            if int(self.value) == 0:
                self.value = 1
                return True
            else:
                return False
        #log.warning("no isDue set for %s" % command)
        return False

    def determine_next_run(self) -> float:
        #TODO: split this into a function per trigger type
        if self.trigger_type == TriggerType.EVERY:
            # triggers every xx seconds
            # if hasnt run, run now
            if self.last_run is None:
                self.next_run = time.time()
            else:
                self.next_run = self.last_run + self.value
        elif self.trigger_type == TriggerType.AT:
            # triggers at specific time each day
            dt_today = datetime.datetime.now()
            dt_now = dt_today.time()
            at_time = datetime.time.fromisoformat(self.value)
            if dt_now < at_time:
                # needs to run today at at_time
                self.next_run = dt_today.replace(hour=at_time.hour, minute=at_time.minute, second=at_time.second, microsecond=0).timestamp()
            else:
                # needs to run tomorrow at at_time
                self.next_run = (dt_today.replace(hour=at_time.hour, minute=at_time.minute, second=at_time.second, microsecond=0) + datetime.timedelta(days=1)).timestamp()
        else:
            self.next_run = None
        return self.next_run

    def to_dto(self):
        return TriggerDTO(
            trigger_type=self.trigger_type,
            value=self.value
        )

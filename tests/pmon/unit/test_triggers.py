import unittest
from unittest import mock
import datetime
import time
from powermon.commands.trigger import Trigger, TriggerType

class test_triggers(unittest.TestCase):
    
    def test_triggertype_every(self):
        """Test that the EVERY trigger will trigger every x seconds"""
        x=1
        trigger = Trigger(trigger_type=TriggerType.EVERY, value=x)
        
        #Check that the initial state is correct
        now = time.time()
        now_str = time.strftime(Trigger.DATE_FORMAT, time.localtime(now))
        self.assertEqual(trigger.get_last_run(), "Not yet run")
        self.assertEqual(trigger.get_next_run(), now_str)
        self.assertEqual(trigger.is_due(), True)
        
        #Check that the state after first run is correct
        trigger.touch()
        now = time.time()
        now_str = time.strftime(Trigger.DATE_FORMAT, time.localtime(now))
        next_str = time.strftime(Trigger.DATE_FORMAT, time.localtime(now + x))
        self.assertEqual(trigger.is_due(), False)
        self.assertEqual(trigger.get_last_run(), now_str)
        self.assertEqual(trigger.get_next_run(), next_str)
        
        #Check the trigger comes due when the next run time is reached
        time.sleep(x) #replace with a mock
        self.assertEqual(trigger.is_due(), True)
        
    def test_triggertype_loops(self):
        """Test that the loops trigger works after the correct number of is_due() calls"""
        trigger = Trigger(trigger_type=TriggerType.LOOPS, value=2)
        now = time.time()
        #Check that the initial state is correct
        self.assertEqual(trigger.get_last_run(), "Not yet run")
        self.assertEqual(trigger.get_next_run(), "unknown")
        self.assertEqual(trigger.is_due(), True)
        
        #check that the state after first run is correct
        trigger.touch()
        now = time.time()
        now_str = time.strftime(Trigger.DATE_FORMAT, time.localtime(now))
        self.assertEqual(trigger.is_due(), False)
        self.assertEqual(trigger.get_last_run(), now_str)
        self.assertEqual(trigger.get_next_run(), "unknown")
        
        #Check that the trigger comes due when the loop criteria is met
        self.assertEqual(trigger.is_due(), False)
        self.assertEqual(trigger.is_due(), True)
        
    def test_triggertype_at(self):
        """Test that the AT trigger goes off when the correct time of day passes"""
        dt_today = datetime.datetime.now()
        x=1
        hour=dt_today.hour
        minute=dt_today.minute
        second=dt_today.second + x
        time_str = str(hour).rjust(2, '0') + ":" + str(minute).rjust(2, '0') + ":" + str(second).rjust(2, '0') #probably a better way to get an isoformat string
        trigger = Trigger(trigger_type=TriggerType.AT, value=time_str)
        #Check that the initial state is correct
        now = time.time()
        next_str = time.strftime(Trigger.DATE_FORMAT, time.localtime(now + x))
        self.assertEqual(trigger.get_last_run(), "Not yet run")
        self.assertEqual(trigger.get_next_run(), next_str)
        self.assertEqual(trigger.is_due(), False)
        
        #check that the trigger comes due when the correct time is reached
        time.sleep(x) #replace with a mock
        self.assertEqual(trigger.is_due(), True)
        
        #check that the state after first run is correct and the next run is the next day
        trigger.touch()
        now = time.time()
        now_str = time.strftime(Trigger.DATE_FORMAT, time.localtime(now))
        next_str = time.strftime(Trigger.DATE_FORMAT, time.localtime(now + 86400))
        self.assertEqual(trigger.is_due(), False)
        self.assertEqual(trigger.get_last_run(), now_str)
        self.assertEqual(trigger.get_next_run(), next_str)

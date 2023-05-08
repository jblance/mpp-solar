
import asyncio
import json
from .db.models import MQTTMessage
from powermon.dto.powermonDTO import PowermonDTO
from powermon.dto.resultDTO import ResultDTO

class MQTTHandler(object):
    _instance = None
    _power_monitors = []
    _results = []
    _commandDictionary = {
            "mqtt/QPIGS": "QPIGS",
        }
    _commandRequests = {}
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance
    

    async def register_command(self, command):
        print("Registering command: ", command)
        request = CommandRequest(command)
        if(command not in self._commandRequests):
            self._commandRequests[command] = []

        self._commandRequests[command].append(request)

        while True:
            requests = self._commandRequests[command]
            for request in requests:
                if(request.done):
                    print("Command done: ", command)
                    result = request.result
                    self._commandRequests[command].remove(request)
                    return result
            await asyncio.sleep(1)
    
    def recieved_result(self, result: ResultDTO):
        # command = self._commandDictionary.get(mqtt_message.topic, None)
        # print("Command Recieved: ", command, self._commandRequests)
        # if(command is None or command not in self._commandRequests):
        #     print("Command not registered: ", command)
        #     return

        self._results.append(result)

    def recieved_announcement(self, message):
        print("Announcement Recieved: ", message)
        schedule = PowermonDTO.parse_raw(message)
        deviceId = schedule.device.identifier
        print("Device ID: ", deviceId)
        if(schedule not in self._power_monitors):
            self._power_monitors.append(schedule)

    async def get_powermon_instances(self):
        return self._power_monitors
    
    async def get_powermon_instance(self, powermon_name) -> PowermonDTO:
        for powermon in self._power_monitors:
            if(powermon.name == powermon_name):
                return powermon
        return None
    
    async def get_results(self):
        return self._results

    
class CommandRequest:
    def __init__(self, command):
        self.command = command
        self.result = None
        self.done = False
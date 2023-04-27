
import asyncio
from .db.models import MQTTMessage

class MQTTHandler(object):
    _instance = None
    _devices = []
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
    
    def recieved_message(self, mqtt_message):
        command = self._commandDictionary.get(mqtt_message.topic, None)
        print("Command Recieved: ", command, self._commandRequests)
        if(command is None or command not in self._commandRequests):
            print("Command not registered: ", command)
            return

        for request in self._commandRequests[command]:
            request.result = mqtt_message
            request.done = True

    def recieved_announcement(self, message):
        print("Announcement Recieved: ", message)
        self._devices.append(message)

    def get_devices(self):
        return self._devices

    
class CommandRequest:
    def __init__(self, command):
        self.command = command
        self.result = None
        self.done = False
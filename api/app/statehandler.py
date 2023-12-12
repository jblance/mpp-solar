
import asyncio

from powermon.dto.deviceDTO import DeviceDTO
from powermon.dto.resultDTO import ResultDTO

class StateHandler(object):
    _instance = None
    _devices : dict[str,DeviceDTO] = {}
    _results : list[ResultDTO] = []
    _topics_waiting_for_result : dict[str, ResultDTO | None] = {}
    
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance
    

    
    def recieved_result(self, topic: str, payload: bytes):
        
        print(f"Recieved result for {topic}")
        if self.is_command_result_topic(topic):
            result = ResultDTO.parse_raw(payload.decode())
            
            self._results.append(result)
            if topic in self._topics_waiting_for_result:
                self._topics_waiting_for_result[topic] = result
        
    async def get_next_result(self, topic: str) -> ResultDTO | None:
        print(f"Waiting for result for {topic}")
        print(self._topics_waiting_for_result)
        self._topics_waiting_for_result[topic] = None
        while True:
            if topic in self._topics_waiting_for_result:
                if self._topics_waiting_for_result[topic] is not None:
                    result = self._topics_waiting_for_result[topic]
                    del self._topics_waiting_for_result[topic]
                    return result
            else:
                raise RuntimeError("Topic not found in waiting for result list")
            print(f"Still waiting for result on {topic}")
            await asyncio.sleep(0.5)

    def is_command_result_topic(self, topic: str) -> bool:
        return "result" in topic

    def recieved_announcement(self, message) -> DeviceDTO:
        device = DeviceDTO.parse_raw(message)
        deviceId : str = device.device_id 
        self._devices[deviceId] = device
        return device


    def get_device_instances(self) -> list[DeviceDTO]:
        return list(self._devices.values())

    def get_device_instance(self, device_id) -> DeviceDTO | None:
        device = self._devices.get(device_id)
        return device

    async def get_results(self):
        return self._results


class CommandRequest:
    def __init__(self, command):
        self.command = command
        self.result = None
        self.done = False
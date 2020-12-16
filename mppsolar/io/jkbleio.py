import logging


from .baseio import BaseIO

log = logging.getLogger("MPP-Solar")


class JkBleIO(BaseIO):
    def __init__(self, device_path) -> None:
        self._device = device_path
        self._test_data = b"(230.0 50.0 0030 42.0 54.0 56.4 46.0 60 0 0 2 0 0 0 0 0 1 1 0 0 1 0 54.0 0 1 000\x9E\x60\r"

    def send_and_receive(self, command, show_raw, protocol) -> dict:
        full_command = protocol.get_full_command(command)
        log.info(f"full command {full_command} for command {command}")
        # Send the full command via the communications port
        command_defn = protocol.get_command_defn(command)
        if command_defn is not None:
            self._test_data = command_defn["test_responses"][
                random.randrange(len(command_defn["test_responses"]))
            ]
        response = self._test_data
        # response = b"(PI30\x9a\x0b\r"
        log.debug(f"Raw response {response}")
        decoded_response = protocol.decode(response, show_raw)
        # _response = response.decode('utf-8')
        log.debug(f"Decoded response {decoded_response}")
        # add command name and description to response
        decoded_response["_command"] = command
        if command_defn is not None:
            decoded_response["_command_description"] = command_defn["description"]
        log.info(f"Decoded response {decoded_response}")
        return decoded_response


#
# jk = jkBMS(
#     name=name,
#     model=model,
#     mac=mac,
#     command=command,
#     tag=tag,
#     format=format,
#     records=args.records,
#     maxConnectionAttempts=max_connection_attempts,
#     mqttBroker=mqtt_broker,
# )
# log.debug(str(jk))
# if jk.connect():
#     jk.getBLEData()
#     jk.disconnect()
# else:
#     print("Failed to connect to {} {}".format(name, mac))

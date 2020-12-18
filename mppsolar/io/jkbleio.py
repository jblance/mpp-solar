import logging


from .baseio import BaseIO

log = logging.getLogger("MPP-Solar")


class JkBleIO(BaseIO):
    def __init__(self, device_path) -> None:
        self._device = device_path
        self._test_data = bytes.fromhex(
            "55aaeb9002ff5b566240e34e62406e6a62404a506240acd7624011d26240bddd62409ad1624044c86240cedc6240ccc7624079e1624057dc624073a262405f80624088c46240000000000000000000000000000000000000000000000000000000000000000013315c3d0636143d26e0113d8021f03c1153363d8980123d7e7c033dac41233d1ad83c3d9d6f4f3d8eb51e3d6a2c293deb28653d189c523da3724e3deb94493d9ab2c23d00000000000000000000000000000000000000000000000000000000000000001aad62400084053c00000000ffff00000b000000000000000000000000000036a3554c40000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000be0b54001456a43fb876a43f00a2"
        )

    def send_and_receive(self, command, show_raw, protocol) -> dict:
        full_command = protocol.get_full_command(command)
        log.info(f"full command {full_command} for command {command}")
        # Send the full command via the communications port
        command_defn = protocol.get_command_defn(command)
        # Need to get response here
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

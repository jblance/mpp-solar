import logging

from .protocol import AbstractProtocol
from .protocol_helpers import decode4ByteHex, crc8


log = logging.getLogger("MPP-Solar")

# >>> print(f'{151:#04x}')
# 0x97
# >>> print(f'{1:#04x}')
# 0x01
# >>> print(f'{1:#02x}')
# 0x1
# >>> print(f'{1:#04x}')
# 0x01
# >>> bytes.fromhex('aa5590eb')
# b'\xaaU\x90\xeb'
# getInfo = b'\xaa\x55\x90\xeb\x97\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11'
# getCellInfo = b'\xaa\x55\x90\xeb\x96\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10'
# message after 9003
# aa5590ebc8010100000000000000000000000044
# 55aaeb90
# 02 record type
# b5 counter

COMMANDS = {
    "getInfo": {
        "name": "getInfo",
        "command_code": "97",
        "description": "BLE Device Information inquiry",
        "help": " -- queries the ble device information",
        "type": "QUERY",
        "response": [
            ["hex", 4, "Header", ""],
            ["hex", 1, "Record Type", ""],
            ["int", 1, "Record Counter", ""],
            ["asc", 10, "Device Model", ""],
            ["asc", 10, "Hardware Version", ""],
            ["asc", 10, "Software Version", ""],
            ["rem"],
        ],
        "test_responses": [
            bytes.fromhex(
                "55aaeb9003f14a4b2d42324132345300000000000000332e300000000000332e322e330000000876450004000000506f7765722057616c6c203100000000313233340000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c2"
            ),
        ],
        "regex": "",
    },
}


class jk04(AbstractProtocol):
    """
    JK04 - Handler for JKBMS 4 byte data communication
         - e.g. ASASASAS = ??V
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"JK04"
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = [
            "",
        ]
        self.SETTINGS_COMMANDS = [
            "getInfo",
        ]
        self.DEFAULT_COMMAND = "getInfo"

    def get_full_command(self, command) -> bytes:
        """
        Override the default get_full_command as its different for JK04
        # getInfo = b'\xaa\x55\x90\xeb\x97\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11'
        """
        log.info(f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands")
        # These need to be set to allow other functions to work`
        self._command = command
        self._command_defn = self.get_command_defn(command)
        # End of required variables setting
        if self._command_defn is None:
            # Maybe returna default here?
            return None
        if "command_code" in self._command_defn:
            # full command is 20 bytes long
            cmd = bytearray(20)
            # starts with \xaa\x55\x90\xeb
            cmd[0:4] = bytes.fromhex("aa5590eb")
            log.debug(f"cmd with SOR: {cmd}")
            # then has command code
            cmd[4] = int(self._command_defn["command_code"], 16)
            log.debug(f"cmd with command code: {cmd}")
            cmd[-1] = crc8(cmd)
            log.debug(f"cmd with crc: {cmd}")
            return cmd
        return None

    def get_responses(self, response):
        """
        Override the default get_responses as its different for JK04
        """
        # responses = response.split(b" ")
        # Trim leading '(' of first response
        # responses[0] = responses[0][1:]
        # Remove CRC and \r of last response
        # responses[-1] = responses[-1][:-3]
        return bytearray(response)

    def decode(self, response, show_raw) -> dict:
        msgs = {}
        log.info(f"response passed to decode: {response}")
        # No response
        if response is None:
            log.info("No response")
            msgs["ERROR"] = ["No response", ""]
            return msgs

        # Raw response requested
        if show_raw:
            log.debug(f'Protocol "{self._protocol_id}" raw response requested')
            # TODO: deal with \x09 type crc response items better
            _response = b""
            for item in response:
                _response += chr(item).encode()
            raw_response = _response.decode("utf-8")
            msgs["raw_response"] = [raw_response, ""]
            return msgs

        # Check for a stored command definition
        if not self._command_defn:
            # No definiution, so just return the data
            len_command_defn = 0
            log.debug(f"No definition for command {self._command}, raw response returned")
            msgs["ERROR"] = [
                f"No definition for command {self._command} in protocol {self._protocol_id}",
                "",
            ]
        else:
            len_command_defn = len(self._command_defn["response"])
            # Decode response based on stored command definition
            responses = self.get_responses(response)
            log.debug(f"trimmed and split responses: {responses}")
            print(f"Length of responses {len(responses)}")

            for defn in self._command_defn["response"]:
                print(f"defn {defn}")
                # ["hex", 4, "Header", ""]
                if defn[0] == "hex":
                    value = ""
                    for x in range(defn[1]):
                        value += f"{responses.pop(0):02x}"
                    msgs[defn[2]] = [value, ""]
                elif defn[0] == "asc":
                    value = ""
                    for x in range(defn[1]):
                        b = responses.pop(0)
                        if b == 0:
                            continue
                        value += f"{b:c}"
                        print(f"value: {value}")
                    msgs[defn[2]] = [value, ""]
                elif defn[0] == "int":
                    msgs[defn[2]] = [responses.pop(0), ""]
                else:
                    msgs["remainder"] = [str(responses), ""]
                    msgs["len remainder"] = [len(responses), ""]
                    # log.error("undefined type")
            # for i, result in enumerate(responses):
            #     # decode result
            #     result = result.decode("utf-8")
            #     # Check if we are past the 'known' responses
            #     if i >= len_command_defn:
            #         resp_format = ["string", f"Unknown value in response {i}", ""]
            #     else:
            #         resp_format = self._command_defn["response"][i]
            #
            #     key = "{}".format(resp_format[1]).lower().replace(" ", "_")
            #     # log.debug(f'result {result}, key {key}, resp_format {resp_format}')
            #     # Process results
            #     if resp_format[0] == "float":
            #         if "--" in result:
            #             result = 0
            #         msgs[key] = [float(result), resp_format[2]]
            print(msgs)
        return msgs

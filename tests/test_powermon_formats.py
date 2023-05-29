import subprocess
import unittest
# import json


class test_powermon_formats(unittest.TestCase):
    maxDiff = 9999

    def test_format_hass(self):
        print("test_format_hass todo")  # TODO: implement
        # return
        try:
            expected = ""
            result = subprocess.run(
                ["powermon", "--once", "--config", '{"device": {"port":{"type":"test"}}, "commands": [{"command":"QPI", "outputs": [{"type": "screen", "format": "hass"}]}]} '],
                check=True,
                capture_output=True,
                text=True,
            )
            print(result.stdout)
            return
            self.assertEqual(result.stdout, expected)
            self.assertEqual(result.returncode, 0)
        except subprocess.CalledProcessError as error:
            print(error.stdout)
            print(error.stderr)
            raise error

    def test_format_htmltable(self):
        try:
            expected = """<table><tr><th>Parameter</th><th>Value</th><th>Unit</th></tr>
<tr><td>protocol_id</td><td>PI30</td><td></td></tr>
</table>\n"""
            result = subprocess.run(
                ["powermon", "--once", "--config", '{"device": {"port":{"type":"test"}}, "commands": [{"command":"QPI", "outputs": [{"type": "screen", "format": "htmltable"}]}]} '],
                check=True,
                capture_output=True,
                text=True,
            )
            # print(result.stdout)
            self.assertEqual(result.stdout, expected)
            self.assertEqual(result.returncode, 0)
        except subprocess.CalledProcessError as error:
            print(error.stdout)
            print(error.stderr)
            raise error

    def test_format_raw(self):
        try:
            expected = "b'(PI30\\x9a\\x0b\\r'\n"
            result = subprocess.run(
                ["powermon", "--once", "--config", '{"device": {"port":{"type":"test"}}, "commands": [{"command":"QPI", "outputs": [{"type": "screen", "format": "raw"}]}]} '],
                check=True,
                capture_output=True,
                text=True,
            )
            # print(result.stdout)
            self.assertEqual(result.stdout, expected)
            self.assertEqual(result.returncode, 0)
        except subprocess.CalledProcessError as error:
            print(error.stdout)
            print(error.stderr)
            raise error

    def test_format_simple(self):
        try:
            expected = "protocol_id=PI30\n"
            result = subprocess.run(
                ["powermon", "--once", "--config", '{"device": {"port":{"type":"test"}}, "commands": [{"command":"QPI", "outputs": [{"type": "screen", "format": "simple"}]}]} '],
                check=True,
                capture_output=True,
                text=True,
            )
            # print(result.stdout)
            self.assertEqual(result.stdout, expected)
            self.assertEqual(result.returncode, 0)
        except subprocess.CalledProcessError as error:
            print(error.stdout)
            print(error.stderr)
            raise error

    def test_format_table(self):
        try:
            expected = """Command: QPI - Protocol ID inquiry
-----------------------
Parameter    Value Unit
protocol_id PI30                
"""
            result = subprocess.run(
                ["powermon", "--once", "--config", '{"device": {"port":{"type":"test"}}, "commands": [{"command":"QPI", "outputs": [{"type": "screen", "format": "table"}]}]} '],
                check=True,
                capture_output=True,
                text=True,
            )
            # print(result.stdout)
            self.assertEqual(result.stdout, expected)
            self.assertEqual(result.returncode, 0)
        except subprocess.CalledProcessError as error:
            print(error.stdout)
            print(error.stderr)
            raise error

    def test_format_topics(self):
        print("test_format_topics todo")  # TODO: implement
        return
        try:
            expected = """Command: QPI - Protocol ID inquiry
-----------------------
Parameter    Value Unit
protocol_id PI30                
"""
            result = subprocess.run(
                ["powermon", "--once", "--config", '{"device": {"port":{"type":"test"}}, "commands": [{"command":"QPI", "outputs": [{"type": "screen", "format": "topics"}]}]} '],
                check=True,
                capture_output=True,
                text=True,
            )
            print(result.stdout)
            return
            self.assertEqual(result.stdout, expected)
            self.assertEqual(result.returncode, 0)
        except subprocess.CalledProcessError as error:
            print(error.stdout)
            print(error.stderr)
            raise error

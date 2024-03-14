import importlib
import unittest
from pathlib import Path

HERE = Path(__file__).parent
PROTOCOLS_DIR = HERE.parent.parent / "mppsolar" / "protocols"
PROTOCOLS = sorted(
    file.stem for file in PROTOCOLS_DIR.glob("*.py")
    if "init" not in file.stem
    and "abstract" not in file.stem
    and "protocol" not in file.stem
)


class testProtocols(unittest.TestCase):

    def test_protocols_count(self):
        # print(len(PROTOCOLS))
        assert len(PROTOCOLS) == 24, len(PROTOCOLS)

    def test_protocols_init(self):
        for protocol in PROTOCOLS:
            module_cls = importlib.import_module(f"mppsolar.protocols.{protocol}", ".")
            cls = getattr(module_cls, protocol)()
            assert cls
            assert type(cls).__name__ == protocol

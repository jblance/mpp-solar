import importlib
import unittest
from pathlib import Path

HERE = Path(__file__).parent
OUTPUTS_DIR = HERE.parent.parent / "mppsolar" / "outputs"
OUTPUTS = sorted(
    file.stem for file in OUTPUTS_DIR.glob("*.py")
    if file.stem != "__init__"
)


class testOutputs(unittest.TestCase):

    def test_outputs_count(self):
        # print(len(OUTPUTS))
        assert len(OUTPUTS) == 24, len(OUTPUTS)

    def test_outputs_init(self):
        for output in OUTPUTS:
            module_cls = importlib.import_module(f"mppsolar.outputs.{output}", ".")
            cls = getattr(module_cls, output)()
            assert cls
            assert type(cls).__name__ == output

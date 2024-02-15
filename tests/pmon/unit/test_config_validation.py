""" test_config_validation.py """
import unittest
from powermon.config_model import ConfigModel
from powermon import read_yaml_file


class TestonfigModel(unittest.TestCase):
    """Test that all the configuration files in the powermon/config directory can be validated by the ConfigModel class"""

    def test_config_model_min(self):
        """ test min.yaml config """
        config = read_yaml_file("./tests/pmon/config/min.yaml")
        config_model = ConfigModel(config=config)
        self.assertTrue(config_model is not None)

    def test_config_model_min_api(self):
        """ test api.yaml config """
        config = read_yaml_file("./tests/pmon/config/api.yaml")
        config_model = ConfigModel(config=config)
        self.assertTrue(config_model is not None)

    def test_config_model_format(self):
        """ test format.yaml config """
        config = read_yaml_file("./tests/pmon/config/format.yaml")
        config_model = ConfigModel(config=config)
        self.assertTrue(config_model is not None)

    def test_config_model_powermon_hass(self):
        """ test hass.yaml config """
        config = read_yaml_file("./tests/pmon/config/hass.yaml")
        config_model = ConfigModel(config=config)
        self.assertTrue(config_model is not None)

    def test_config_model_powermon_qed(self):
        """ test qed.yaml config """
        config = read_yaml_file("./tests/pmon/config/qed.yaml")
        config_model = ConfigModel(config=config)
        self.assertTrue(config_model is not None)

    def test_config_model_powermon(self):
        """ test powermon.yaml config """
        config = read_yaml_file("./tests/pmon/config/powermon.yaml")
        config_model = ConfigModel(config=config)
        self.assertTrue(config_model is not None)

""" test_config_validation.py """
import unittest
from glob import glob

from pydantic import ValidationError

from powermon import read_yaml_file
from powermon.config_model import ConfigModel


class TestConfigModel(unittest.TestCase):
    """Test that all the configuration files in the powermon/config directory can be validated by the ConfigModel class"""
    def test_validate_config_files(self):
        """ validate all the yaml config files """
        files = glob('docker/*.yaml')
        files.extend(glob('docker/dev/config/*.yaml'))
        files.extend(glob('tests/pmon/config/*.yaml'))
        for filename in files:
            print(f"Checking valid: {filename}")
            config = read_yaml_file(filename)
            config_model = ConfigModel(config=config)
            self.assertTrue(config_model is not None)
            self.assertIsInstance(config_model, ConfigModel)

    def test_invalid_config_files(self):
        """ test that invalid config file raise exception """
        files = glob('tests/pmon/config_errors/*.yaml')
        for filename in files:
            print(f"Checking invalid: {filename}")
            config = read_yaml_file(filename)
            # config_model = ConfigModel(config=config)
            with self.assertRaises(ValidationError):
                ConfigModel(config=config)

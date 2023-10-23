import unittest
from powermon.config.config_model import ConfigModel
from powermon import read_yaml_file


class test_config_model(unittest.TestCase):
    """Test that all the configuration files in the powermon/config directory can be validated by the ConfigModel class"""
    
    def test_config_model_min(self):
        
        config = read_yaml_file("./powermon/config/min.yaml")

        try:
            config_model = ConfigModel(config=config)
            self.assertTrue(config_model is not None)
        except Exception as e:
            self.fail(e)
        
    def test_config_model_min_api(self):
        
        config = read_yaml_file("./powermon/config/min-api.yaml")

        try:
            config_model = ConfigModel(config=config)
            self.assertTrue(config_model is not None)
        except Exception as e:
            self.fail(e)

    def test_config_model_format(self):
        
        config = read_yaml_file("./powermon/config/format.yaml")

        try:
            config_model = ConfigModel(config=config)
            self.assertTrue(config_model is not None)
        except Exception as e:
            self.fail(e)
            
    def test_config_model_powermon_hass(self):
        
        config = read_yaml_file("./powermon/config/powermon-hass.yaml")

        try:
            config_model = ConfigModel(config=config)
            self.assertTrue(config_model is not None)
        except Exception as e:
            self.fail(e)
            
    def test_config_model_powermon_qed(self):
        
        config = read_yaml_file("./powermon/config/powermon-qed.yaml")

        try:
            config_model = ConfigModel(config=config)
            self.assertTrue(config_model is not None)
        except Exception as e:
            self.fail(e)
            
    def test_config_model_powermon(self):
        
        config = read_yaml_file("./powermon/config/powermon.yaml")

        try:
            config_model = ConfigModel(config=config)
            self.assertTrue(config_model is not None)
        except Exception as e:
            self.fail(e)
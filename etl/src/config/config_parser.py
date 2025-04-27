# load config yaml and create a config object to be used elsewhere

import yaml

CONFIG_FILE = "src/config/config.yaml"

class YamlPaserError(Exception):
    pass

class YamlParser:
    config = None
    def __init__(self, file):
        with open(file, 'r') as f:
            self.config = yaml.safe_load(f)

    def get(self, attribute):
        if self.config is None:
            raise YamlPaserError("Config not loaded")
        try:
            return self.config[attribute]
        except:
            raise YamlPaserError(f"Could not get {attribute} from config")
        

config = YamlParser(CONFIG_FILE)

        
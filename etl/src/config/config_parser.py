# load config yaml and create a config object to be used elsewhere
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


import os
import yaml

path = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(path, "config.yaml")

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
        except AttributeError:
            raise YamlPaserError(f"Could not get {attribute} from config")
    
    @property
    def db_engine(self):
        return create_engine(self.config.get("DATABASE"), echo=True)
    
    @property
    def db_session(self):
        return sessionmaker(bind=config.db)
    

config = YamlParser(CONFIG_FILE)

        
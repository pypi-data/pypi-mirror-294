import json
import os
import sys
from easydict import EasyDict as Edict

class Config:
    _config_data = None

    @classmethod
    def load_config(cls, filepath):
        if cls._config_data is None:
            with open(filepath, 'r') as file:
                cls._config_data = Edict(json.load(file))
        else:
            print(f"{filepath} not found!!")
            sys.exit()
        return cls._config_data

    @classmethod
    def get_config(cls):
        if cls._config_data is None:
            raise ValueError("Config not loaded. Call 'load_config' first.")
        return cls._config_data

config = Config.load_config(os.path.join(os.path.expanduser('~'), '.config/paper_down/config.json'))
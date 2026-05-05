import json
import os
import sys
import os

def getAssetPath(relativePath):
    if getattr(sys, 'frozen', False):
        basePath = sys._MEIPASS
    else:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)

class ConfigManager:

    if getattr(sys, 'frozen', False):
        BASE_DIR = os.path.dirname(sys.executable)
    else:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    CONFIG_PATH = os.path.join(BASE_DIR, "..", "config", "settings.json")

    DEFAULT_CONFIG = {
        "monitorIndex": 0,
        "position": "topRight",
        "bgColor": "black",
        "fgColor": "white"
    }

    @classmethod
    def load(cls):
        if not os.path.exists(cls.CONFIG_PATH):
            return cls.DEFAULT_CONFIG

        try:
            with open(cls.CONFIG_PATH, "r") as f:
                return json.load(f)
        except Exception:
            return cls.DEFAULT_CONFIG

    @classmethod
    def save(cls, config):
        os.makedirs(os.path.dirname(cls.CONFIG_PATH), exist_ok=True)

        with open(cls.CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)
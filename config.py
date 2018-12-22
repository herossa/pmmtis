import os
import json

class config:
    def __init__(self, config_file: str):
        self.config = None
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                self.config = json.loads(f.read())

    def get_config(self):
        return self.config

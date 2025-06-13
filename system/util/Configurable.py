import yaml

class Configurable:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)

    def load_config(self, path):
            with open(path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            return config
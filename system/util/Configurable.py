import yaml

class Configurable:
    def __init__(self, config_path):
        self.config_path = config_path  # сохраняем путь к файлу
        self.config = self.load_config(config_path)

    def load_config(self, path):
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return config

    def save_config(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(self.config, f, allow_unicode=True)

    def set_value(self, keys: list, value):
        """
        Изменить значение в config по списку ключей keys, например:
        keys = ['nmap', 'target']
        """
        d = self.config
        for key in keys[:-1]:
            if key not in d or not isinstance(d[key], dict):
                d[key] = {}
            d = d[key]
        d[keys[-1]] = value
        self.save_config()
    
    def get_value(self, keys: list[str]):
        """
        Получить значение из config по списку ключей keys, например:
        keys = ['nmap', 'target']
        """
        d = self.config
        for key in keys:
            d = d[key]
        return d
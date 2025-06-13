import time
import threading
from system.interface.ListMenu.Button import Button
import yaml


class DynamicButton(Button):
    def __init__(self, label, config_path, yaml_path: list[str], hop_context=None):
        self.config_path = config_path
        self.yaml_path = yaml_path
        self._cached_value = self._read_from_yaml()
        super().__init__(label, hop_context=hop_context)

    def _format_label(self, value):
        return f"{self.label}{value}"

    def _read_from_yaml(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # Переход по вложенным ключам
        for key in self.yaml_path:
            data = data[key]

        return data

    def _write_to_yaml(self, new_value):
        with open(self.config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # Переход по пути, создание ключей по пути если надо
        d = data
        for key in self.yaml_path[:-1]:
            if key not in d:
                d[key] = {}
            d = d[key]

        d[self.yaml_path[-1]] = new_value  # Установка значения

        # Запись обратно в YAML
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True)

    def get_item_text(self):
        return self._format_label(self._cached_value)

    def set_value(self, new_value):
        self._cached_value = new_value
        self.label = self._format_label(new_value)
        self._write_to_yaml(new_value)

    def refresh(self):
        """Обновляет значение из файла"""
        self._cached_value = self._read_from_yaml()

        
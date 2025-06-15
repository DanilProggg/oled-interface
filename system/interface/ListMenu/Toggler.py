
from system.interface.ListMenu.ListMenuItem import ListMenuItem
from system.util.Configurable import Configurable

class Toggler(ListMenuItem):
    def __init__(self, label: str, toggler_config: Configurable, keys: list[str]):
        """
        label           — текст пункта меню (до “: ”)
        toggler_config  — экземпляр Configurable
        keys            — путь в YAML-карте к блоку, например ["file"]
                          тогда читаем ["file","options"] и ["file","current"]
        """
        super().__init__(label)
        self.config = toggler_config
        self.keys = keys

        # Загрузим список опций и текущее значение
        self.options = self._load_options()
        self.value = self._load_value()
        # Найдём индекс
        try:
            self.index = self.options.index(self.value)
        except ValueError:
            # если current в options нет, вернёмся к первому
            self.index = 0
            if self.options:
                self.value = self.options[0]
                self._save_value()

    def _load_options(self) -> list[str]:
        try:
            return self.config.get_value(self.keys + ["options"])
        except KeyError:
            return []

    def _load_value(self) -> str | None:
        try:
            return self.config.get_value(self.keys + ["current"])
        except KeyError:
            return None

    def _save_value(self):
        # Запишем в конфиг и сохраним файл
        self.config.set_value(self.keys + ["current"], self.value)

    def handle_left(self):
        if not self.options:
            return
        # влево — уменьшаем индекс
        self.index = (self.index - 1) % len(self.options)
        self.value = self.options[self.index]
        self._save_value()

    def handle_right(self):
        if not self.options:
            return
        # вправо — увеличиваем
        self.index = (self.index + 1) % len(self.options)
        self.value = self.options[self.index]
        self._save_value()

    def handle_ok(self):
        # можно тут вызывать какое-то действие при нажатии Enter, 
        # но по-умолчанию мы уже сохраняем в handle_left/right
        pass

    def get_item_text(self):
        return self.label

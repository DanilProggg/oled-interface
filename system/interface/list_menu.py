import json
from abc import ABC, abstractmethod
from typing import override

from system.interface.menu_template import Menu

class ListMenu(Menu):
    def __init__(self, title: str, items):
        self.index = 0
        self.title = title
        self.items = items
        self._display_buffer = []

    @override
    def draw(self):
        pass

    @override
    def move(self, direction):
        if direction == "left":
            self.items[self.index].handle_left()  # Свайп влево для переключателя
        elif direction == "right":
            self.items[self.index].handle_right()  # Свайп вправо
        elif direction == "up":
            self.index = max(0, self.index - 1)
        elif direction == "down":
            self.index = min(len(self.items) - 1, self.index + 1)


class ListMenuItem(ABC):
    def __init__(self, label):
        self.label = label
    @abstractmethod
    def get_item_text(self) -> str:
        pass


    # ==== BUTTON ==== #
    def handle_ok(self):
        """Обработка нажатия OK (для кнопок и подтверждения выбора)"""
        pass
    # ==== TOGGLER ==== #

    def handle_left(self):
        """Обработка свайпа влево (для переключателей)"""
        pass

    def handle_right(self):
        """Обработка свайпа вправо (для переключателей)"""
        pass




class Button(ListMenuItem):
    def __init__(self, label, hop_context):
        super().__init__(label)
        self.hop_context = hop_context

    def get_item_text(self) -> str:
        return self.label

    def handle_ok(self):
        return self.hop_context

    def handle_left(self):
        pass

    def handle_right(self):
        pass



class Toggler(ListMenuItem):
    def __init__(self, label, json_path, json_param):
        super().__init__(label)
        self.json_path = json_path
        self.json_param = json_param
        self.options = self.load_options()
        self.current_option = self._set_up_first_option()
    def _set_up_first_option(self):
        if self.options:
            return self.options[0]
        else:
            return None

    def load_options(self):
        with open(self.json_path, "r") as file:
            data = json.load(file)

            for i in data["options"]:
                if i == self.json_param:
                    return i["options"]
        return None


    def get_item_text(self) -> str:
        pass

    def handle_ok(self): pass

    def handle_left(self):
        pass

    def handle_right(self):
        pass

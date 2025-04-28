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
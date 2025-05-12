from typing import override
import ctypes

from system.interface.menu_template import Menu




class ListMenu(Menu):
    def __init__(self, title: str, items):
        self.index = 0
        self.title = title
        self.items = items
        self.offset = 0

    @override
    def draw(self):
        pass

    @override
    def move(self, direction):
        if direction == "LEFT":
            self.items[self.index].handle_left()  # Свайп влево для переключателя
        elif direction == "RIGHT":
            self.items[self.index].handle_right()  # Свайп вправо
        elif direction == "UP":
            pass
        elif direction == "DOWN":
            pass

    @override
    def ok(self, set_context):
        self.items[self.index].handle_ok(set_context)

    @override
    def back(self):
        pass
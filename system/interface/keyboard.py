from typing import override

from system.interface.menu_template import Menu

class Keyboard(Menu):
    def __init__(self):
        pass

    @override
    def move(self, direction):
        #Переключение кнопок клавиатуры
        pass

    @override
    def back(self):
        pass

    @override
    def ok(self):
        pass


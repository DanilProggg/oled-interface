from typing import override

from system.interfaces.menu_template import Menu

class ListMenu(Menu):
    def __init__(self, title: str, items):
        self.index = 0
        self.title = title
        self.items = items

    @override
    def draw(self):
        pass

    @override
    def move(self, direction):
        pass

    @override
    def back(self):
        pass

    @override
    def ok(self):
        pass

class ListMenuItem:
    def __init__(self, label):
        self.label = label

    def action(self):
        pass

class Button(ListMenuItem):
    def __init__(self, label, hop_context):
        super().__init__(label)
        self.hop_context = hop_context

    @override
    def action(self):
        #Переход в другой контекст
        return self.hop_context



class Toggler:
    def __init__(self, label,json_path, json_param):
        self.label = label
        self.json_param = json_param
        self.options = self.load_options()

    def load_options(self):
        pass
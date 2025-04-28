from abc import ABC, abstractmethod


class AppTemplate(ABC):
    def __init__(self):
        self.menu = self.menu_init()

    @abstractmethod
    def menu_init(self):
        pass
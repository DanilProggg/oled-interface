from abc import abstractmethod, ABC

class Menu(ABC):
    def __init__(self, title: str):
        self.title = title

    @abstractmethod
    def get_draw_data(self):
        """Отрисовка для каждого меню реализуеться отдельно"""
        pass

    @abstractmethod
    def move(self, direction):
        pass

    @abstractmethod
    def back(self, switch_context):
        pass

    @abstractmethod
    def ok(self, switch_context):
        pass



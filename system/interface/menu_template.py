from abc import abstractmethod, ABC

class Menu(ABC):

    @abstractmethod
    def draw(self):
        """Отрисовка для каждого меню реализуеться отдельно"""
        pass

    @abstractmethod
    def move(self, direction):
        pass

    @abstractmethod
    def back(self):
        pass

    @abstractmethod
    def ok(self, set_context):
        pass



from abc import abstractmethod, ABC

class Menu(ABC):

    @abstractmethod
    def get_draw_data(self):
        """Отрисовка для каждого меню реализуеться отдельно"""
        pass

    @abstractmethod
    def move(self, direction):
        pass

    @abstractmethod
    def back(self, backward_context):
        pass

    @abstractmethod
    def ok(self, forward_context):
        pass



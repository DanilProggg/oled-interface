from abc import abstractmethod, ABC


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
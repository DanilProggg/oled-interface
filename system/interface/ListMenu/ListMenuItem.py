from abc import abstractmethod, ABC
import ctypes

#
# Класс для использования С++
#
class CListMenuItem(ctypes.Structure):
    _fields_ = [
        ("label", ctypes.c_char_p),  # Указатель на строку (char*)
        ("selected", ctypes.c_bool),
        ("value", ctypes.c_char_p)  # Указатель на строку (char*)
    ]

class ListMenuItem(ABC):
    def __init__(self, label):
        self.label = label
    @abstractmethod
    def get_item_text(self):
        pass


    # ==== BUTTON ==== #
    def handle_ok(self):
        """Обработка нажатия OK (для кнопок и подтверждения выбора)"""
        pass

    def handle_back(self):
        """Обработка нажатия BACK"""
        pass
    # ==== TOGGLER ==== #

    def handle_left(self):
        """Обработка свайпа влево (для переключателей)"""
        pass

    def handle_right(self):
        """Обработка свайпа вправо (для переключателей)"""
        pass
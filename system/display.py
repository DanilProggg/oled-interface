import ctypes
from system.interface.ListMenu.ListMenuItem import CListMenuItem
import logging

display_logger = logging.getLogger('debug')

class DisplayManager:
    def __init__(self):
        display_logger.debug("Инициализация дисплея")
        self.lib = ctypes.CDLL("./system/cpp/display/libst7735.so")

        # Определяем типы для initialize_display()
        self.lib.initialize_display.argtypes = []  
        self.lib.initialize_display.restype = None
        # Инициализация дисплея при запуске менеджера
        self.lib.initialize_display()
        display_logger.debug("Дисплей инициализирован")
        #
        #   Инициализация функция с++
        #
        self.lib.draw_list_menu.argtypes = (ctypes.POINTER(CListMenuItem), ctypes.c_int, ctypes.c_char_p)
        self.lib.draw_list_menu.restype = None

        self.render_map = {
            "list": self._draw_list_menu,
        }

    
    def draw(self, current_context):
        display_logger.debug(f"Отрисовка контекста {current_context.title}")
        data = current_context.get_draw_data()
        draw_func = self.render_map.get(data["type"])
        try:
            if draw_func:
                draw_func(data)
                display_logger.debug("Кадр отрисован")
            else:
                raise ValueError(f"Неизвестный тип меню: {data['type']}")
        except Exception as ex:
            display_logger.error(ex)
            

    def _draw_list_menu(self, data):
        c_items = []
        index = 0
        for item in data["items"]:
            c_item = CListMenuItem(item.label.encode(), index == data["selected"], item.value)
            index += 1

        c_items_array = (CListMenuItem * len(c_items))(*c_items)

        self.lib.draw_list_menu(c_items_array, len(c_item), data["title"].encode())
    
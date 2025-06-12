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
        #   Инициализация функций с++
        #
        self.lib.draw_list_menu.argtypes = (ctypes.POINTER(CListMenuItem), ctypes.c_int, ctypes.c_char_p)
        self.lib.draw_list_menu.restype = None

        self.lib.draw_keyboard.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p))
        self.lib.draw_keyboard.restype = None

        self.lib.read_file_menu.argtypes = (ctypes.c_uint8, ctypes.c_uint8, ctypes.POINTER(ctypes.c_char_p), ctypes.c_char_p)
        self.lib.read_file_menu.restype = None

        self.render_map = {
            "list": self._draw_list_menu,
            "keyboard": self._draw_keyboard,
            "file_reader": self._draw_file_reader
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
            label = item.label.encode()
            selected = index == data["selected"]
            value = item.value if hasattr(item, 'current_option') else None
            c_item = CListMenuItem(label, selected, value)
            c_items.append(c_item)
            index += 1

        c_items_array = (CListMenuItem * len(c_items))(*c_items)

        self.lib.draw_list_menu(c_items_array, len(c_items), data["title"].encode())
    
    def _draw_keyboard(self, data):
        CharPP = ctypes.c_char_p * 40
        grid_array = CharPP(*data['keys'])
        self.lib.draw_keyboard(data['cursor_row'], data['cursor_col'], data['input_buffer'].encode(), grid_array)

    def _draw_file_reader(self, data):
        rows = len(data["lines"])
        cols = max((len(row) for row in data["lines"]), default=0)

        # Преобразуем строки в C-массив
        CharPP = ctypes.POINTER(ctypes.c_char_p)
        c_lines = (ctypes.c_char_p * rows)(*[s.encode() for s in data["lines"]])

        self.lib.read_file_menu(
            ctypes.c_uint8(rows),
            ctypes.c_uint8(cols),
            c_lines,
            data["title"].encode()
        )

    
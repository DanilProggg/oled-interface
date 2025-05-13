import ctypes

class DisplayManager:
    def __init__(self, device):
        self.lib = ctypes.CDLL("./cpp/display/libst7735.so")

        # Определяем типы для initialize_display()
        self.lib.initialize_display.argtypes = []  
        self.lib.initialize_display.restype = None
        # Инициализация дисплея при запуске менеджера
        self.lib.initialize_display()

    
    def draw(self, current_context):
        data = current_context.get_draw_data()

import logging
import ctypes
from ctypes import c_uint8, c_char_p, POINTER

input_logger = logging.getLogger("input")

lib = ctypes.CDLL("./system/cpp/input/libinput.so", mode=ctypes.RTLD_GLOBAL)
lib.initialize_buttons.restype = ctypes.c_bool
lib.get_button_action.restype = c_char_p

# Определяем типы параметров
lib.initialize_buttons.argtypes = [POINTER(c_uint8), POINTER(c_char_p), ctypes.c_int]

class InputHandler:
    def __init__(self):
        self.pin_map = {
            4: "UP",
            17: "DOWN",
            27: "LEFT",
            22: "RIGHT",
            5: "OK",
            6: "BACK"
        }
        # pin_map: {pin_number: button_name}
        self.pins = (c_uint8 * len(self.pin_map))(*self.pin_map.keys())
        names = [name.encode('utf-8') for name in self.pin_map.values()]
        self.names = (c_char_p * len(names))(*names)

        success = lib.initialize_buttons(self.pins, self.names, len(self.pin_map))
        if not success:
            raise RuntimeError("Failed to initialize GPIO buttons")


    def get_action(self):
        action = lib.get_button_action()
        return action.decode('utf-8') if action else None
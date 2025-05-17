import logging
import keyboard

input_logger = logging.getLogger("debug")

class InputHandler:
    def __init__(self):
        # инициализация GPIO
        input_logger.debug("Инициализация ввода")
        

    def get_action(self):
        key = self._get_keyboard_action()
        input_logger.debug(f"Нажата клавиша: {key}")
        return key

    def _get_keyboard_action(self):
        if keyboard.is_pressed('up'):
            return "UP"
        elif keyboard.is_pressed('down'):
            return "DOWN"
        elif keyboard.is_pressed('left'):
            return "LEFT"
        elif keyboard.is_pressed('right'):
            return "RIGHT"
        elif keyboard.is_pressed('enter'):
            return "OK"
        elif keyboard.is_pressed('esc'):
            return "BACK"




import logging
import keyboard

input_logger = logging.getLogger("debug")

class InputHandler:
    def __init__(self):
        # инициализация GPIO
        input_logger.debug("Инициализация ввода")

    def get_action(self):
        return curses.wrapper(self._curses_loop)

    def _curses_loop(self, stdscr):
        stdscr.nodelay(False)
        stdscr.keypad(True)
        
        key = stdscr.getch()
        if key == curses.KEY_UP:
            return "UP"
        elif key == curses.KEY_DOWN:
            return "DOWN"
        elif key == curses.KEY_LEFT:
            return "LEFT"
        elif key == curses.KEY_RIGHT:
            return "RIGHT"
        elif key in (10, 13):  # Enter
            return "OK"
        elif key == 27:  # Esc
            return "BACK"


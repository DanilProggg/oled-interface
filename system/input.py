import logging
import curses

input_logger = logging.getLogger("debug")

class InputHandler:
    def __init__(self):
        # инициализация GPIO
        input_logger.debug("Инициализация ввода")

    def get_action(self):
        return curses.wrapper(self._curses_loop)

    def _curses_loop(self, stdscr):
        stdscr.nodelay(True)   # Включаем неблокирующий ввод
        stdscr.keypad(True)

        key = stdscr.getch()
        if key == -1:
            return None

        if key == 27:
            curses.napms(10)  # Дать шанс другим байтам появиться
            next_key = stdscr.getch()
            if next_key == -1:
                input_logger.debug("Нажата кнопка BACK (ESC)")
                return "BACK"
            else:
                # Это escape-последовательность (например, стрелка)
                stdscr.getch()  # съесть ещё один символ, если есть
                return None  # Не возвращаем BACK

        if key == curses.KEY_UP:
            input_logger.debug("Нажата кнопка UP")
            return "UP"
        elif key == curses.KEY_DOWN:
            input_logger.debug("Нажата кнопка DOWN")
            return "DOWN"
        elif key == curses.KEY_LEFT:
            input_logger.debug("Нажата кнопка LEFT")
            return "LEFT"
        elif key == curses.KEY_RIGHT:
            input_logger.debug("Нажата кнопка RIGHT")
            return "RIGHT"
        elif key in (10, 13):  # Enter
            input_logger.debug("Нажата кнопка OK")
            return "OK"
        
        return None


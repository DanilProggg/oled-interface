from system.interface.menu_template import Menu
from system.interface.TextMenu.TextMenu import TextMenu
from system.util.Configurable import Configurable
import subprocess, threading
import textwrap
import shlex

import logging

logger = logging.getLogger("display")

class AppRunner(Menu, TextMenu):
    def __init__(self, title, configurable: Configurable, get_command_callback):
        Menu.__init__(self, title)
        TextMenu.__init__(self, title)
        self.configurable = configurable
        #Команда для старта
        #Например 'nmap -sN 192.168.0.0/24'
        self.command = get_command_callback()
        
        self.process = None

        logger.debug(f"AppRunner init\nConfig path: {self.configurable.config_path}")

    #Запуск программы в отдельном потоке
    def run(self, command: str):
        def runner():
            self.process = subprocess.Popen(
                shlex.split(command),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            self.lines.clear()
            real_line_number = 1

            for line in self.process.stdout:
                line = line.rstrip("\n")
                wrapped_lines = textwrap.wrap(line, self.CHARS_IN_LINE)
                for i, chunk in enumerate(wrapped_lines):
                    if i == 0:
                        numbered_line = f"{real_line_number:>3} {chunk}"
                        self.lines.append(numbered_line)
                    else:
                        self.lines.append(f"    {chunk}")
                real_line_number += 1

            self.process.wait()
            self.is_running = False  # флаг, что поток завершился

        self.is_running = True
        self.thread = threading.Thread(target=runner)
        self.thread.start()

        

    #Временная затычка для вызова только во время активного экрана
    
    def get_draw_data(self):
        #Вызов процесса приложения, если он не активен
        if self.process is None:
            self.run(self.command)

        return TextMenu.get_draw_data(self)

    def move(self, direction):
        TextMenu.move(self, direction)


    def back(self, switch_context):
        switch_context()

    def ok(self, switch_context):
        switch_context()

    #Деструктор
    def __del__(self):
        logger.debug("Вызов деструктора. Завершение процесса Nmap")

        # Завершаем subprocess
        if self.process and self.process.poll() is None:
            logger.debug("Процесс ещё жив. Завершаем...")
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                logger.debug("Принудительное завершение...")
                self.process.kill()

        # Ждём завершения фонового потока, если ещё работает
        if self.thread and self.thread.is_alive():
            logger.debug("Ожидание завершения фонового потока...")
            self.thread.join(timeout=2)
            if self.thread.is_alive():
                logger.debug("Поток не завершён принудительно")
            else:
                logger.debug("Фоновый поток завершён корректно")

        self.is_running = False

from system.interface.menu_template import Menu
from system.interface.TextMenu.TextMenu import TextMenu
import textwrap
import logging
import os


logger = logging.getLogger("display")

class FileReader(Menu, TextMenu):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.filename = os.path.basename(self.file_path)
        Menu.__init__(self, self.filename)
        TextMenu.__init__(self, self.filename)
        self._load_file()
        

    def _load_file(self):
        """Читает файл и формирует список отформатированных строк с номерами."""
        self.lines.clear()
        with open(self.file_path, "r", encoding="utf-8") as file:
            real_line_number = 1
            for line in file:
                line = line.rstrip("\n")
                wrapped_lines = textwrap.wrap(line, self.CHARS_IN_LINE)
                for i, chunk in enumerate(wrapped_lines):
                    if i == 0:
                        # Нумеруем только первую строку блока, например: " 1 текст..."
                        numbered_line = f"{real_line_number:>3} {chunk}"
                        self.lines.append(numbered_line)
                    else:
                        # Продолжение с отступом, чтобы не путать с новой строкой
                        self.lines.append(f"    {chunk}")
                real_line_number += 1
    
    def get_draw_data(self):
        return TextMenu.get_draw_data(self)

    def move(self, direction):
        TextMenu.move(self, direction)


    def back(self, switch_context):
        switch_context()

    def ok(self, switch_context):
        switch_context()
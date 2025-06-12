from system.interface.menu_template import Menu
import textwrap
import logging
import os

logger = logging.getLogger("debug")

class FileReader(Menu):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.filename = os.path.basename(self.file_path)
        super().__init__(self.filename)
        self.lines = []
        self.offset = 0
        self.CHARS_PER_LINE = 22
        self.max_visible = 10
        self._load_file()
        


    def _load_file(self):
        """Читает файл и формирует список отформатированных строк с номерами."""
        self.lines.clear()
        with open(self.file_path, 'r', encoding='utf-8') as file:
            real_line_number = 1
            for line in file:
                line = line.rstrip('\n')
                wrapped_lines = textwrap.wrap(line, self.CHARS_PER_LINE)
                for i, chunk in enumerate(wrapped_lines):
                    if i == 0:
                        # Нумеруем только первую строку блока, например: " 1 текст..."
                        numbered_line = f"{real_line_number:>3} {chunk}"
                        self.lines.append(numbered_line)
                    else:
                        # Продолжение с отступом, чтобы не путать с новой строкой
                        self.lines.append(f"    {chunk}")
                real_line_number += 1

        # Логируем содержимое self.lines
        total_lines = len(self.lines)
        logger.debug(f"Loaded {total_lines} formatted lines from file:")
        for idx, content in enumerate(self.lines):
            logger.debug(f"[{idx}] Content: '{content}'")


    def get_draw_data(self):
        visible_lines = self.lines[self.offset:self.offset + self.max_visible]
        draw_data = {
            "type": "file_reader",
            "lines": visible_lines,
            "title": self.filename
        }
        return draw_data
    
    def move(self, direction):
        if direction == "UP":
            if self.offset > 0:
                self.offset -= 1
        elif direction == "DOWN":
            if self.offset + self.max_visible < len(self.lines):
                self.offset += 1
        logger.debug(f"Move: {direction}, offset={self.offset}")


    def back(self, switch_context):
        switch_context()

    def ok(self, switch_context):
        switch_context()
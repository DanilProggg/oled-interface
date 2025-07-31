from system.interface.menu_template import Menu
import logging

logger = logging.getLogger("display")

class Keyboard(Menu):
    def __init__(self):
        Menu.__init__(self, "Keyboard")

        self.cursor_row = 0
        self.cursor_col = 0
        self.input_buffer = ""
        self.keyboard_grid = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', '.', '<'],  # Кнопка Backspace
            ['z', 'x', 'c', 'v', 'b', 'n', 'm', '-', '/', 'OK']   # Кнопка подтверждения
        ]
        self._ensure_valid_cursor_position()

        #Callback reservation to DynamicButton
        self._on_change_callback = None

    #Callback to DynamicButton function setup
    def set_on_change_callback(self, callback):
        self._on_change_callback = callback


    def _ensure_valid_cursor_position(self):
        original_row = self.cursor_row
        original_col = self.cursor_col
        while True:
            if not (0 <= self.cursor_row < 4) or not (0 <= self.cursor_col < 10):
                self.cursor_row = 0
                self.cursor_col = 0
            
            key_label = self.keyboard_grid[self.cursor_row][self.cursor_col]
            if key_label.strip() != '':
                return
            
            self.cursor_col += 1
            if self.cursor_col >= 10:
                self.cursor_col = 0
                self.cursor_row += 1
                if self.cursor_row >= 4:
                    self.cursor_row = 0
            
            if self.cursor_row == original_row and self.cursor_col == original_col:
                return
    def _get_new_position(self, direction):
        new_row = self.cursor_row
        new_col = self.cursor_col
        
        if direction == 'RIGHT':
            new_col += 1
            if new_col >= 10:
                new_col = 0
                new_row += 1
                if new_row >= 4:
                    new_row = 0
        elif direction == 'LEFT':
            new_col -= 1
            if new_col < 0:
                new_col = 9
                new_row -= 1
                if new_row < 0:
                    new_row = 3
        elif direction == 'DOWN':
            new_row += 1
            if new_row >= 4:
                new_row = 0
        elif direction == 'UP':
            new_row -= 1
            if new_row < 0:
                new_row = 3
        return new_row, new_col

    def _get_next_position(self, direction, current_row, current_col):
        if direction == 'RIGHT':
            current_col += 1
            if current_col >= 10:
                current_col = 0
                current_row += 1
                if current_row >= 4:
                    current_row = 0
        elif direction == 'LEFT':
            current_col -= 1
            if current_col < 0:
                current_col = 9
                current_row -= 1
                if current_row < 0:
                    current_row = 3
        elif direction == 'DOWN':
            current_row += 1
            if current_row >= 4:
                current_row = 0
        elif direction == 'UP':
            current_row -= 1
            if current_row < 0:
                current_row = 3
        return current_row, current_col

    def move(self, direction):
        original_row = self.cursor_row
        original_col = self.cursor_col
        
        new_row, new_col = self._get_new_position(direction)
        current_row, current_col = new_row, new_col
        
        while True:
            if 0 <= current_row < 4 and 0 <= current_col < 10:
                key_label = self.keyboard_grid[current_row][current_col]
                if key_label.strip() != '':
                    self.cursor_row = current_row
                    self.cursor_col = current_col
                    return
            
            current_row, current_col = self._get_next_position(direction, current_row, current_col)
            
            if current_row == original_row and current_col == original_col:
                return

    def back(self, switch_context):
        switch_context()

    def ok(self, switch_context):
        current_key = self.keyboard_grid[self.cursor_row][self.cursor_col]
        
        if current_key == 'OK':
            # Возвращаем введенный текст через контекст
            self._on_change_callback(self.input_buffer)
            switch_context()  # Инициируем возврат в предыдущее меню
        elif current_key == '<':
            # Удаляем последний символ
            self.input_buffer = self.input_buffer[:-1]
        else:
            # Добавляем символ в буфер
            if current_key.strip() != '':
                self.input_buffer += current_key

    def get_draw_data(self):
        draw_data = {
            'type': 'keyboard',
            'input_buffer': self.input_buffer,
            'cursor_row': self.cursor_row,
            'cursor_col': self.cursor_col,
            'keys': [s.encode('utf-8') for row in self.keyboard_grid for s in row]
        }
        return draw_data
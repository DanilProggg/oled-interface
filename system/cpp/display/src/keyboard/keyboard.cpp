#include "keyboard.h"
#include <cstring>

void draw_key(uint8_t x, uint8_t y, const char* label, bool selected) {
    uint16_t key_color = selected ? COLOR_BLACK : COLOR_WHITE;
    uint16_t bg_color  = selected ? COLOR_GREEN : COLOR_BLUE;

    st7735_draw_rect(x, y, 16, 16, bg_color);

    // Центрируем текст
    uint8_t len = strlen(label);
    uint8_t text_x = x + (8 - len * 3);  // 6px/char, выравнивание в центре
    uint8_t text_y = y + 4;

    for (uint8_t i = 0; i < len; ++i) {
        st7735_draw_char(text_x, text_y, label[i], key_color, bg_color);
        text_x += 6;
    }
}


void draw_keyboard(uint8_t cursor_row, uint8_t cursor_col, const char* input_buffer, const char** grid) {
    buffer_clear(COLOR_BLACK);

    // Поле ввода
    st7735_draw_string(5, 2, input_buffer, COLOR_WHITE, COLOR_BLACK);

    for (uint8_t row = 0; row < 4; ++row) {
        for (uint8_t col = 0; col < 10; ++col) {
            const char* key_label = grid[row * 10 + col];
            if (strlen(key_label) == 0) continue;

            uint8_t x = col * 16;
            uint8_t y = 22 + row * 18;

            bool selected = (cursor_row == row && cursor_col == col);
            draw_key(x, y, key_label, selected);
        }
    }

    buffer_flush_to_display();
}



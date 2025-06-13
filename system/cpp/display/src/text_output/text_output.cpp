#include "text_output.h"
#include <cstdint>

void text_output(uint8_t rows, uint8_t cols, const char** matrix, const char* title) {
    buffer_clear(BACKGROUND_COLOR);

    // Заголовок
    set_window_label(title, TEXT_COLOR, BACKGROUND_COLOR);

    // Отрисовка строк
    uint8_t start_x = 1;
    uint8_t start_y = 20;
    uint8_t line_height = 10;

    for (uint8_t i = 0; i < rows; i++) {
        if (!matrix[i]) continue; // Проверка на null

        st7735_draw_string(start_x, start_y + i * line_height, matrix[i], TEXT_COLOR, BACKGROUND_COLOR);
    }

    // Обновляем экран
    buffer_flush_to_display();
}
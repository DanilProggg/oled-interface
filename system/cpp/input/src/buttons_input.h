#ifndef BUTTONS_H
#define BUTTONS_H
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// Инициализация кнопок динамически:
// pin_array - массив GPIO номеров (BCM)
// name_array - массив C-строк с именами кнопок
// pin_count - длина массивов
// Возвращает true, если инициализация прошла успешно
bool initialize_buttons(const uint8_t* pin_array, const char** name_array, int pin_count);

// Возвращает имя нажатой кнопки или пустую строку, если кнопка не нажата
const char* get_button_action();

#ifdef __cplusplus
}
#endif

#endif // BUTTONS_H

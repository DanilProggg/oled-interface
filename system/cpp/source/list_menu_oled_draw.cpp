#include <vector>
#include <string>
#include <cstring>  // Для работы с C-строками (snprintf)

// Предполагаемые низкоуровневые функции для OLED-дисплея
// (Их реализация зависит от вашей библиотеки, например, luma.oled или кастомный драйвер)
extern "C" {
    void oled_clear();                          // Очистка экрана
    void oled_draw_string(int x, int y, const char* text);  // Вывод текста в (x, y)
    void oled_update();                         // Обновление дисплея (вывод буфера)
}

// Основная функция отрисовки меню
extern "C" void draw_list_menu(
    const char* title,         // Заголовок меню (например, "Main Menu")
    const char** items,        // Массив строк-пунктов (например, ["Start", "Settings"])
    const char** values,       // Массив значений для переключателей (например, ["high", nullptr])
    int items_count,          // Количество пунктов
    int selected_idx          // Индекс выбранного пункта (для подсветки)
) {
    // 1. Очищаем экран (заполняем чёрным)
    oled_clear();

    // 2. Выводим заголовок в верхней строке (координаты x=0, y=0)
    oled_draw_string(0, 0, title);

    // 3. Перебираем все пункты меню
    for (int i = 0; i < items_count; ++i) {
        // 3.1. Вычисляем Y-координату для текущего пункта
        //      (Каждый новый пункт смещается на 10 пикселей вниз)
        int y_pos = 10 + i * 10;

        // 3.2. Формируем строку для отрисовки
        char buffer[128];  // Буфер для текста (128 символов — с запасом)

        if (values[i] != nullptr) {
            // Если есть значение (для Toggler), форматируем как "Label <value>"
            snprintf(buffer, sizeof(buffer), "%s <%s>", items[i], values[i]);
        } else {
            // Обычный пункт (без < >)
            snprintf(buffer, sizeof(buffer), "%s", items[i]);
        }

        // 3.3. Подсвечиваем выбранный пункт стрелкой ">"
        if (i == selected_idx) {
            oled_draw_string(0, y_pos, ("> " + std::string(buffer)).c_str());
        } else {
            oled_draw_string(0, y_pos, ("  " + std::string(buffer)).c_str());
        }
    }

    // 4. Обновляем дисплей (выводим буфер на OLED)
    oled_update();
}
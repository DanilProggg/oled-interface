#include "list_menu.h"
#include <cstdio>
#include <stdint.h>
#include <cstring>


void draw_list_menu_item(uint8_t y, const char *str, uint16_t color, uint16_t bg, bool selected, const char *value) {
    
    const uint8_t CHAR_WIDTH = 6;
    const uint8_t PADDING = 5;
    const uint8_t TEXT_START_X = 10;

    // Проверяем выбор значения
    if (selected) {
        st7735_draw_char(3, y, '>', color, bg);
    }
    //Ставим курсор на начало значений
    uint8_t x = TEXT_START_X;

    while(*str) {
        st7735_draw_char(x, y, *str++, color, bg);
        x += CHAR_WIDTH;
        //Если значения нет, то пишем до границы экрана
        if (value == nullptr) {
            if(x + CHAR_WIDTH*2 >= TFT_WIDTH - PADDING) {
                st7735_draw_char(x, y, '.', color, bg);
                st7735_draw_char(x+CHAR_WIDTH, y, '.', color, bg);
                break;
            }
        // Если занение есть - оставляем 55px под значение (11 символов)
        } else {
            if(x == 76) {
                st7735_draw_char(x, y, '.', color, bg);
                st7735_draw_char(x+CHAR_WIDTH, y, '.', color, bg);
                st7735_draw_char(x+CHAR_WIDTH*2, y, ' ', color, bg);
                break;
            }
            
        }
    }

    if (value != nullptr) {
        x = 90;
        st7735_draw_char(x, y, '<', color, bg);
        x += CHAR_WIDTH;
        while (*value){
            st7735_draw_char(x, y, *value++, color, bg);
            x += CHAR_WIDTH;
            if (x + CHAR_WIDTH*2 >= TFT_WIDTH - PADDING) {
                st7735_draw_char(x, y, '.', color, bg);
                st7735_draw_char(x+6, y, '.', color, bg);
                break;
            }
        }
        st7735_draw_char(150, y, '>', color, bg);
    }
    
}


void draw_list_menu(const MenuItem *items, int itemsCount, const char *menu_label) {
    buffer_clear(COLOR_BLACK);
    set_window_label(menu_label, COLOR_GREEN, COLOR_BLACK);

    if (itemsCount > 10) {
        itemsCount = 10;
    }
    //Начальна строка для списка
    uint8_t y = 18;
    for (int i = 0; i < itemsCount; ++i) {
        draw_list_menu_item(y, items[i].label, COLOR_ORANGE, COLOR_BLACK, items[i].selected, items[i].value);
        y+=10;
    }
    buffer_flush_to_display();
}



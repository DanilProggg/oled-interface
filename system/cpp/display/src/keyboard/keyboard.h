#ifndef KEYBOARD_MENU_H
#define KEYBOARD_MENU_H

#ifdef __cplusplus
extern "C" {
#endif

#include "st7735.h"

void draw_keyboard(uint8_t cursor_row, uint8_t cursor_col, const char* input_buffer, const char** grid);

#ifdef __cplusplus
}
#endif

#endif

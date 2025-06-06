#ifndef KEYBOARD_MENU_H
#define KEYBOARD_MENU_H

#ifdef __cplusplus
extern "C" {
#endif

#include "st7735.h"

const char* keyboard_grid[4][10] = {
    { "q", "w", "e", "r", "t", "y", "u", "i", "o", "p" },
    { "a", "s", "d", "f", "g", "h", "j", "k", "l", ""  },
    { "z", "x", "c", "v", "b", "n", "m", "0", "1", "2" },
    { "3", "4", "5", "6", "7", "8", "9", "<", "OK", "" }
};





#ifdef __cplusplus
}
#endif

#endif

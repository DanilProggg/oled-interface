#ifndef LIST_MENU_H
#define LIST_MENU_H

#ifdef __cplusplus
extern "C" {
#endif

#include "st7735.h"

typedef struct {
    const char* label;
    bool selected;
    const char* value;
} MenuItem;


void draw_list_menu(const MenuItem *items, int itemsCount, const char *menu_label);

#ifdef __cplusplus
}
#endif

#endif


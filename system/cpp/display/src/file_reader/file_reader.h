#ifndef FILE_READER_H
#define FILE_READER_H

#ifdef __cplusplus
extern "C" {
#endif

#include "st7735.h"

#define BACKGROUND_COLOR 0x0000      // Черный
#define TEXT_COLOR        0xFFFF     // Белый

void read_file_menu(uint8_t rows, uint8_t cols, const char** matrix, const char* title);

#ifdef __cplusplus
}
#endif


#endif
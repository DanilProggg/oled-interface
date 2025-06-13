#ifndef TEXT_OUTPUT_H
#define TEXT_OUTPUT_H

#ifdef __cplusplus
extern "C" {
#endif

#include "st7735.h"

#define BACKGROUND_COLOR 0x0000      // Черный
#define TEXT_COLOR        0xFFFF     // Белый

void text_output(uint8_t rows, uint8_t cols, const char** matrix, const char* title);

#ifdef __cplusplus
}
#endif


#endif
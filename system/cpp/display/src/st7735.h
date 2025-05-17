#ifndef ST7735_H
#define ST7735_H

#ifdef __cplusplus
extern "C" {
#endif

#include <bcm2835.h>
#include "font.h"

#define DC_PIN RPI_GPIO_P1_22
#define RST_PIN RPI_GPIO_P1_18

// Константы дисплея
#define TFT_WIDTH 160
#define TFT_HEIGHT 128
#define COLOR_BLACK 0x0000
#define COLOR_WHITE 0xFFFF
#define COLOR_RED 0xF800
#define COLOR_GREEN 0x07E0
#define COLOR_BLUE 0x001F
#define COLOR_ORANGE 0x00FF

// Параметры ориентации
#define MADCTL_MY  0x80
#define MADCTL_MX  0x40
#define MADCTL_MV  0x20
#define MADCTL_ML  0x10
#define MADCTL_RGB 0x08
#define MADCTL_MH  0x04



// Прототипы функций
void st7735_init();
void buffer_draw_pixel(uint8_t x, uint8_t y, uint16_t color);
void buffer_clear(uint16_t color);
void buffer_flush_to_display();
void st7735_draw_char(uint8_t x, uint8_t y, char c, uint16_t color, uint16_t bg);
void st7735_draw_string(uint8_t x, uint8_t y, const char *str, uint16_t color, uint16_t bg);
void set_window_label(const char *label, uint16_t color, uint16_t bg);
void st7735_draw_rect(uint8_t x, uint8_t y, uint8_t width, uint8_t height, uint16_t color);

#ifdef __cplusplus
}
#endif

#endif
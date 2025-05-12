#include <U8g2lib.h>

// Конфигурация для ST7735S (128x160, 4-проводной SPI)
U8G2_ST7735_128x160_F_4W_SW_SPI u8g2(
    U8G2_R0,  // Поворот
    11,       // SCK (GPIO11)
    10,       // MOSI (GPIO10)
    8,        // CS (GPIO8)
    24,       // DC (GPIO24)
    25        // RESET (GPIO25)
);
extern "C" {
    // Инициализация (вызывается 1 раз)
    void init_display() {
        u8g2.begin();
        u8g2.setFont(u8g2_font_6x10_tf);
        u8g2.clearBuffer();
    }

    // Отрисовка текста
    void draw_text(const char* text) {
        u8g2.clearBuffer();
        u8g2.drawStr(10, 30, text);
        u8g2.drawFrame(0, 0, 128, 160);
        u8g2.sendBuffer();
    }
}
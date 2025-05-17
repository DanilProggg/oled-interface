#include "st7735.h"
#include <cstdio>
#include <cstring>

//Буффер для отрисовки кадра
uint16_t framebuffer[TFT_WIDTH * TFT_HEIGHT];

void st7735_write_command(uint8_t cmd) {
    bcm2835_gpio_write(DC_PIN, LOW);
    bcm2835_spi_transfer(cmd);
}

void st7735_write_data(uint8_t data) {
    bcm2835_gpio_write(DC_PIN, HIGH);
    bcm2835_spi_transfer(data);
}

void st7735_set_address_window(uint8_t x0, uint8_t y0, uint8_t x1, uint8_t y1) {
    st7735_write_command(0x2A); // CASET
    st7735_write_data(0x00);
    st7735_write_data(x0);
    st7735_write_data(0x00);
    st7735_write_data(x1);

    st7735_write_command(0x2B); // RASET
    st7735_write_data(0x00);
    st7735_write_data(y0);
    st7735_write_data(0x00);
    st7735_write_data(y1);

    st7735_write_command(0x2C); // RAMWR
}

void st7735_set_rotation(uint8_t rotation) {
    st7735_write_command(0x36); // MADCTL
    switch(rotation) {
        case 3: // 270°
            st7735_write_data(MADCTL_MX | MADCTL_MV | MADCTL_RGB);
            break;
        case 1: // 90°
            st7735_write_data(MADCTL_MV | MADCTL_MY | MADCTL_RGB);
            break;
        default: // 0°
            st7735_write_data(MADCTL_MX | MADCTL_MY | MADCTL_RGB);
    }
}

void st7735_init() {
    // Сброс
    bcm2835_gpio_write(RST_PIN, LOW);
    bcm2835_delay(100);
    bcm2835_gpio_write(RST_PIN, HIGH);
    bcm2835_delay(100);

    // Инициализация
    st7735_write_command(0x01); // SWRESET
    bcm2835_delay(150);
    
    st7735_write_command(0x11); // SLPOUT
    bcm2835_delay(255);

    st7735_write_command(0x3A); // COLMOD
    st7735_write_data(0x05);    // 16-bit

    // Настройка ориентации
    st7735_set_rotation(3); // Поворот 270°
    
    // Корректировка смещения для 160x128
    st7735_write_command(0x2A); // CASET
    st7735_write_data(0x00);
    st7735_write_data(0x01);    // XStart = 1
    st7735_write_data(0x00);
    st7735_write_data(0xA0);    // XEnd = 160

    st7735_write_command(0x2B); // RASET
    st7735_write_data(0x00);
    st7735_write_data(0x20);    // YStart = 32
    st7735_write_data(0x00);
    st7735_write_data(0x7F);    // YEnd = 127

    st7735_write_command(0x29); // DISPON
    bcm2835_delay(100);

     // Очистка экрана
    st7735_set_address_window(0, 0, TFT_WIDTH-1, TFT_HEIGHT-1);
    for(uint32_t i = 0; i < TFT_WIDTH * TFT_HEIGHT; i++) {
        st7735_write_data(COLOR_BLACK >> 8);
        st7735_write_data(COLOR_BLACK & 0xFF);
    }
}


void buffer_draw_pixel(uint8_t x, uint8_t y, uint16_t color) {
    if (x >= TFT_WIDTH || y >= TFT_HEIGHT) return;
    framebuffer[y * TFT_WIDTH + x] = color;
}

void buffer_clear(uint16_t color) {
    for (int i = 0; i < TFT_WIDTH * TFT_HEIGHT; ++i) {
        framebuffer[i] = color;
    }
}

void buffer_flush_to_display() {
    st7735_set_address_window(0, 0, TFT_WIDTH - 1, TFT_HEIGHT - 1);
    for (int i = 0; i < TFT_WIDTH * TFT_HEIGHT; ++i) {
        uint16_t color = framebuffer[i];
        st7735_write_data(color >> 8);
        st7735_write_data(color & 0xFF);
    }
}



void st7735_draw_char(uint8_t x, uint8_t y, char c, uint16_t color, uint16_t bg) {
    if(c < 32 || c > 127) return;

    const uint8_t *chr = &font[(c - 32) * 5];
    
    for(uint8_t i = 0; i < 5; i++) {
        uint8_t line = chr[i];
        for(uint8_t j = 0; j < 8; j++) {
            if(line & 0x1) {
                buffer_draw_pixel(x + i, y + j, color);
            } else {
                buffer_draw_pixel(x + i, y + j, bg);
            }
            line >>= 1;
        }
    }
}

void st7735_draw_string(uint8_t x, uint8_t y, const char *str, uint16_t color, uint16_t bg) {
    while(*str) {
        st7735_draw_char(x, y, *str++, color, bg);
        x += 6;
        if(x + 5 >= TFT_WIDTH) {
            x = 0;
            y += 9;
        }
    }
}

void st7735_draw_rect(uint8_t x, uint8_t y, uint8_t width, uint8_t height, uint16_t color) {
    // Проверка выхода начальных координат за пределы экрана
    if (x >= TFT_WIDTH || y >= TFT_HEIGHT) return;

    // Расчет конечных координат с учетом границ экрана
    uint16_t end_x = (uint16_t)x + width;
    if (end_x > TFT_WIDTH) end_x = TFT_WIDTH;
    
    uint16_t end_y = (uint16_t)y + height;
    if (end_y > TFT_HEIGHT) end_y = TFT_HEIGHT;

    // Отрисовка каждого пикселя прямоугольника
    for (uint16_t i = x; i < end_x; i++) {
        for (uint16_t j = y; j < end_y; j++) {
            buffer_draw_pixel((uint8_t)i, (uint8_t)j, color);
        }
    }
}


void set_window_label(const char *label, uint16_t color, uint16_t bg) {
    uint8_t x = 5;
    uint8_t y = 6;
    while(*label) {
        st7735_draw_char(x, y, *label++, color, bg);
        x += 6;
        if(x + 18 >= TFT_WIDTH - 60) {
            st7735_draw_char(x, y, '.', color, bg);
            st7735_draw_char(x+6, y, '.', color, bg);
            st7735_draw_char(x+12, y, '.', color, bg);
        }
    }
}


#include <bcm2835.h>
#include <cstdio>
#include <cstring>

// Пины
#define DC_PIN RPI_GPIO_P1_22
#define RST_PIN RPI_GPIO_P1_18

// Размеры для поворота 270°
#define TFT_WIDTH 160
#define TFT_HEIGHT 128

// Параметры ориентации
#define MADCTL_MY  0x80
#define MADCTL_MX  0x40
#define MADCTL_MV  0x20
#define MADCTL_ML  0x10
#define MADCTL_RGB 0x08
#define MADCTL_MH  0x04

// Цвета RGB565
#define COLOR_BLACK   0x0000
#define COLOR_WHITE   0xFFFF
#define COLOR_RED     0xF800
#define COLOR_GREEN   0x07E0
#define COLOR_BLUE    0x001F

// Шрифт 5x8
extern const unsigned char font[];

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
    bcm2835_gpio_write(RST_PIN, HIGH);
    bcm2835_delay(100);
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
}

void st7735_draw_pixel(uint8_t x, uint8_t y, uint16_t color) {
    if(x >= TFT_WIDTH || y >= TFT_HEIGHT) return;
    
    st7735_set_address_window(x, y, x, y);
    st7735_write_data(color >> 8);
    st7735_write_data(color & 0xFF);
}

void st7735_draw_char(uint8_t x, uint8_t y, char c, uint16_t color, uint16_t bg) {
    if(c < 32 || c > 127) return;

    const uint8_t *chr = &font[(c - 32) * 5];
    
    for(uint8_t i = 0; i < 5; i++) {
        uint8_t line = chr[i];
        for(uint8_t j = 0; j < 8; j++) {
            if(line & 0x1) {
                st7735_draw_pixel(x + i, y + j, color);
            } else {
                st7735_draw_pixel(x + i, y + j, bg);
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


void draw_list_menu_item(uint8_t y, const char *str, uint16_t color, uint16_t bg, bool selected, const char *value = nullptr) {

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
            if(x == 88) {
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
        st7735_draw_char(144, y, '>', color, bg);
    }
    
    
}


int main() {
    if(!bcm2835_init()) {
        printf("BCM2835 init failed!\n");
        return 1;
    }

    bcm2835_spi_begin();
    bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);
    bcm2835_spi_setDataMode(BCM2835_SPI_MODE0);
    bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_64);

    bcm2835_gpio_fsel(DC_PIN, BCM2835_GPIO_FSEL_OUTP);
    bcm2835_gpio_fsel(RST_PIN, BCM2835_GPIO_FSEL_OUTP);

    st7735_init();

    // Очистка экрана
    st7735_set_address_window(0, 0, TFT_WIDTH-1, TFT_HEIGHT-1);
    for(uint32_t i = 0; i < TFT_WIDTH * TFT_HEIGHT; i++) {
        st7735_write_data(COLOR_BLACK >> 8);
        st7735_write_data(COLOR_BLACK & 0xFF);
    }

    //Шрифт 5х8

    // Вывод текста для ориентации 270°
    draw_list_menu_item(5, "Hello! Super duper long text on the display", COLOR_WHITE, COLOR_BLACK, false);
    draw_list_menu_item(15, "Raspberry Pi", COLOR_WHITE, COLOR_BLACK, false, "any value");
    draw_list_menu_item(25, "Wifi", COLOR_WHITE, COLOR_BLACK, true, "OFF");
    draw_list_menu_item(35, "Easy win", COLOR_WHITE, COLOR_BLACK, false);
    draw_list_menu_item(45, "Radio", COLOR_WHITE, COLOR_BLACK, false, "443Mgz");

    bcm2835_spi_end();
    bcm2835_close();
    return 0;
}

/* 
 * Полный шрифт 5x8 (ASCII 32-127)
 * Каждый символ занимает 5 байт (по одному на столбец)
 */
const unsigned char font[] = {
    // Space (ASCII 32)
    0x00, 0x00, 0x00, 0x00, 0x00,
    // ! 
    0x00, 0x00, 0x5F, 0x00, 0x00,
    // "
    0x00, 0x07, 0x00, 0x07, 0x00,
    // #
    0x14, 0x7F, 0x14, 0x7F, 0x14,
    // $
    0x24, 0x2A, 0x7F, 0x2A, 0x12,
    // %
    0x23, 0x13, 0x08, 0x64, 0x62,
    // &
    0x36, 0x49, 0x55, 0x22, 0x50,
    // '
    0x00, 0x05, 0x03, 0x00, 0x00,
    // (
    0x00, 0x1C, 0x22, 0x41, 0x00,
    // )
    0x00, 0x41, 0x22, 0x1C, 0x00,
    // *
    0x08, 0x2A, 0x1C, 0x2A, 0x08,
    // +
    0x08, 0x08, 0x3E, 0x08, 0x08,
    // ,
    0x00, 0x50, 0x30, 0x00, 0x00,
    // -
    0x08, 0x08, 0x08, 0x08, 0x08,
    // .
    0x00, 0x60, 0x60, 0x00, 0x00,
    // /
    0x20, 0x10, 0x08, 0x04, 0x02,
    // 0
    0x3E, 0x51, 0x49, 0x45, 0x3E,
    // 1
    0x00, 0x42, 0x7F, 0x40, 0x00,
    // 2
    0x42, 0x61, 0x51, 0x49, 0x46,
    // 3
    0x21, 0x41, 0x45, 0x4B, 0x31,
    // 4
    0x18, 0x14, 0x12, 0x7F, 0x10,
    // 5
    0x27, 0x45, 0x45, 0x45, 0x39,
    // 6
    0x3C, 0x4A, 0x49, 0x49, 0x30,
    // 7
    0x01, 0x71, 0x09, 0x05, 0x03,
    // 8
    0x36, 0x49, 0x49, 0x49, 0x36,
    // 9
    0x06, 0x49, 0x49, 0x29, 0x1E,
    // :
    0x00, 0x36, 0x36, 0x00, 0x00,
    // ;
    0x00, 0x56, 0x36, 0x00, 0x00,
    // <
    0x08, 0x14, 0x22, 0x41, 0x00,
    // =
    0x14, 0x14, 0x14, 0x14, 0x14,
    // >
    0x00, 0x41, 0x22, 0x14, 0x08,
    // ?
    0x02, 0x01, 0x51, 0x09, 0x06,
    // @
    0x32, 0x49, 0x79, 0x41, 0x3E,
    // A
    0x7E, 0x11, 0x11, 0x11, 0x7E,
    // B
    0x7F, 0x49, 0x49, 0x49, 0x36,
    // C
    0x3E, 0x41, 0x41, 0x41, 0x22,
    // D
    0x7F, 0x41, 0x41, 0x22, 0x1C,
    // E
    0x7F, 0x49, 0x49, 0x49, 0x41,
    // F
    0x7F, 0x09, 0x09, 0x09, 0x01,
    // G
    0x3E, 0x41, 0x49, 0x49, 0x7A,
    // H
    0x7F, 0x08, 0x08, 0x08, 0x7F,
    // I
    0x00, 0x41, 0x7F, 0x41, 0x00,
    // J
    0x20, 0x40, 0x41, 0x3F, 0x01,
    // K
    0x7F, 0x08, 0x14, 0x22, 0x41,
    // L
    0x7F, 0x40, 0x40, 0x40, 0x40,
    // M
    0x7F, 0x02, 0x04, 0x02, 0x7F,
    // N
    0x7F, 0x04, 0x08, 0x10, 0x7F,
    // O
    0x3E, 0x41, 0x41, 0x41, 0x3E,
    // P
    0x7F, 0x09, 0x09, 0x09, 0x06,
    // Q
    0x3E, 0x41, 0x51, 0x21, 0x5E,
    // R
    0x7F, 0x09, 0x19, 0x29, 0x46,
    // S
    0x46, 0x49, 0x49, 0x49, 0x31,
    // T
    0x01, 0x01, 0x7F, 0x01, 0x01,
    // U
    0x3F, 0x40, 0x40, 0x40, 0x3F,
    // V
    0x1F, 0x20, 0x40, 0x20, 0x1F,
    // W
    0x7F, 0x20, 0x18, 0x20, 0x7F,
    // X
    0x63, 0x14, 0x08, 0x14, 0x63,
    // Y
    0x03, 0x04, 0x78, 0x04, 0x03,
    // Z
    0x61, 0x51, 0x49, 0x45, 0x43,
    // [
    0x00, 0x7F, 0x41, 0x41, 0x00,
    // Backslash
    0x02, 0x04, 0x08, 0x10, 0x20,
    // ]
    0x00, 0x41, 0x41, 0x7F, 0x00,
    // ^
    0x04, 0x02, 0x01, 0x02, 0x04,
    // _
    0x40, 0x40, 0x40, 0x40, 0x40,
    // `
    0x00, 0x01, 0x02, 0x04, 0x00,
    // a
    0x20, 0x54, 0x54, 0x54, 0x78,
    // b
    0x7F, 0x48, 0x44, 0x44, 0x38,
    // c
    0x38, 0x44, 0x44, 0x44, 0x20,
    // d
    0x38, 0x44, 0x44, 0x48, 0x7F,
    // e
    0x38, 0x54, 0x54, 0x54, 0x18,
    // f
    0x08, 0x7E, 0x09, 0x01, 0x02,
    // g
    0x08, 0x14, 0x54, 0x54, 0x3C,
    // h
    0x7F, 0x08, 0x04, 0x04, 0x78,
    // i
    0x00, 0x44, 0x7D, 0x40, 0x00,
    // j
    0x20, 0x40, 0x44, 0x3D, 0x00,
    // k
    0x7F, 0x10, 0x28, 0x44, 0x00,
    // l
    0x00, 0x41, 0x7F, 0x40, 0x00,
    // m
    0x7C, 0x04, 0x18, 0x04, 0x78,
    // n
    0x7C, 0x08, 0x04, 0x04, 0x78,
    // o
    0x38, 0x44, 0x44, 0x44, 0x38,
    // p
    0x7C, 0x14, 0x14, 0x14, 0x08,
    // q
    0x08, 0x14, 0x14, 0x18, 0x7C,
    // r
    0x7C, 0x08, 0x04, 0x04, 0x08,
    // s
    0x48, 0x54, 0x54, 0x54, 0x20,
    // t
    0x04, 0x3F, 0x44, 0x40, 0x20,
    // u
    0x3C, 0x40, 0x40, 0x20, 0x7C,
    // v
    0x1C, 0x20, 0x40, 0x20, 0x1C,
    // w
    0x3C, 0x40, 0x30, 0x40, 0x3C,
    // x
    0x44, 0x28, 0x10, 0x28, 0x44,
    // y
    0x0C, 0x50, 0x50, 0x50, 0x3C,
    // z
    0x44, 0x64, 0x54, 0x4C, 0x44,
    // {
    0x00, 0x08, 0x36, 0x41, 0x00,
    // |
    0x00, 0x00, 0x7F, 0x00, 0x00,
    // }
    0x00, 0x41, 0x36, 0x08, 0x00,
    // ~
    0x08, 0x08, 0x2A, 0x1C, 0x08
};
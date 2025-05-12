#include "display_init.h"
#include "st7735.h"
#include <bcm2835.h>
#include <stdio.h>

extern "C" void initialize_display() {
    if(!bcm2835_init()) {
        printf("BCM2835 init failed!\n");
        return;
    }
    // Настройка SPI
    bcm2835_spi_begin();
    bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);
    bcm2835_spi_setDataMode(BCM2835_SPI_MODE0);
    bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_64);

    // Настройка GPIO
    bcm2835_gpio_fsel(DC_PIN, BCM2835_GPIO_FSEL_OUTP);
    bcm2835_gpio_fsel(RST_PIN, BCM2835_GPIO_FSEL_OUTP);

    // Инициализация дисплея
    st7735_init();
}
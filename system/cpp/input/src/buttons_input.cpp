#include <bcm2835.h>
#include <stdint.h>
#include <cstring>

extern "C" {

static const uint8_t* pins = nullptr;
static const char** names = nullptr;
static int count = 0;

bool initialize_buttons(const uint8_t* pin_array, const char** name_array, int pin_count) {

    pins = pin_array;
    names = name_array;
    count = pin_count;

    for (int i = 0; i < count; ++i) {
        bcm2835_gpio_fsel(pins[i], BCM2835_GPIO_FSEL_INPT);
        bcm2835_gpio_set_pud(pins[i], BCM2835_GPIO_PUD_UP);
    }
    return true;
}

// Возвращает имя нажатой кнопки или "" если нет
const char* get_button_action() {
    if (!pins || !names || count == 0)
        return "";

    for (int i = 0; i < count; ++i) {
        if (bcm2835_gpio_lev(pins[i]) == LOW) {
            // Подождём 10–20 мс и проверим снова (дребезг)
            bcm2835_delay(20);
            if (bcm2835_gpio_lev(pins[i]) == LOW) {
                return names[i];
            }
        }
    }
    return "";
}

}

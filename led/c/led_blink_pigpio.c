#include <stdio.h>
#include <pigpio.h>

#define GPIO_LED 18

int main() {
    if (gpioInitialise() == PI_INIT_FAILED) {
        printf("ERROR: Failed to initialize the GPIO interface.\n");
        return 1;
    }
    gpioSetMode(GPIO_LED, PI_OUTPUT);
    printf("Start blinking for 10 times...\n");
    for(int i = 0; i < 10; i++) {
        gpioWrite(GPIO_LED, PI_HIGH);
        time_sleep(1);
        gpioWrite(GPIO_LED, PI_LOW);
        time_sleep(1);
    }
    gpioSetMode(GPIO_LED, PI_INPUT);
    gpioTerminate();
    printf("Done!\n");

    return 0;
}

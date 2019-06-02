#include "lcd.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main()   {
    char line1[16], line2[16];
    char days[][16] = { "Son", "Mon", "Die", "Mit", "Don", "Fri", "Sam" };

    i2c_setup(I2C_ADDR);
    lcd_init(); // setup LCD

    while(1) {
        time_t T = time(NULL);
        struct  tm tm = *localtime(&T);

        sprintf(line1, "    %02d:%02d:%02d",tm.tm_hour, tm.tm_min, tm.tm_sec);
        sprintf(line2, " %03s %02d.%02d.%04d",days[tm.tm_wday], tm.tm_mday, tm.tm_mon+1, tm.tm_year+1900);

        //lcd_clear();
        lcd_write_line(1, line1);
        lcd_write_line(2, line2);
        delay(1000);
    }
    return 0;
}


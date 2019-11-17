#include "../lcd-hd44780/lcd.h"
#include "mpc_command.h"
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <unistd.h>


int main()   {
    int fd_lcd;
    char line[4][21];
    MpcPlaylist playlist;
    MpcStation station_info;
    int station_count = mpc_get_playlist(&playlist);
    memset(line[0], ' ', 20);
    char days[][3] = { "So", "Mo", "Di", "Mi", "Do", "Fr", "Sa" };

    fd_lcd = i2c_setup(I2C_ADDR);
    lcd_init(fd_lcd); // setup LCD

    mpc_play_station(6, &station_info);
    mpc_set_volume(50);

    while(1) {
        time_t T = time(NULL);
        struct  tm tm = *localtime(&T);

        sprintf(line[0], "%02d:%02d  %02s,%02d.%02d.%02d",
                tm.tm_hour, tm.tm_min, days[tm.tm_wday],tm.tm_mday, tm.tm_mon+1, tm.tm_year+1900);
        memset(line[1], ' ', 20);
        memset(line[2], ' ', 20);
        memset(line[3], ' ', 20);
        mpc_get_info(&station_info);

        if(strlen(station_info.station) >= 20)
            station_info.station[20] = 0;
        if(strlen(station_info.info1) >= 20)
            station_info.info1[20] = 0;
        if(strlen(station_info.info2) >= 20)
            station_info.info2[20] = 0;

        if(station_info.station[0] != 0)
            memcpy(line[1], station_info.station, strlen(station_info.station));
        if(station_info.info1[0] != 0)
            memcpy(line[2], station_info.info1, strlen(station_info.info1));
        if(station_info.info2[0] != 0)
            memcpy(line[3], station_info.info2, strlen(station_info.info2));

        line[0][20] = 0;
        line[1][20] = 0;
        line[2][20] = 0;
        line[3][20] = 0;

        printf("%02d  %s *\n", strlen(line[0]), line[0]);
        printf("%02d  %s *\n", strlen(line[1]), line[1]);
        printf("%02d  %s *\n", strlen(line[2]), line[2]);
        printf("%02d  %s *\n", strlen(line[3]), line[3]);

        lcd_write_line(fd_lcd, 1, line[0]);
        lcd_write_line(fd_lcd, 2, line[1]);
        lcd_write_line(fd_lcd, 3, line[2]);
        lcd_write_line(fd_lcd, 4, line[3]);

        sleep(1);
    }
    return 0;
}

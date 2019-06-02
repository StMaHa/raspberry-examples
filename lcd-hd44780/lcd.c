#include "lcd.h"
#include <fcntl.h>
#include <time.h>
#include <sys/time.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <linux/i2c.h>

/*
 * Clear lcd display
 */
void lcd_clear(int fd_lcd) {
    lcd_access(fd_lcd, 0x01, LCD_CMD);
    lcd_access(fd_lcd, 0x02, LCD_CMD);
}

/*
 * Write text line to lcd display
 */
void lcd_write_line(int fd_lcd, int line, const char *text)   {
    if(line == 1)
        lcd_access(fd_lcd, LCD_LINE1, LCD_CMD);
    if(line == 2)
        lcd_access(fd_lcd, LCD_LINE2, LCD_CMD);
    if(line == 3)
        lcd_access(fd_lcd, LCD_LINE3, LCD_CMD);
    if(line == 4)
        lcd_access(fd_lcd, LCD_LINE4, LCD_CMD);
    while( *text )
        lcd_access(fd_lcd, *(text++), LCD_REG_SELECT);
}

/*
 * Send byte to data pins nibble wise
 */
void lcd_access(int fd_lcd, int cmd, int mode)   {
    int nibbles[2];
    // writes nibbles (two half bytes) to LCD
    nibbles[0] = mode | (cmd & 0xF0);
    nibbles[1] = mode | ((cmd << 4) & 0xF0);

    // loop through nibbles (high bits first)
    for(int i= 0; i < 2; i++) {
        lcd_i2c_access(fd_lcd, nibbles[i] | LCD_BACKLIGHT);
        delay_microseconds(500);
        // clocks EN to latch command
        lcd_i2c_access(fd_lcd, (nibbles[i] | LCD_ENABLE | LCD_BACKLIGHT));
        delay_microseconds(500);
        lcd_i2c_access(fd_lcd, (nibbles[i] & ~LCD_ENABLE | LCD_BACKLIGHT));
        delay_microseconds(1000);
    }
}

/*
 * Initialise LCD display
 */
void lcd_init(int fd) {
    lcd_access(fd, 0x03, LCD_CMD); // Initialise
    lcd_access(fd, 0x03, LCD_CMD); // Initialise
    lcd_access(fd, 0x03, LCD_CMD); // Initialise
    lcd_access(fd, 0x02, LCD_CMD); // Initialise
    lcd_access(fd, LCD_FUNCTIONSET | LCD_2LINE |
               LCD_5x8DOTS | LCD_4BITMODE, LCD_CMD); // Data length, number of lines, font size
    lcd_access(fd, LCD_DISPLAYCONTROL | LCD_DISPLAYON, LCD_CMD); // 0x0F On, Blink Off
    lcd_access(fd, LCD_CLEARDISPLAY, LCD_CMD); // Clear display
    delay_microseconds(500);
}

/*
 * Access lcd via i2c
 */
int lcd_i2c_access(int fd_lcd, int command) {
    union i2c_smbus_data data;
    struct i2c_smbus_ioctl_data args;

    args.read_write = I2C_SMBUS_READ;
    args.command    = command;
    args.size       = I2C_SMBUS_BYTE_DATA;
    args.data       = &data;

    if(ioctl(fd_lcd, I2C_SMBUS, &args))
      return -1;
    else
      return data.byte & 0xFF;
}

/*
 * Setup I2C (get file descriptor for device)
 */
int i2c_setup(const int address) {
    int fd_lcd;
    const char *device ;
    //device = "/dev/i2c-0";
    device = "/dev/i2c-1";

    if ((fd_lcd = open (device, O_RDWR)) < 0)
        return -1;

    if (ioctl (fd_lcd, I2C_SLAVE, address) < 0)
        return -1;
    return fd_lcd;
}

/*
 * Delay program flow for seconds
 */
void delay(unsigned int time) {
    struct timespec delay, dummy;

    delay.tv_sec  = (time_t)(time / 1000);
    delay.tv_nsec = (long)(time % 1000) * 1000000;
    nanosleep(&delay, &dummy);
}

/*
 * Delay program flow for micro seconds
 */
void delay_microseconds(unsigned int time) {
    unsigned int micro_seconds = time % 1000000;
    unsigned int seconds = time / 1000000;

    if (time == 0)
        return;
    else if (time < 100) {
        struct timeval time_now, time_long, time_end;
        gettimeofday (&time_now, NULL);
        time_long.tv_sec  = seconds;
        time_long.tv_usec = micro_seconds;
        timeradd (&time_now, &time_long, &time_end);
        while (timercmp (&time_now, &time_end, <))
            gettimeofday (&time_now, NULL);
    } else {
        struct timespec delay;
        delay.tv_sec  = seconds;
        delay.tv_nsec = (long)(micro_seconds * 1000L);
        nanosleep (&delay, NULL);
    }
}


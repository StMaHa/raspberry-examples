#!/usr/bin/python
from smbus2 import SMBus
from time import sleep


# Define some LCD device parameters
LCD_1602_LINE_LENGTH = 16
LCD_1602_LINE_COUNT  =  2
LCD_2004_LINE_LENGTH = 20
LCD_2004_LINE_COUNT  =  4

# LCD command register addresses
LCD_CLEARDISPLAY   = 0x01
LCD_RETURNHOME     = 0x02
LCD_ENTRYMODESET   = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT    = 0x10
LCD_FUNCTIONSET    = 0x20
LCD_SETCGRAMADDR   = 0x40
LCD_SETDDRAMADDR   = 0x80

# LCD flags for display on/off control
LCD_DISPLAYON  = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON   = 0x02
LCD_CURSOROFF  = 0x00
LCD_BLINKON    = 0x01
LCD_BLINKOFF   = 0x00

# LCD lines
LCD_LINE1 = 0x80  # 1st line
LCD_LINE2 = 0xC0  # 2nd line
LCD_LINE3 = 0x94  # 3rd line
LCD_LINE4 = 0xD4  # 4th line

# LCD flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE  = 0x00
LCD_MOVERIGHT   = 0x04
LCD_MOVELEFT    = 0x00

# LCD flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE    = 0x08
LCD_1LINE    = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS  = 0x00

LCD_BACKLIGHT   = 0x08  # On
LCD_NOBACKLIGHT = 0x00  # Off

LCD_ENABLE     = 0b00000100  # Enable bit
LCD_REG_SELECT = 0b00000001  # Register select bit
LCD_CMD        = 0           # Mode - Sending command

'''
I2C device bus (1 or 0 for Pi rev.1)
I2C device address (execute: i2cdetect -y 1 or i2cdetect -y 0 for Pi rev.1)
'''
class HD44780:
    # initialises objects and lcd
    def __init__(self, i2c_bus = 1, i2c_address = 0x3f, lcd_line_count = LCD_1602_LINE_COUNT):
        if lcd_line_count == LCD_1602_LINE_COUNT:
            self.__lcd_line_length = LCD_1602_LINE_LENGTH
        elif lcd_line_count == LCD_2004_LINE_COUNT:
            self.__lcd_line_length = LCD_2004_LINE_LENGTH
        else:
            raise ValueError('Error! Only 2 (LCD1602) or 4 (LCD2004) lines are supported.')
        self.__lcd_line_count = lcd_line_count
        self.__lcd_lines = [LCD_LINE1, LCD_LINE2, LCD_LINE3, LCD_LINE4]
        # Open I2C interface
        self.__bus = SMBus(i2c_bus)
        self.__i2c_addr = i2c_address
        # initialises lcd
        self.__lcd_i2c_write(0x03,LCD_CMD)  # Initialise
        self.__lcd_i2c_write(0x03,LCD_CMD)  # Initialise
        self.__lcd_i2c_write(0x03,LCD_CMD)  # Initialise
        self.__lcd_i2c_write(0x02,LCD_CMD)  # Initialise
        self.__lcd_i2c_write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE, LCD_CMD)  # Data length, number of lines, font size
        self.__lcd_i2c_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON, LCD_CMD)  # 0x0F On, Blink Off
        self.__lcd_i2c_write(LCD_CLEARDISPLAY, LCD_CMD)  # Clear display
        sleep(0.0005)

    # Write data to lcd via i2c
    def __lcd_i2c_write(self, cmd, mode):
        nibbles = [mode | (cmd & 0xF0), mode | ((cmd << 4) & 0xF0)]

        for i in range(len(nibbles)):
            # High bits / low bits
            self.__bus.write_byte(self.__i2c_addr, nibbles[i] | LCD_BACKLIGHT)
            sleep(0.0005)
            self.__bus.write_byte(self.__i2c_addr, nibbles[i] | LCD_ENABLE | LCD_BACKLIGHT)
            sleep(0.0005)
            self.__bus.write_byte(self.__i2c_addr, nibbles[i] & ~LCD_ENABLE | LCD_BACKLIGHT)
            sleep(0.0005)

    # Send text to display
    def lcd_write_line(self, text, line):
        if line > self.__lcd_line_count:
            raise ValueError("ERROR! The line count exceeds the maximum count of {self.__lcd_line_count}.")
        if len(text) > self.__lcd_line_length:
            raise ValueError(f"ERROR! The text line length exceeds the maximum length of {self.__lcd_line_length}.")
        # set line to write text to
        self.__lcd_i2c_write(self.__lcd_lines[line - 1], LCD_CMD)
        # write text byte by byte
        for i in range(len(text)):
            self.__lcd_i2c_write(ord(text[i]), LCD_REG_SELECT)

    # Clear display
    def lcd_clear(self):
        self.__lcd_i2c_write(LCD_CLEARDISPLAY, LCD_CMD)
        self.__lcd_i2c_write(LCD_RETURNHOME, LCD_CMD)


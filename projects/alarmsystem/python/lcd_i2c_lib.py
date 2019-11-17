#!/usr/bin/python
import smbus
import time


# Define some LCD device parameters
LCD_1602_LINE_LENGTH = 16
LCD_1602_LINE_COUNT  =  2
LCD_2004_LINE_LENGTH = 20
LCD_2004_LINE_COUNT  =  4

LCD_LINE_LENGTH = LCD_1602_LINE_LENGTH
LCD_LINE_COUNT  = LCD_1602_LINE_COUNT

# Define some I2C device parameters as default (/dev/i2c-1 or /dev/i2c-0 for Pi rev.1)
I2C_ADDR  = 0x27  # I2C device address (execute: i2cdetect -y 1 or i2cdetect -y 0 for Pi rev.1)
I2C_BUS   =    1  # I2C device bus (1 or 0 for Pi rev.1)

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


class lcd:
    # initialises objects and lcd
    def __init__(self, i2c_address=I2C_ADDR, i2c_bus=I2C_BUS, lcd_line_length=LCD_LINE_LENGTH, lcd_line_count=LCD_LINE_COUNT):
        self.lcd_lines = [LCD_LINE1, LCD_LINE2, LCD_LINE3, LCD_LINE4]
        self.lcd_line_length = lcd_line_length
        self.lcd_line_count = lcd_line_count
        #Open I2C interface
        self.bus = smbus.SMBus(i2c_bus)
        self.i2c_addr = i2c_address
        # initialises lcd
        self.lcd_access(0x03,LCD_CMD)  # Initialise
        self.lcd_access(0x03,LCD_CMD)  # Initialise
        self.lcd_access(0x03,LCD_CMD)  # Initialise
        self.lcd_access(0x02,LCD_CMD)  # Initialise
        self.lcd_access(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE, LCD_CMD)  # Data length, number of lines, font size
        self.lcd_access(LCD_DISPLAYCONTROL | LCD_DISPLAYON, LCD_CMD)  # 0x0F On, Blink Off
        self.lcd_access(LCD_CLEARDISPLAY, LCD_CMD)  # Clear display
        time.sleep(0.0005)

    # Access lcd via i2c
    def lcd_access(self, cmd, mode):
        nibbles = [mode | (cmd & 0xF0), mode | ((cmd << 4) & 0xF0)]

        for i in range(len(nibbles)):
            # High bits / low bits
            self.bus.write_byte(self.i2c_addr, nibbles[i] | LCD_BACKLIGHT)
            time.sleep(0.0005)
            self.bus.write_byte(self.i2c_addr, nibbles[i] | LCD_ENABLE | LCD_BACKLIGHT)
            time.sleep(0.0005)
            self.bus.write_byte(self.i2c_addr, nibbles[i] & ~LCD_ENABLE | LCD_BACKLIGHT)
            time.sleep(0.0005)

    # Send text to display
    def lcd_write_line(self, text, line):
        if line > self.lcd_line_count:
            print("ERROR! Line is out of range.")
            return;
        if len(text) > self.lcd_line_length:
            print("ERROR! Text is out of range.")
            return;
        # set line to write text to
        self.lcd_access(self.lcd_lines[line - 1], LCD_CMD)
        # write text byte by byte
        for i in range(len(text)):
            self.lcd_access(ord(text[i]), LCD_REG_SELECT)

    # Clear display
    def lcd_clear(self):
        self.lcd_access(LCD_CLEARDISPLAY, LCD_CMD)
        self.lcd_access(LCD_RETURNHOME, LCD_CMD)


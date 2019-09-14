// header file for lcd.c
#ifndef LCD_H
#define LCD_H

// Define some LCD device parameters
#define LCD_1602_LINE_LENGTH  16
#define LCD_1602_LINE_COUNT    2
#define LCD_2004_LINE_LENGTH  20
#define LCD_2004_LINE_COUNT    4

// Define some I2C device parameters
#define I2C_ADDR   0x27         // I2C device address
#define I2C_SLAVE  0x0703
#define I2C_SMBUS  0x0720   // SMBus-level access

#define I2C_SMBUS_READ       1
#define I2C_SMBUS_WRITE      0
#define I2C_SMBUS_BYTE_DATA  2
#define I2C_SMBUS_BLOCK_MAX 32      // As specified in SMBus standard

// LCD command register addresses
#define LCD_CLEARDISPLAY   0x01
#define LCD_RETURNHOME     0x02
#define LCD_ENTRYMODESET   0x04
#define LCD_DISPLAYCONTROL 0x08
#define LCD_CURSORSHIFT    0x10
#define LCD_FUNCTIONSET    0x20
#define LCD_SETCGRAMADDR   0x40
#define LCD_SETDDRAMADDR   0x80

// LCD flags for display entry modes
#define LCD_ENTRYRIGHT           0x00
#define LCD_ENTRYLEFT            0x02
#define LCD_ENTRYSHIFTINCREMENT  0x01
#define LCD_ENTRYSHIFTDECREMENT  0x00

// LCD flags for display on/off control
#define LCD_DISPLAYON  0x04
#define LCD_DISPLAYOFF 0x00
#define LCD_CURSORON   0x02
#define LCD_CURSOROFF  0x00
#define LCD_BLINKON    0x01
#define LCD_BLINKOFF   0x00

// LCD lines
#define LCD_LINE1      0x80 // 1st line
#define LCD_LINE2      0xC0 // 2nd line
#define LCD_LINE3      0x94 // 3rd line
#define LCD_LINE4      0xD4 // 4th line

// LCD flags for display/cursor shift
#define LCD_DISPLAYMOVE 0x08
#define LCD_CURSORMOVE  0x00
#define LCD_MOVERIGHT   0x04
#define LCD_MOVELEFT    0x00

// LCD flags for function set
#define LCD_8BITMODE    0x10
#define LCD_4BITMODE    0x00
#define LCD_2LINE       0x08
#define LCD_1LINE       0x00
#define LCD_5x10DOTS    0x04
#define LCD_5x8DOTS     0x00

#define LCD_BACKLIGHT   0x08  // On
#define LCD_NOBACKLIGHT 0x00  // Off

#define LCD_ENABLE     0b00000100  // Enable bit
#define LCD_RW         0b00000010  // Read/Write bit
#define LCD_REG_SELECT 0b00000001  // Register select bit
#define LCD_CMD        0           // Mode - Sending command


// functions
int i2c_setup(const int address);

void lcd_init(int fd_lcd);
void lcd_access(int fd_lcd, int cmd, int mode);
void lcd_write_line(int fd_lcd, int line, const char *text);
void lcd_clear(int fd_lcd);
int  lcd_i2c_access(int fd_lcd, int cmd);

#endif /* LCD_H */

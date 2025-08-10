# LCD HD44780 (1602 / 2004) with I2C interface

Example *lcd_clock.py* will show time and date on the display.

# How to use it
Get I2C buses...
```bash
ls /dev/i2c*
```
You may receive:
/dev/i2c-**1**

Get I2C address by bus number...
```bash
i2cdetect -y 1
```
You may receive a number like 27 or 3F, these are hex numbers 0x27 or 0x3F
```python
import lcd_i2c_lib as LCD

lcd = LCD.lcd()  # will use defaul values
# or
lcd = LCD.lcd(i2c_address=0x27, i2c_bus=1)
```

# LICENSE
See the [LICENSE](../../LICENSE.md) file for license rights and limitations.

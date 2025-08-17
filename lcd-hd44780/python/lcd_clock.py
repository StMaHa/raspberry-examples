#!/usr/bin/python
import time
from hd44780 import HD44780 as LCD

# Initialise display
lcd = LCD()

try:
    while True:
        # Send date and time
        lcd.lcd_write_line(time.strftime("    %H:%M:%S", time.localtime()), 1)
        lcd.lcd_write_line(time.strftime(" %a %d.%m.%Y ", time.localtime()), 2)
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    lcd.lcd_clear()
    print("Program aborted.")




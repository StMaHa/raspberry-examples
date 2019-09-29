#!/usr/bin/python
import time
import lcd_i2c_lib as lcd

# Initialise display
lcd = lcd.lcd()

def clock():
    # Main program block
    while True:
        # Send date and time
        lcd.lcd_write_line(time.strftime("    %H:%M:%S", time.localtime()), 1)
        lcd.lcd_write_line(time.strftime(" %a %d.%m.%Y ", time.localtime()), 2)
        time.sleep(1)


try:
    clock()
except KeyboardInterrupt:
    pass
finally:
    lcd.lcd_clear()




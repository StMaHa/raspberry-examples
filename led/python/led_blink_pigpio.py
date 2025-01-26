# Beispiel mit pigpio library
#
# ATTENTION:
# Start pigpio daemon first:
# sudo systemctl start pigpiod
#
print("Daemon pigpiod is not supported on Raspberry Pi 5.")

import pigpio
from time import sleep

GPIO_LED = 21

gpio = pigpio.pi()
gpio.set_mode(GPIO_LED, pigpio.OUTPUT)

print("Start blinking...")
print("Press CTRL-C to stop.")

try:
    while(True):
        gpio.write(GPIO_LED, True)
        sleep(0.5)
        gpio.write(GPIO_LED, False)
        sleep(0.5)
except KeyboardInterrupt:
    pass

print("Done!")

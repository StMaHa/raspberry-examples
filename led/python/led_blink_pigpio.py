# Beispiel mit pigpio library
#
# ATTENTION:
# Start pigpio daemon first:
# sudo systemctl status pigpiod
#
import pigpio
from time import sleep

GPIO_LED = 18

gpio = pigpio.pi()
gpio.set_mode(GPIO_LED, pigpio.OUTPUT)
while(True):
    gpio.write(GPIO_LED, True)
    sleep(0.5)
    gpio.write(GPIO_LED, False)
    sleep(0.5)
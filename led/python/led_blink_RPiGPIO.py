# Beispiel mit Rpi.GPIO library
import RPi.GPIO as GPIO
from time import sleep

GPIO_LED = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_LED, GPIO.OUT)

try:
    while(True):
        GPIO.output(GPIO_LED, GPIO.LOW)
        sleep(0.5)
        GPIO.output(GPIO_LED, GPIO.HIGH)
        sleep(0.5)
except KeyboardInterrupt:
    GPIO.output(GPIO_LED, GPIO.LOW)
    GPIO.cleanup()


import RPi.GPIO as GPIO
import time

PIN_PIR = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_PIR, GPIO.IN)

def callback_function(channel):
    print("Motion detected.")

try:
    GPIO.add_event_detect(PIN_PIR , GPIO.RISING, callback=callback_function)
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("END")
GPIO.cleanup()

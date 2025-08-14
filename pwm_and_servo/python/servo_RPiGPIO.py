# Beispiel mit Rpi.GPIO library
import RPi.GPIO as GPIO
from time import sleep

GPIO_SERVO = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_SERVO, GPIO.OUT)

pwm = GPIO.PWM(GPIO_SERVO, 50) # GPIO 18 als PWM mit 50Hz
pwm.start(12) # Initialisierung (Duty Cylce)

print("Start turning...")
print("Press CTRL-C to stop.")

try:
    while(True):
        print("0 Grad")
        pwm.ChangeDutyCycle(12)
        sleep(1)
        print("90 Grad")
        pwm.ChangeDutyCycle(8)
        sleep(1)
        print("180 Grad")
        pwm.ChangeDutyCycle(4)
        sleep(1)
        print("90 Grad")
        pwm.ChangeDutyCycle(8)
        sleep(1)
except KeyboardInterrupt:
    pwm.ChangeDutyCycle(12)
    pwm.stop()
    GPIO.cleanup()

print("Done!")

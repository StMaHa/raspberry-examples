# Beispiel mit AngularServo und PiGPIOFactory aus der gpiozero library
#
# ATTENTION:
# Start pigpio daemon first:
# sudo systemctl start pigpiod
#

print("Daemon pigpiod is not supported on Raspberry Pi 5.")

from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from time import sleep

factory = PiGPIOFactory()
# Dreht nur im Winkel von 90 Grad
#servo = AngularServo(18, min_angle=-90, max_angle=90, pin_factory=factory)
servo = AngularServo(18,
                     min_angle=-90,
                     max_angle=90,
                     min_pulse_width=0.0007,
                     max_pulse_width=0.0023,
                     pin_factory=factory)

print("Start turning...")
print("Press CTRL-C to stop.")

try:
    while True:
        servo.angle= -90
        sleep(1)
        servo.angle = 0
        sleep(1)
        servo.angle = 90
        sleep(1)
        servo.angle = 0
        sleep(1)
except KeyboardInterrupt:
    servo.angle = 0
    servo = None

print("Done!")

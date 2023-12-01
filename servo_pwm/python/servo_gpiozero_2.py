# Beispiel mit Servo und PiGPIOFactory aus der gpiozero library
#
# ATTENTION:
# Start pigpio daemon first:
# sudo systemctl start pigpiod
#
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
from time import sleep

factory = PiGPIOFactory()
# Dreht nur im Winkel von 90 Grad
#servo = Servo(18)
servo = Servo(18,
              min_pulse_width=0.0007,
              max_pulse_width=0.0023,
              pin_factory=factory)

print("Start turning...")
print("Press CTRL-C to stop.")

try:
    while True:
        servo.max()
        sleep(1)
        servo.mid()
        sleep(1)
        servo.min()
        sleep(1)
        servo.mid()
        sleep(1)
except KeyboardInterrupt:
    servo.mid()
    servo = None

print("Done!")


# Beispiel mit Servo

from gpiozero import Servo
from time import sleep

# Dreht nur im Winkel von 90 Grad
#servo = Servo(18)
servo = Servo(18,
              min_pulse_width=0.0007,
              max_pulse_width=0.0023)

print("Start turning...")
print("Press CTRL-C to stop.")

try:
    while True:
        servo.max()
        sleep(2)
        servo.mid()
        sleep(2)
        servo.min()
        sleep(2)
        servo.mid()
        sleep(2)
except KeyboardInterrupt:
    servo.mid()
    servo = None

print("Done!")


# motor.py verwendet den Service von ‚pigpio‘

# Bibliotheken und Klassen
from gpiozero import Motor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# Globale Variablen
# GPIOs zur Ansteuerung der Motoren
pin_m1a = 16  # motor 1
pin_m1b = 20  # motor 1
pin_m2a = 19  # motor 2
pin_m2b = 26  # motor 2

my_factory = PiGPIOFactory()

motor1 = Motor(pin_m1a, pin_m1b, pwm=True, pin_factory = my_factory)
motor2 = Motor(pin_m2a, pin_m2b, pwm=True, pin_factory = my_factory)

motor1.forward()        # vollgas, oder motor.forward(1)
motor2.forward()
sleep(2)
motor1.forward(0.5)  # langsam
motor2.forward(0.5)
sleep(2)
motor1.forward(0)     # stillstand
motor2.forward(0)
sleep(2)
motor1.stop()             # motor aus
motor2.stop()

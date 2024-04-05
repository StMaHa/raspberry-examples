# Beispiel mit AngularServo und PiGPIOFactory aus der gpiozero library
#
# ATTENTION:
# Start pigpio daemon first:
# sudo systemctl start pigpiod
#
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from time import sleep

factory = PiGPIOFactory()

servo_horizontal = AngularServo(12,
                                min_angle=-90,
                                max_angle=90,
                                min_pulse_width=0.0007,
                                max_pulse_width=0.0023,
                                pin_factory=factory)
servo_horizontal.angle= 20
sleep(1)
servo_horizontal = None

servo_vertical = AngularServo(18,
                              min_angle=-90,
                              max_angle=90,
                              min_pulse_width=0.0007,
                              max_pulse_width=0.0023,
                              pin_factory=factory)
servo_vertical.angle= -73
sleep(1)
servo_vertical = None

print("Done!")

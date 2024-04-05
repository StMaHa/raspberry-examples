#!/usr/bin/python
# This is an example for the I2C device PCA9685
import sys
sys.path.append('../../pca9685/python')  # Add path to library of PCA9685

from PCA9685 import PWM
from time import sleep
import traceback

print("Start turning...")
print("Press CTRL-C to stop.")
try:
    pwm = PWM(frequency=50, servo_max_pulse_width=0.0026, servo_min_pulse_width=0.00065,
              servo_max_angle=90, servo_min_angle=-90)
    while True:
        pwm.change_servo_angle(0, 0)
        sleep(1)
        pwm.change_servo_angle(0, 90)
        sleep(1)
        pwm.change_servo_angle(0, 0)
        sleep(1)
        pwm.change_servo_angle(0, -90)
        sleep(1)

except (KeyboardInterrupt, ValueError) as e:
    pwm.change_servo_angle(0, 0)
    sleep(1)
    pwm.stop()
    print()
    if type(e) == ValueError:
        print(str(e))
    else:
        print("Done!")
except:
    traceback.print_exc()

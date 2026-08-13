from syspwm import SYSPWM
from time import sleep

PWM_FREQUENCY = 5000

pwm1 = SYSPWM(channel = 1, frequency = PWM_FREQUENCY)

try:
    print("Increase brightness using the PWM duty cycle in percentage.")
    for i in range(0, 100):
        pwm1.duty_cycle(i)
        sleep(0.1)
    sleep(1)
    print("Decrease brightness using the PWM duty cycle in percentage.")
    for i in range(100, 0, -1):
        pwm1.duty_cycle(i)
        sleep(0.1)
        
except KeyboardInterrupt:
    print("Program aborted.")
finally:
    pwm1.close()

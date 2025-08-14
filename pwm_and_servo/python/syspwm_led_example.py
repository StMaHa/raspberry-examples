from syspwm import SYSPWM
from time import sleep

pwm_frequency = 5000

pwm0 = SYSPWM()
pwm0.open()  # try to open again

pwm0.set_frequency(pwm_frequency)
pwm_period = pwm0.get_period_ns()  # Period in nano seconds

pwm0.enable()

try:
    for i in range(0, pwm_period):
        pwm0.set_pulse_width(i)
        sleep(0.00001)

    for i in range(0, 100):
        pwm0.set_duty_cycle(i)
        sleep(0.1)
        
except KeyboardInterrupt:
    print("Program aborted.")
pwm0.close()

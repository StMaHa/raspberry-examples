from syspwm import PWM
from time import sleep

PWM_FREQUENCY = 5000

# dtoverlay=pwm-2chan
# - chip = 0
# - channel = 0 for GPIO 12 / 18
# - channel = 1 for GPIO 13 / 19
# dtoverlay=pwm-pio (Pi 5 only)
# - chip = 1...4 depending on GPIO
# - channel = 0
led_pwm = PWM(chip = 0, channel = 1, frequency = PWM_FREQUENCY)

brightness_list = (0, 1, 2, 5, 10, 15, 20, 25, 50, 75, 100)

try:
    print("Increase brightness using the PWM duty cycle in percentage.")
    for i in brightness_list:  # 0% - 100%
        led_pwm.duty_cycle(i)
        sleep(0.5)
    sleep(1)
    print("Decrease brightness using the PWM duty cycle in percentage.")
    for i in reversed(brightness_list):  # 100% - 0%
        led_pwm.duty_cycle(i)
        sleep(0.5)
        
except KeyboardInterrupt:
    print("Program aborted.")
finally:
    led_pwm.close()
    print("Program finished.")

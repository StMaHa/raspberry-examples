from sysfs_pwm import PWM, Servo
from time import sleep

# dtoverlay=pwm-2chan
# - chip = 0
# - channel = 0 for GPIO 12 / 18
# - channel = 1 for GPIO 13 / 19
# dtoverlay=pwm-pio (Pi 5 only)
# - chip = 1...4 depending on GPIO
# - channel = 0

PWM_CHIP = 0
PWM_CHANNEL = 0
PWM_FREQUENCY = 50

servo = PWM(chip = PWM_CHIP, channel = PWM_CHANNEL, frequency = PWM_FREQUENCY, pulse_width = 0)  # Period: 0.02 secods = 20ms

try:
    print("Adjust the servo angle using the PWM duty cycle in percentage.")
    for i in range(0, 2):
        for duty_cycle in (2.5, 7.5, 12.5, 7.5):  # same as angle 0°, 90°, 180°, 90°
            servo.duty_cycle(duty_cycle)
            sleep(0.5)

    sleep(1)
    print("Adjust the servo angle using the PWM pulse width in secods.")
    for i in range(0, 2):
        for pulse_width in (0.0005, 0.0015, 0.0025, 0.0015):  # same as 7.5%, 12.5%, 7.5%, 2.5%
            servo.pulse_width(pulse_width)
            sleep(0.5)

    servo.close()
    sleep(1)

    print("Adjust the servo angle.")
    servo = Servo(pwm_chip = PWM_CHIP, pwm_channel = PWM_CHANNEL, pwm_frequency = PWM_FREQUENCY, pwm_pulse_width = 0,
                  pwm_min_pulse_width = 0.0005, pwm_max_pulse_width = 0.0025,
                  servo_min_angle = 0, servo_max_angle = 180)
    for i in range(0, 2):
        for servo_angle in (0, 90, 180, 90):
            servo.angle(servo_angle)
            sleep(0.5)
    servo.close()
except KeyboardInterrupt:
    print("Program aborted.")
finally:
    if servo and servo.is_active():
        servo.close()
    print("Program finished.")

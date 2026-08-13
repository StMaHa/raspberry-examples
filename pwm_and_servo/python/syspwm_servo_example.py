from syspwm import SYSPWM, Servo
from time import sleep


pwm0 = SYSPWM(frequency = 50)  # Period: 0.02 secods = 20ms
servo = None

try:
    print("Adjust the servo angle using the PWM duty cycle in percentage.")
    for i in range(0, 2):
        for duty_cycle in (2.5, 7.5, 12.5, 7.5):  # same as angle 0°, 90°, 180°, 90°
            pwm0.duty_cycle(duty_cycle)
            sleep(0.5)

    sleep(1)
    print("Adjust the servo angle using the PWM pulse width in secods.")
    for i in range(0, 2):
        for pulse_width in (0.0005, 0.0015, 0.0025, 0.0015):  # same as 7.5%, 12.5%, 7.5%, 2.5%
            pwm0.pulse_width(pulse_width)
            sleep(0.5)
            
    pwm0.close()
    sleep(1)
    print("Adjust the servo angle.")
    servo = Servo(frequency = 50, servo_pulse_width = 0,
                  servo_min_pulse_width = 0.0005, servo_max_pulse_width = 0.0025,
                  servo_min_angle = 0, servo_max_angle = 180)
    for i in range(0, 2):
        for servo_angle in (0, 90, 180, 90):
            servo.angle(servo_angle)
            sleep(0.5)
    servo.close()
except KeyboardInterrupt:
    print("Program aborted.")
finally:
    if pwm0 and pwm0.is_active():
        pwm0.close()
    if servo and pwm0.is_active():
        servo.close()

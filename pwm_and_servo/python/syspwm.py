import os
from time import sleep

class SYSPWM():
    PWM_SYSFS_CHIP_PATH = "/sys/class/pwm/pwmchip0"

    # Constructor
    def __init__(self, channel = 0, frequency = 50, duty_cycle = 0, pulse_width = 0):
        '''
        Option 1: supported on all Raspberry Pi's
        Add 'dtoverlay=pwm-2chan' to '/boot/firmware/config.txt'
        - PWM0: GPIO 12 and GPIO 18 (channel = 0)
        - PWM1: GPIO 13 and GPIO 19 (channel = 1)

        Option 2: supported only on Raspberry Pi 5
        Add 'dtoverlay=pwm-pio,gpio=18:' to '/boot/firmware/config.txt'
        All GPIO's possible, but reserves this IO for PWM only.
        PWM0 only (channel = 0)

        Parameter:
        - channel: 0 (PWM0), 1 (PWM1)
        - frequency: value in Herz
        - duty_cycle: value in percentage
        - pulse_width: value in seconds
        '''
        if not os.path.isdir(self.PWM_SYSFS_CHIP_PATH):
            raise Exception(
                "ERROR! PWM device tree overlay not not loaded.\n"
                "E.g. add 'dtoverlay=pwm-2chan' to '/boot/firmware/config.txt'\n"
                "and reboot Raspberry Pi."
                )
        if duty_cycle and pulse_width:
            raise ValueError("Set only one of the parameter: duty_cycle or pulse_width")

        self._pwm_channel = channel
        self._period_ns = 0
        self._is_open = False
        self._is_active = False
        self._open()
        self.frequency(frequency)

        if duty_cycle:
            self.set_duty_cycle(duty_cycle)
        if pulse_width:
            self.set_pulse_width_ns(pulse_width_ns)

    def _pwm_write_parameter(self, pwm_parameter, pwm_value):
        result = False
        # Since it is sysfs, previous step might take a moment until file is accessible
        for i in range(0, 10):  # retry up to 10 times with a delay 0.1 seconds
            try:
                if (pwm_parameter == "export") or (pwm_parameter == "unexport"):
                    pwm_file_path = os.path.join(self.PWM_SYSFS_CHIP_PATH, pwm_parameter)
                else:
                    pwm_file_path = os.path.join(self.PWM_SYSFS_CHIP_PATH, f"pwm{self._pwm_channel}", pwm_parameter)
                with open(pwm_file_path,'w') as f:
                    f.write(f"{pwm_value}\n")
                result = True
                break
            except:
                sleep(0.1)
        if result == False:
            print(f"Writing parameter '{pwm_value}' to file '{pwm_file_path}' failed.")
        return result

    def _open(self):
        '''
        Open PWM channel
        '''
        if not self._is_open:
            self._is_open = self._pwm_write_parameter("export", self._pwm_channel)
            self._is_open = True
        else:
            print("PWM channel already open.")

    def _set_pulse_width_ns(self, pulse_width):
        '''
        Set pulse width in nano seconds
        '''
        if pulse_width > self._period_ns:
            print("ERROR! Pulse width exceeds the period.")
        self._pwm_write_parameter("duty_cycle", int(pulse_width))
        self.on()

    def is_active(self):
        '''
        Returns PWM state.
        '''
        return self._is_active

    def off(self):
        '''
        Deactivate PWM signal
        '''
        self._pwm_write_parameter("enable", 0)
        self._is_active = False

    def close(self):
        '''
        Close PWM channel
        '''
        self.off()
        self._pwm_write_parameter("unexport", self._pwm_channel)
        self._is_open = False

    def on(self):
        '''
        Activate PWM signal
        '''
        if not self._is_active:  # write only if necessary
            self._pwm_write_parameter("enable", 1)
            self._is_active = True

    def pulse_width(self, pulse_width):
        '''
        Set pulse width in seconds
        '''
        self._set_pulse_width_ns(pulse_width * 1000000000)

    def duty_cycle(self, duty_cycle):
        '''
        Set duty cycle in percentage
        '''
        pulse_width = int(self._period_ns * duty_cycle / 100)
        self._set_pulse_width_ns(pulse_width)

    def period_ns(self, period):
        '''
        Set period in nano seconds
        '''
        self._period_ns = period
        self._pwm_write_parameter("period", period)
        
    def frequency(self, frequency):
        '''
        Set frequency in Hz
        '''
        self.period_ns(int((1 / frequency) * 1000000000))  # set period in nano seconds


class Servo():
    # Constructor
    def __init__(self, channel = 0, frequency = 50,
                 servo_pulse_width = 0, servo_angle = None,
                 servo_min_pulse_width = 0.001, servo_max_pulse_width = 0.002,
                 servo_min_angle = 0, servo_max_angle = 180):
        # Only one intial value is possible
        if servo_pulse_width and servo_angle:
            raise ValueError("Set only one of the parameter: servo_pulse_width or servo_angle")
        # Set class initial values
        self._servo_min_pulse_width = servo_min_pulse_width * 1000000000  # Pulse width in nano secods
        self._servo_max_pulse_width = servo_max_pulse_width * 1000000000  # Pulse width in nano secods
        self._servo_min_angle = servo_min_angle
        self._servo_max_angle = servo_max_angle
        # Prepare servo angle calculation (based on y = m * x + b -> pulse = m * angle + b)
        #   servo_min_pulse_width = m * servo_min_angle + b
        #   servo_max_pulse_width = m * servo_max_angle + b
        # Calculate servo pulse per angle: m = (pulse1 - pulse2) / (angle1 - angle2)
        self._servo_pulse_per_angle = (self._servo_max_pulse_width - self._servo_min_pulse_width) / (self._servo_max_angle - self._servo_min_angle)
        # Calculate servo pulse offset: b = pulse2 - m * angle2
        self._servo_pulse_offset = self._servo_max_pulse_width - self._servo_pulse_per_angle * self._servo_max_angle
        # Initialize PWM
        self._servo = SYSPWM(channel = channel, frequency = frequency, pulse_width = servo_pulse_width)
        # Set initial values
        if servo_angle:
            self.angle(servo_angle)
        
    def angle(self, angle):
        '''
        Adjust servo angle
        '''
        if(angle < self._servo_min_angle or angle > self._servo_max_angle):
            raise ValueError("Angle is out of range. Should be between {} and {} degree.".format(self._servo_min_angle, self._servo_max_angle))
        # Calculate pulse width
        pulse_ns = self._servo_pulse_per_angle * angle + self._servo_pulse_offset  # calculate pulse width in nano secods: y = mx + b
        self._servo._set_pulse_width_ns(pulse_ns)

    def pulse_width(self, pulse_width):
        '''
        Adjust pulse width in seconds
        '''
        self._servo.pulse_width(pulse_width)

    def on(self):
        '''
        Activate servo.
        '''
        return self._servo.on()

    def off(self):
        '''
        Deactivate servo.
        '''
        return self._servo.off()

    def is_active(self):
        '''
        Returns server state.
        '''
        return self._servo._is_active

    def close(self):
        self._servo.close()

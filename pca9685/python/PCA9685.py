#!/usr/bin/python
from smbus import SMBus  # I2C Bus
from time import sleep

#
# Python module for PCA9685: 16-channel, 12-bit PWM I2C-bus LED controller
#
class PWM:
    # Constants, e.g. registers, flags...
    __SUBADR1            = 0x02
    __SUBADR2            = 0x03
    __SUBADR3            = 0x04
    __MODE1              = 0x00
    __MODE2              = 0x01
    __PRE_SCALE          = 0xFE
    __LED0_ON_L          = 0x06
    __LED0_ON_H          = 0x07
    __LED0_OFF_L         = 0x08
    __LED0_OFF_H         = 0x09
    __ALL_LED_ON_L       = 0xFA
    __ALL_LED_ON_H       = 0xFB
    __ALL_LED_OFF_L      = 0xFC
    __ALL_LED_OFF_H      = 0xFD

    __RESTART            = 0x80
    __SLEEP              = 0x10
    __OUTDRV             = 0x04

    __LED_CHANNEL_OFFSET_FACTOR     = 4         # Offset to address LED1_ON/OFF_L/H to LED15_ON/OFF_L/H
    __INTERNAL_OSCILLATOR_FREQUENCY = 25000000  # 25 MHz
    __STEPS_PER_PERIOD              = 4096      # The PCA9685 has 4096 steps (12-bit PWM) of individual LED brightness control
    __DELAY_STABILIZE_OSCILLATOR    = 0.001     # 1ms to stabalize oscillator
    __PWM_MIN_FREQUENCY             = 24        # Minimal PWM frequency of PCA9685
    __PWM_MAX_FREQUENCY             = 1526      # Maximum PWM frequency of PCA9685
    __PCA9685_MAX_CHANNEL           = 15

    def __init__(self, address=0x40,  # standard address for PCA9685
                 i2c_bus_number=1,    # set to '1' for Raspberry Pi revisions 1B+/2/3/4/5, set to '0' for 1A/1B/1A+
                 frequency=50,        # standard frequency for servos
                 servo_min_pulse_width=0.001, servo_max_pulse_width=0.002,  # standard values for servos
                 servo_min_angle=0, servo_max_angle=180):
        "Init method / constructor of PWM class for PCA9685 module"
        self._logging = False
        self._frequency = frequency
        self._i2c_bus = SMBus(i2c_bus_number)
        self._address = address
        self._servo_max_pulse_width = servo_max_pulse_width * 1000000  # convert to micro seconds
        self._servo_min_pulse_width = servo_min_pulse_width * 1000000  # convert to micro seconds
        self._servo_max_angle = servo_max_angle
        self._servo_min_angle = servo_min_angle
        # Prepare servo angle calculation (based on y = m * x + b -> pulse = m * angle + b)
        #   servo_min_pulse_width = m * servo_min_angle + b
        #   servo_max_pulse_width = m * servo_max_angle + b
        # Calculate servo pulse per angle: m = (pulse1 - pulse2) / (angle1 - angle2)
        self._servo_pulse_per_angle = (self._servo_max_pulse_width - self._servo_min_pulse_width) / (self._servo_max_angle - self._servo_min_angle)
        # Calculate servo pulse offset: b = pulse2 - m * angle2
        self._servo_pulse_offset = self._servo_max_pulse_width - self._servo_pulse_per_angle * self._servo_max_angle
        # Initialize PWM
        self._write_byte_data(self.__MODE1, 0x00)
        self._set_pwm_frequency(self._frequency)  # set default frequency

    def _log(self, text):
        "Writes text to console"
        if self._logging:
            print(text)

    def _write_byte_data(self, register, value):
        "Writes a byte value to the I2C device"
        self._i2c_bus.write_byte_data(self._address, register, value)
        self._log("Write 0x%02X to register 0x%02X of I2C device 0x%02X" % (value, register, self._address))

    def _read_byte_data(self, register):
        "Read a byte value from the I2C device"
        result = self._i2c_bus.read_byte_data(self._address, register)
        self._log("I2C device 0x%02X returned 0x%02X from register 0x%02X" % (self._address, result, register))
        return result

    def _set_pwm(self, channel, on, off):
        "Sets PWM registers for a single channel"
        self._write_byte_data(self.__LED0_ON_L + self.__LED_CHANNEL_OFFSET_FACTOR * channel, on & 0xFF)
        self._write_byte_data(self.__LED0_ON_H + self.__LED_CHANNEL_OFFSET_FACTOR * channel, on >> 8)
        self._write_byte_data(self.__LED0_OFF_L + self.__LED_CHANNEL_OFFSET_FACTOR * channel, off & 0xFF)
        self._write_byte_data(self.__LED0_OFF_H + self.__LED_CHANNEL_OFFSET_FACTOR * channel, off >> 8)

    def _set_pwm_frequency(self, frequency):
        "Sets the PWM frequency"
        prescale = float(self.__INTERNAL_OSCILLATOR_FREQUENCY)  # internal 25 MHz oscillator
        prescale /= float(self.__STEPS_PER_PERIOD)              # steps, 12-bit PWM
        prescale /= float(frequency)                            # update rate
        prescale -= 1.0                                         # as defined in datasheet
        prescale_value = round(prescale, 0)                     # round to integer value

        old_mode = self._read_byte_data(self.__MODE1)  # remember initial state
        new_mode = (old_mode & ~self.__RESTART) | self.__SLEEP    # prepare bits for sleep (remove restart bit)
        self._write_byte_data(self.__MODE1, new_mode)  # go to sleep before setting prescale value
        self._write_byte_data(self.__PRE_SCALE, int(round(prescale_value, 0)))
        self._write_byte_data(self.__MODE1, old_mode)  # restore initial state
        sleep(self.__DELAY_STABILIZE_OSCILLATOR)
        self._write_byte_data(self.__MODE1, old_mode | self.__RESTART)
        self._write_byte_data(self.__MODE2, self.__OUTDRV)  # wake up / restart

    def enable_logging(self, enable):
        "Enables logging"
        self._logging = enable

    def change_pwm_frequency(self, frequency):
        "Changes the PWM frequency"
        if(frequency < self.__PWM_MIN_FREQUENCY and frequency > self.__PWM_MAX_FREQUENCY):
            raise ValueError("Frequency is out of range. Should be between {} Hz and {} Hz.".format(self.__PWM_MIN_FREQUENCY, self.__PWM_MAX_FREQUENCY))
        self._frequency = frequency
        self._set_pwm_frequency(frequency)

    def change_servo_angle(self, channel, angle):
        "Changes servo angle"
        if(angle < self._servo_min_angle or angle > self._servo_max_angle):
            raise ValueError("Angle is out of range. Should be between {} and {} degree.".format(self._servo_min_angle, self._servo_max_angle))
        if(channel < 0 or channel > self.__PCA9685_MAX_CHANNEL):
            raise ValueError("Channel is out of range. Should be between 0 and {}.".format(self.__PCA9685_MAX_CHANNEL))
        # Calculate duty cycle
        pulse = self._servo_pulse_per_angle * angle + self._servo_pulse_offset  # calculate pulse width: y = mx + b 
        period = 1000000 / self._frequency  # period in micro seconds (us)
        duty_cycle = 100 * pulse / period  # duty cycle in percentage
        self.change_duty_cycle(channel, duty_cycle)

    def change_duty_cycle(self, channel, duty_cycle):
        "Changes duty cycle between 0% and 100%"
        if(duty_cycle < 0 or duty_cycle > 100):
            raise ValueError("Duty cycle is out of range. Should be between 0% and 100%.")
        if(channel < 0 or channel > self.__PCA9685_MAX_CHANNEL):
            raise ValueError("Channel is out of range. Should be between 0 and {}.".format(self.__PCA9685_MAX_CHANNEL))
        led_on_step_count = duty_cycle * self.__STEPS_PER_PERIOD / 100
        self._set_pwm(channel, 0, int(led_on_step_count))

    def start(self):
        "Starts PWM output"
        self._write_byte_data(self.__MODE2, self.__OUTDRV)

    def stop(self):
        "Stops PWM output"
        self._write_byte_data(self.__MODE2, 0x00)


if __name__ == '__main__':
    print("This module is library only!")
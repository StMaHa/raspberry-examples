import os
from time import sleep

class SYSPWM():
    __pwm_chip_path = "/sys/class/pwm/pwmchip0"

    # Constructor
    def __init__(self,channel = 0, frequency = None):
        if not os.path.isdir(self.__pwm_chip_path):
            raise Exception("ERROR! PWM device tree overlay not not loaded.")

        self.__pwm_channel = channel
        self.__pwm_channel_path = f"{self.__pwm_chip_path}/pwm{self.__pwm_channel}"
        self.__frequency = frequency
        self.__is_open = False
        self.open()
        if self.__frequency:
            self.set_frequency(self.__frequency)

    def __pwm_write_parameter(self, pwm_file_path, pwm_parameter):
        result = False
        # Since it is sysfs, previous step might take a moment until file is accessible
        for i in range(0, 10):  # retry up to 10 times with a delay 0.1 seconds
            try:
                with open(pwm_file_path,'w') as f:
                    f.write(f"{pwm_parameter}\n")
                result = True
                break
            except:
                sleep(0.1)
        if result == False:
            print(f"Writing parameter '{pwm_parameter}' to file '{pwm_file_path}' failed.")
        return result

    def open(self):
        '''
        Open PWM channel
        '''
        if not self.__is_open:
            self.__is_open = self.__pwm_write_parameter(f"{self.__pwm_chip_path}/export", self.__pwm_channel)
        else:
            print("PWM channel already open.")

    def close(self):
        '''
        Close PWM channel
        '''
        self.__pwm_write_parameter(f"{self.__pwm_chip_path}/unexport", self.__pwm_channel)
        self.__is_open = False

    def enable(self):
        '''
        Enable PWM signal
        '''
        self.__pwm_write_parameter(f"{self.__pwm_channel_path}/enable", 1)

    def disable(self):
        '''
        Disable PWM signal
        '''
        self.__pwm_write_parameter(f"{self.__pwm_channel_path}/enable", 0)

    def set_pulse_width(self, pulse_width):
        '''
        pulse_width in nano seconds
        '''
        self.__pwm_write_parameter(f"{self.__pwm_channel_path}/duty_cycle", int(pulse_width))

    def set_duty_cycle(self, duty_cycle):
        '''
        duty_cycle in percentage
        '''
        period = self.get_period_ns()
        pulse_width = int(period * duty_cycle / 100)
        self.set_pulse_width(pulse_width)

    def set_period(self, period):
        '''
        period in nano seconds
        '''
        self.__frequency = int(1 / (period / 1000000000))
        self.__pwm_write_parameter(f"{self.__pwm_channel_path}/period", period)
        
    def get_period_ns(self):
        '''
        Returns period in nano seconds
        '''
        return int((1 / self.__frequency) * 1000000000)

    def set_frequency(self, frequency):
        '''
        frequency in Hz
        '''
        self.__frequency = frequency
        self.set_period(self.get_period_ns())  # set period in nano seconds

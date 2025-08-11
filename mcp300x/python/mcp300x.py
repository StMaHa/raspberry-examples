from spidev import SpiDev


# Internal parent class
class __MCP300X:
    def __init__(self, bus = 0, device = 0, frequency = 1000000, max_channels = 8):
        self.max_channels = max_channels
        self.bus = bus
        self.device = device
        self.open_flag = False
        self.spi = SpiDev()
        self.open()  # open before setting frequency
        self.spi.max_speed_hz = frequency

    def open(self):
        if not self.open_flag:
            # open spi bus
            self.spi.open(self.bus, self.device)
            self.open_flag = True

    def close(self):
        # close spi bus
        self.spi.close()
        self.open_flag = False

    def read(self, channel=0):
        # check value of channel
        if (channel >= self.max_channels) or (channel < 0):
            raise ValueError("Channel number is not valid.")
        if not self.open_flag:
            self.open()
        # send configuration data and receive analog value data
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        # Combine 10bits of 2 bytes
        analog_value = ((adc[1] & 3) << 8) + adc[2]
        return analog_value  # max 1023


class MCP3008(__MCP300X):
    def __init__(self, bus = 0, device = 0, frequency = 1000000):
        super().__init__(bus, device, frequency, 8)  # 8 channels


class MCP3004(__MCP300X):
    def __init__(self, bus = 0, device = 0, frequency = 1000000):
        super().__init__(bus, device, frequency, 4)  # 4 channels

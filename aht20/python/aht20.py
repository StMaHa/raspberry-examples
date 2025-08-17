'''
I2C driver class for AHT20 without checksum verification
'''
from smbus2 import SMBus
from time import sleep


# Constants
RESET_CMD_BYTE = [0xBA]
INITIALIZE_CMD_BYTES = [0xBE, 0x08, 0x00]
MEASURE_CMD_BYTES = [0xAC, 0x33, 0x00]
STATUS_BUSY_BIT = 7                    # The 7th bit is the Busy indication bit. 1 = Busy, 0 = not.
STATUS_CALIBRATED_BIT = 3              # The 3rd bit is the CAL (calibration) Enable bit. 1 = Calibrated, 0 = not

class AHT20:

    def __init__(self, i2c_bus_number = 1, i2c_address = 0x38, debug = False):
        '''
        Initialize sensor AHT20
        Reset and calibrates sensor
        '''
        self.__debug = debug
        self.__i2c_bus_number = i2c_bus_number
        self.__i2c_address = i2c_address
        self.__reset()

        # Check for calibration, if not done then do and wait 10 ms
        if not self.__get_status_calibrated():
            self.__initialize()
            while not self.__get_status_calibrated():
                sleep(0.01)
        
    def __reset(self):
        '''
        Send the command byte to reset sensor
        '''
        with SMBus(self.__i2c_bus_number) as i2c_bus:
            i2c_bus.write_i2c_block_data(self.__i2c_address, 0x0, RESET_CMD_BYTE)
        sleep(0.04)    # Wait 40 ms after poweron
        return True

    def __initialize(self):
        '''
        Sends the command bytes to initialize sensor
        Calibrate sensor
        '''
        with SMBus(self.__i2c_bus_number) as i2c_bus:
            i2c_bus.write_i2c_block_data(self.__i2c_address, 0x0 , INITIALIZE_CMD_BYTES)
        return True

    def __get_status_byte(self):
        '''
        Returns status byte
        '''
        status_byte = None
        # Get the full status byte
        with SMBus(self.__i2c_bus_number) as i2c_bus:
            status_byte = i2c_bus.read_i2c_block_data(self.__i2c_address, 0x0, 1)[0]
        return status_byte

    def __get_status_calibrated(self):
        '''
        Returns calibration state as True or False
        '''
        return bool((self.__get_status_byte() >> STATUS_CALIBRATED_BIT) & 1)

    def __get_status_busy(self):
        '''
        Returns busy state as True or False
        '''
        return bool((self.__get_status_byte() >> STATUS_BUSY_BIT) & 1)

    def __get_hex_list_from_int_list(self, int_list):
        hex_list = []

        for int_value in int_list:
            hex_list.append(f"0x{int_value:02X}")

        return hex_list

    def __measure(self):
        '''
        Sends the command bytes to measure temperature and humidity
        Returns data bytes
        '''
        # Open i2c bus, write command data and close i2c bus
        with SMBus(self.__i2c_bus_number) as i2c_bus:
            i2c_bus.write_i2c_block_data(self.__i2c_address, 0, MEASURE_CMD_BYTES)
        sleep(0.075) # wait 75 ms as required in the technical manual

        # Wait as long as device is still busy, wait for busy bit == 0
        while self.__get_status_busy():
            sleep(0.08) # wait 80 ms and retry

        # Open i2c bus, read data and close i2c bus
        data_bytes = None
        with SMBus(self.__i2c_bus_number) as i2c_bus:
            data_bytes = i2c_bus.read_i2c_block_data(self.__i2c_address, 0x0, 7)
        # Data bytes: first byte status + 2.5 bytes humidity value + 2.5 bytes temperature value + last byte checksum (crc8)
        # [SSSS SSSS][HHHH HHHH][HHHH HHHH][HHHH TTTT][TTTT TTTT][TTTT TTTT][CCCC CCCC]
        # [  0xSS   ][ 0xH1H2  ][ 0xH3H4  ][ 0xH5T1  ][ 0xT2T3  ][ 0xT4T5  ][  0xCC   ]
        return data_bytes

    def get_humidity(self):
        '''
        Measures temperature and humidity
        Returns humidity in percentage
        '''
        data_bytes = self.__measure()
        # Combine humidity bytes (20 bits) to one value
        # First byte contains the state and is not required for the humidity value
        # Take all 8 bits of second byte (highest byte of value)
        humidity_value = (data_bytes[1] << 12)           # byte 2: H1H2 shift to 0H1 H2x xx
        # Add all 8 bits of third byte
        humidity_value |= (data_bytes[2] << 4)           # byte 3: H3H4 shift and add to 0H1 H2H3 H4x
        # Add highest 4 bits of fourth byte (lowest bytes of value)
        humidity_value |= ((data_bytes[3] & 0xF0) >> 4)  # byte 4, highest 4 bits: H5T1 shift and add to 0H1 H2H3 H4H5
        if self.__debug:
            print(f"\nget_humidity: {self.__get_hex_list_from_int_list(data_bytes)} -> 0x{humidity_value:02X}")
        # Calculate the humidity according to the technical manual
        humidity_value = (humidity_value / pow(2,20)) * 100 

        return humidity_value

    def get_temperature(self):
        '''
        Measures temperature and humidity
        Returns temperature in degree Celsius
        '''
        data_bytes = self.__measure()
        # Combine temperature bytes (20 bits) to one value
        # First byte contains the state and is not required for the humidity value
        # Byte 2 to 4 contain humidity values (20 bits = 2.5 bytes)
        # Take lowest 4 bits of fourth byte (highest byte of value)
        temperature_value = ((data_bytes[3] & 0x0F) << 16)  # byte 2: H5T1 shift to 0T1 xx xx
        # Add all 8 bits of fifth byte
        temperature_value |= (data_bytes[4] << 8)           # byte 3: T2T3 shift and add to 0T1 T2T3 xx
        # Add all 8 bits of sixth byte (lowest bytes of value)
        temperature_value |= data_bytes[5]                  # byte 3: T4T5 add to 0T1 T2T3 T4T5
        if self.__debug:
            print(f"\nget_temperature: {self.__get_hex_list_from_int_list(data_bytes)} -> 0x{temperature_value:02X}")
        # Calculate the temperature according to the technical manual
        temperature_value = (temperature_value / pow(2,20)) * 200 - 50

        return temperature_value

'''
sudo apt update
sudo apt install python3-bme280
'''
# Example shows values of sensor BME280
# - Temperature in °C
# - Barometric  pressure in hPa on station level (sea level might be higher)
# - Relative humidity in %
import bme280
import smbus2
import time

i2c_bus_number = 1
i2c_address = 0x76
i2c_bus = smbus2.SMBus(i2c_bus_number)

print("BME280 example\n")
print("Program can be aborted by pressing [STRG]+[C] or [CTRL]+[C]\n")
print("Info: Atmospheric pressure is measured on station level\n")

bme280_calibration_data = bme280.load_calibration_params(i2c_bus, i2c_address)

try:
    while True:
        time.sleep(2)
        bme280_data = bme280.sample(i2c_bus, i2c_address, bme280_calibration_data)
        '''
        Available data:
        - bme280_data.id
        - bme280_data.timestamp
        - bme280_data.temperature
        - bme280_data.pressure
        - bme280_data.humidity
        '''
        print(f"""
{bme280_data.timestamp.strftime("%Y-%m-%d %H:%M:%S")}
  Temperature: {bme280_data.temperature:3.2f} °C
  Pressure:    {bme280_data.pressure:5.2f} hPa
  Humidity:    {bme280_data.humidity:5.2f} %""")
except KeyboardInterrupt:
    print("Program aborted.")

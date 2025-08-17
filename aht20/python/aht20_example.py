from aht20 import AHT20
from datetime import datetime
from time import sleep


aht20 = AHT20(debug=False)
# aht20 = AHT20(i2c_bus_number = 1, i2c_address = 0x38, debug = True)

try:
    while True:
        print(f"""
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Temperature: {aht20.get_temperature():3.2f} °C
Humidity:    {aht20.get_humidity():3.2f} %""")
        sleep(1)
except KeyboardInterrupt:
    pass

print("\nProgramm beendet")
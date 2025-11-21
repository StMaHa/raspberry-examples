# MCP3008 example using gpiozero module

from gpiozero import MCP3008
from time import sleep


spi_bus = 0
spi_device = 1  # CS1
adc_channel = 0

mcp3008 = MCP3008(port=spi_bus, device=spi_device, channel=adc_channel)

try:
    while True:
        voltage = mcp3008.raw_value / 1023 * 3.3
        print(f"Voltage: {voltage:1.2f} V")
        sleep(1)
except KeyboardInterrupt:
    print("Program aborted.")

mcp3008.close()
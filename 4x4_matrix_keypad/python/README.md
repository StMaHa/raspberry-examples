# Example for 4x4 keypad matrix using an analog-digital-converter MCP3008
The usage of an ADC will minimize the number of ICs to one.  
The Python library gpiozero already supports MCP3008 and its family.  
The MCP3008 is connected via the SPI interface to the Raspberry Pi.

## Description
- VDD = AREF = 3.3V
- The analog input channels must be pulled down with resistors at lease of 100k to minimize measurement failures.
- A voltage devider with 4 resistores of e.g. 1k (to minimize measurement failures) will be input for the column lines of the pinpad
  - R1 = R2 = R3 = R4 = 1k
  - Voltage devider connection: VDD--R1--R2--R3--R4--GND
  - col0 > 0.25 * VDD
  - col1 > 0.5 * VDD
  - col2 > 0.75 * VDD
  - col3 > 1 * VDD
- The row lines of the pin pad will be connected to the analog input channels of the ADC.
  - row0 > ch0
  - row1 > ch1
  - row2 > ch2
  - row3 > ch3
- PinPad connector, lines/pins from left to right:

| Pins | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| ---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **KeyPad** | row0 | row1 | row2 | row3 | col0 | col1 | col2 | col3 |
| **MCP3008** | ch0 | ch1 | ch2 | ch3
| **V-Devider** | |||| R4-^-R3 | R3-^-R2 | R2-^-R1 | R1-^-VDD
|  | |||| 0.25 | 0.5 | 0.75 | 1

# LICENSE

See the [LICENSE](..\..\LICENSE.md) file for license rights and limitations.
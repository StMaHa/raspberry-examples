# Examples for Pulse-Width-Modulation (PWM) and servo motors

To control servo motors without jitter a real time clock is required.
The Python module gpiozero supports the use of pin factories, allowing the fast daemon pigpiod to be used.
The pigpio library is not supported on Raspberry Pi 5 and has been removed within Raspberry Pi OS Debian Trixie.

To install it:
- sudo apt update
- sudo apt install python3-pigpio pigpio
- sudo systemctl start pigpiod

The Python module sysfs_pwm.py uses sysfs to control rp1 chip, allowing the Raspberry Pi 5 to use servo motors without jitter.

See the [Hardware PWM via sysfs](../README.md)

# LICENSE

See the [LICENSE](../../LICENSE.md) file for license rights and limitations.
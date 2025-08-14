# Examples for Pulse-Width-Modulation (PWM) and servo motors

Add the following line to /boot/firmware/config.txt:
```
dtoverlay=pwm-2chan
```
... and reboot to enable PWM.

To control servo motors without jitter a real time clock is required.
The Python module gpiozero supports the use of pin factories, allowing the fast daemon pigpiod to be used.
The pigpio library is currently not supported on Raspberry Pi 5.

The Python module syspwm.py uses sysfs to control pwmchip0, allowing the Raspberry Pi 5 to use servo motors without jitter.

# LICENSE

See the [LICENSE](LICENSE.md) file for license rights and limitations.
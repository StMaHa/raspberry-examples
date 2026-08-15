# Examples for Pulse-Width-Modulation (PWM) and servo motors

To control servo motors without jitter a real time clock is required.
The Python module gpiozero supports the use of pin factories, allowing the fast daemon pigpiod to be used.
The pigpio library is not supported on Raspberry Pi 5 and has been removed within Raspberry Pi OS Debian Trixie.

## Hardware PWM via sysfs

### Option 1: All Raspberry Pi's

**Enable PWM channels:**
- Add `dtoverlay=pwm-2chan` to the file `/boot/firmware/config.txt`
- Reboot Raspberry Pi

**Check PWM channels:**
```bash
ls -la /sys/class/pwm
```
Output:  
&nbsp;&nbsp;pwmchip**0** -> ../../devices/platform/soc/2020c000.pwm/pwm/pwmchip**0**  
or Raspberry Pi 5  
&nbsp;&nbsp;pwmchip**0** -> ../../devices/platform/axi/1000120000.pcie/1f00098000.pwm/pwm/pwmchip**0**  
&nbsp;&nbsp;pwmchip1 -> ../../devices/platform/axi/1000120000.pcie/1f0009c000.pwm/pwm/pwmchip1 &nbsp;&nbsp;&nbsp; (only Pi 5, e.g. fan)

**2 PWM channels (all Pi's except Pi 5):**
- PWM Chip 0 Channel 0 – GPIO 18 and GPIO 12
- PWM Chip 0 Channel 1 – GPIO 19 and GPIO 13

**4 PWM channels (Pi 5 only):**
- PWM Chip 0 Channel 0 – GPIO 12
- PWM Chip 0 Channel 1 – GPIO 13
- PWM Chip 0 Channel 2 – GPIO 18
- PWM Chip 0 Channel 3 – GPIO 19

**Check IO status:**
```bash
pinctrl get 12,13,18,19
```

**Configure IO's for PWM (all Pi's except Pi 5):**
```bash
sudo pinctrl set 12 a0
sudo pinctrl set 13 a0
sudo pinctrl set 18 a5
sudo pinctrl set 19 a5
```

**Configure IO's for PWM (Pi 5 only):**
```bash
sudo pinctrl set 12 a0
sudo pinctrl set 13 a0
sudo pinctrl set 18 a3
sudo pinctrl set 19 a3
```

**File system:** `/sys/class/pwm/pwmchip0`

**Export PWM channel 0:**
```bash
echo 0 > /sys/class/pwm/pwmchip0/export
```

**Set PWM frequency to 50Hz (Period 20ms = 20000000ns):**
```bash
echo 20000000 > /sys/class/pwm/pwmchip0/pwm0/period
```

**Set Duty Cycle to 10% (2ms = 2000000ns):**
```bash
echo 2000000 > /sys/class/pwm/pwmchip0/pwm0/duty_cycle
```

**Enable PWM:**
```bash
echo 1 > /sys/class/pwm/pwmchip0/pwm0/enable
```

**Disable PWM:**
```bash
echo 0 > /sys/class/pwm/pwmchip0/pwm0/enable
```

**Remove PWM channel 0:**
```bash
echo 0 > /sys/class/pwm/pwmchip0/unexport
```


### Option 2: Only Raspberry Pi 5

- PWM channel 0 – GPIO 02 to GPIO 27 (all GPIO's)
- Max. 4 PWM IO's
- Each PWM IO is mapped to pwmchip(n) &nbsp;&nbsp;&nbsp;&nbsp; (pwmchip1 ... pwmchip4)

**Activation example (GPIO 3, 18, 23, and 4):**  
- Add the following lines to the file `/boot/firmware/config.txt`
```
dtoverlay=pwm-pio,gpio=3
dtoverlay=pwm-pio,gpio=18
dtoverlay=pwm-pio,gpio=23
dtoverlay=pwm-pio,gpio=4
```
- Reboot Raspberry Pi

**Check available PWM chips:**
```bash
ls -la /sys/class/pwm
```
Output:  
pwmchip0 -> ../../devices/platform/axi/1000120000.pcie/1f0009c000.pwm/pwm/pwmchip0 &nbsp;&nbsp;&nbsp; (Pi5, e.g. fan)  
pwmchip1 -> ../../devices/platform/pwm_pio@**4**/pwm/pwmchip1 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (@**4**  -> **GPIO 4**)  
pwmchip2 -> ../../devices/platform/pwm_pio@**17**/pwm/pwmchip2 &nbsp;&nbsp;&nbsp;&nbsp; (@**17** -> **GPIO 23**)  
pwmchip3 -> ../../devices/platform/pwm_pio@**12**/pwm/pwmchip3 &nbsp;&nbsp;&nbsp;&nbsp; (@**12** -> **GPIO 18**)  
pwmchip4 -> ../../devices/platform/pwm_pio@**3**/pwm/pwmchip4 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (@**3**  -> **GPIO 3**)  

**Using sysfs to control PWM** (e.g. **GPIO 4** -> pwmchip**1**)**:**

**File system:** `/sys/class/pwm/pwmchip1`

**Export PWM channel 0 of pwmchip1 (GPIO 4):**
```bash
echo 0 > /sys/class/pwm/pwmchip1/export
```

**Set PWM frequency to 50Hz (Period 20ms = 20000000ns):**
```bash
echo 20000000 > /sys/class/pwm/pwmchip1/pwm0/period
```

**Set Duty Cycle to 10% (2ms = 2000000ns):**
```bash
echo 2000000 > /sys/class/pwm/pwmchip1/pwm0/duty_cycle
```

**Enable PWM:**
```bash
echo 1 > /sys/class/pwm/pwmchip1/pwm0/enable
```

**Disable PWM:**
```bash
echo 0 > /sys/class/pwm/pwmchip1/pwm0/enable
```

**Remove PWM channel 0 of pwmchip1 (GPIO 4):**
```bash
echo 0 > /sys/class/pwm/pwmchip1/unexport
```

# LICENSE
See the [LICENSE](../LICENSE.md) file for license rights and limitations.

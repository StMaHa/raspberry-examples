# Examples for Pulse-Width-Modulation (PWM) and servo motors

To control servo motors without jitter a real time clock is required.
The Python module gpiozero supports the use of pin factories, allowing the fast daemon pigpiod to be used.
The pigpio library is not supported on Raspberry Pi 5 and has been removed within Raspberry Pi OS Debian Trixie.

The Python module pwm_sysfs.py uses sysfs to control rp1 chip, allowing the Raspberry Pi 5 to use servo motors without jitter.

## Hardware PWM via sysfs

### Option 1: All Raspberry Pi's

**Enable PWM Channels:**
- Add `dtoverlay=pwm-2chan` to the file `/boot/firmware/config.txt`
- Reboot Raspberry Pi

**Check PWM channels:**
```bash
ls /sys/class/pwm/pwmchip0
ls /sys/class/pwm/pwmchip1  # Pi5, e.g. for fan
```

**2 PWM Channels (all Pi's except Pi 5):**
- PWM Chip 0 Channel 0 – GPIO 18 and GPIO 12
- PWM Chip 0 Channel 1 – GPIO 19 and GPIO 13

**4 PWM Channels (Pi 5 only):**
- PWM Chip 0 Channel 0 – GPIO 12
- PWM Chip 0 Channel 1 – GPIO 13
- PWM Chip 0 Channel 2 – GPIO 18
- PWM Chip 0 Channel 3 – GPIO 19

**Check IO Status:**
```bash
pinctrl get 12,13,18,19
```

**Configure IO's for PWM:**
```bash
sudo pinctrl set 12 a0
sudo pinctrl set 13 a0
sudo pinctrl set 18 a3
sudo pinctrl set 19 a3
```


**File System:** `/sys/class/pwm/pwmchip0`

**Export PWM Channel 0:**
```bash
echo 0 > /sys/class/pwm/pwmchip0/export
```

**Set PWM Frequency to 50Hz (Period 20ms = 20000000ns):**
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

**Remove PWM Channel 0:**
```bash
echo 0 > /sys/class/pwm/pwmchip0/unexport
```

### Option 2: Only Raspberry Pi 5

**Configuration:**
- PWM channel 0 – GPIO 02 to GPIO 27 (all GPIO's)
- Max. 4 PWM IO's
- each PWM IO is mapped to pwmchip<n> (pwmchip1 ... pwmchip4)

**Activation Example (GPIO 3, 18, 23, and 4):**
Add the following lines to the file `/boot/firmware/config.txt`
```
dtoverlay=pwm-pio,gpio=3
dtoverlay=pwm-pio,gpio=18
dtoverlay=pwm-pio,gpio=23
dtoverlay=pwm-pio,gpio=4
```

Reboot Raspberry Pi

**Check available PWM chips:**
```bash
ls -la /sys/class/pwm
# Output:
# pwmchip0 -> ../../devices/platform/axi/1000120000.pcie/1f0009c000.pwm/pwm/pwmchip0  (Pi5, z.B. Lüfter)
# pwmchip1 -> ../../devices/platform/pwm_pio@4/pwm/pwmchip1    (@4  -> GPIO 4)
# pwmchip2 -> ../../devices/platform/pwm_pio@17/pwm/pwmchip2   (@17 -> GPIO 23)
# pwmchip3 -> ../../devices/platform/pwm_pio@12/pwm/pwmchip3   (@12 -> GPIO 18)
# pwmchip4 -> ../../devices/platform/pwm_pio@3/pwm/pwmchip4    (@3  -> GPIO 3)
```

**Using sysfs to control PWM (e.g. GPIO 4):**

**File System:** `/sys/class/pwm/pwmchip1`

**Export PWM Channel 0 of pwmchip1 (GPIO 4):**
```bash
echo 0 > /sys/class/pwm/pwmchip1/export
```

**Set PWM Frequency to 50Hz (Period 20ms = 20000000ns):**
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

**Remove PWM Channel 0 of pwmchip1 (GPIO 4):**
```bash
echo 0 > /sys/class/pwm/pwmchip1/unexport
```

# LICENSE

See the [LICENSE](LICENSE.md) file for license rights and limitations.
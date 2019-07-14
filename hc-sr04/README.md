# Example for distance sensors like HC-SR04

# Python
## distance-sensor.py
Example uses python library *gpiozero*.\
Python script uses daemon of *pigpio*, therefore start daemon *pigpiod*:\
(Enable daemon *pigpiod* to start automatically at system start.)
```
$ sudo systemctl start pigpiod
$ sudo systemctl enable pigpiod
$ python3 distance-sensor.py
```

# C
## How to build
```
gcc ...
```

# LICENSE
See the [LICENSE](../LICENSE.md) file for license rights and limitations.

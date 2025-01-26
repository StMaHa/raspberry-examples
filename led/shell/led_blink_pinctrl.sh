#!/bin/bash

# WARNING! pinctrl set writes directly to the GPIO control registers
# ignoring whatever else may be using them (such as Linux drivers) -
# it is designed as a debug tool, only use it if you know what you
# are doing and at your own risk!


# Define GPIO pin where LED is connected

GPIO_LED=21

echo "Start Blinking..."

# Set GPIO pin as output
pinctrl set $GPIO_LED op

i=1
while [ $i -le 10 ]
do
    sleep 1
    echo "Blink $i"
    # Drive GPIO pin to high
    pinctrl set $GPIO_LED dh
    sleep 1
    # Drive GPIO pin to low
    pinctrl set $GPIO_LED dl
    let i++
done
echo "Blinking done!"

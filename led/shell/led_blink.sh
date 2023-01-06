#!/bin/bash

# Define GPIO pin where LED is connected
GPIO_LED=21

echo "Start Blinking..."

# Enable GPIO pin
echo $GPIO_LED > /sys/class/gpio/export
# Set GPIO pin as output
echo "out" > /sys/class/gpio/gpio$GPIO_LED/direction 

i=1
while [ $i -le 10 ]
do
    sleep 1
    echo "Blink $i"
    # Set GPIO pin to high
    echo "1" > /sys/class/gpio/gpio$GPIO_LED/value
    sleep 1
    # Set GPIO pin to low
    echo "0" > /sys/class/gpio/gpio$GPIO_LED/value
    let i++
done
# Free resource
echo $GPIO_LED > /sys/class/gpio/unexport
echo "Blinking done!"

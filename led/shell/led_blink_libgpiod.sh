#!/bin/bash

# Define GPIO pin where LED is connected

GPIO_LED=21

echo "Start Blinking..."

i=1
while [ $i -le 10 ]
do
    sleep 1
    echo "Blink $i"
    # Drive GPIO pin to high
    gpioset gpiochip0 $GPIO_LED=1
    sleep 1
    # Drive GPIO pin to low
    gpioset gpiochip0 $GPIO_LED=0
    let i++
done
echo "Blinking done!"

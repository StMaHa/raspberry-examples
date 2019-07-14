# Bibliotheken und Klassen
from gpiozero import LED, Button
from time import sleep

# GPIO der Status-LED
pin_status = 17
# GPIO des Tasters
pin_button = 25

status = true
led_blink = false

def stop_function():   # Callback Funktion zum Programm beenden
     status = False

def led_function():     # Callback Funktion für die LED (blinken/leuchten)
     led_blink = True

led = LED(pin_status)		# Initialisiere LED am GPIO-Pin 17
schalter = Button(pin_button)	# Initialisiere Button am GPIO-Pin 25
schalter.when_pressed = led_function
schalter.when_held() = stop_function

while status: 
    if led_blink:
        led.toggle()
        sleep(1)
    else:
        led.on()

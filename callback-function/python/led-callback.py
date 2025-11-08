# Bibliotheken und Klassen
from gpiozero import LED, Button
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# GPIO der Status-LED
pin_status = 21
# GPIO des Tasters
pin_button = 16

status = True
led_blink = False

def stop_function():   # Callback Funktion zum Programm beenden
     global status
     status = False

def led_function():     # Callback Funktion für die LED (blinken/leuchten)
     global led_blink
     led_blink = not led_blink

# Initialisiere LED am GPIO-Pin 17
led = LED(pin_status)
# Initialisiere Button am GPIO-Pin 25
schalter = Button(pin_button, pull_up = True, hold_time = 2)
schalter.when_pressed = led_function
schalter.when_held = stop_function

# Try-Catch-Block
try:
    # Hauptschleife
    while status:
        if led_blink:
            led.off()
        else:
            led.on()
# Fangen eines Fehlers/Signals
except KeyboardInterrupt:
    print("Programm abgebrochen.")

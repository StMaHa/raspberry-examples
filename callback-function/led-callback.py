# Bibliotheken und Klassen
from gpiozero import LED, Button
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# GPIO der Status-LED
pin_status = 17
# GPIO des Tasters
pin_button = 25

status = True
led_blink = False

def stop_function():   # Callback Funktion zum Programm beenden
     status = False

def led_function():     # Callback Funktion für die LED (blinken/leuchten)
     led_blink = True

my_factory = PiGPIOFactory()

led = LED(pin_status, pin_factory = my_factory)		# Initialisiere LED am GPIO-Pin 17
schalter = Button(pin_button, hold_time = 2, pin_factory = my_factory)	# Initialisiere Button am GPIO-Pin 25
schalter.when_pressed = led_function
schalter.when_held() = stop_function

while status:
    if led_blink:
        led.toggle()
        sleep(1)
    else:
        led.on()

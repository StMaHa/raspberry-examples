from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# GPIOs des Abstandssensors
pin_trigger = 24
pin_echo = 23
# Erstellen  einer Sensorinstanz
factory = PiGPIOFactory()
sensor = DistanceSensor(echo = pin_echo, trigger = pin_trigger, pin_factory = factory ) 

# Try-Catch-Block
try:
    # Hauptschleife
    while True:
        print(sensor.distance * 100)
        sleep(1)
# Fangen eines Fehlers/Signals
except KeyboardInterrupt:
    print("Programm abgebrochen.")

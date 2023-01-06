from gpiozero import LED
from time import sleep

GPIO_LED = 21

led = LED(GPIO_LED)

print("Start blinking...")
print("Press CTRL-C to stop.")

try:
    while(True):
        led.on()
        sleep(0.5)
        led.off()
        sleep(0.5)
except KeyboardInterrupt:
    pass

print("Done!")


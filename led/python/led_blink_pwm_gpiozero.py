# Beispiel mit gpiozero library
from gpiozero import PWMLED
from time import sleep


GPIO_LED = 21

led = PWMLED(GPIO_LED)

print("Start blinking...")
print("Press CTRL-C to stop.")

try:
    while True:
        led.value = 0  # off
        sleep(0.5)
        led.value = 0.25  # 25% brightness
        sleep(0.5)
        led.value = 0.5  # 50% brightness
        sleep(0.5)
        led.value = 1  # 100% brightness
        sleep(0.5)
except:
    print("Done!")

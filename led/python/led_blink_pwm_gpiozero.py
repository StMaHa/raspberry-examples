from gpiozero import PWMLED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

GPIO_LED = 21

factory = PiGPIOFactory()
led = PWMLED(GPIO_LED, pin_factory = factory)

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

from gpiozero import Buzzer
import time

buz = Buzzer(21)

buz.on()
time.sleep(3)
buz.off()

from gpiozero import MotionSensor
import time

PIN_PIR = 23

pir = MotionSensor(PIN_PIR)

def callback_function(channel):
    print("Motion detected.")

try:
    pir.when_motion = callback_function
    while(True):
        time.sleep(10)
except KeyboardInterrupt:
    print("END")

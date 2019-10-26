import RPi.GPIO as GPIO

PIN_PIR = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_PIR, GPIO.IN)

try:
    while(True):
        if(GPIO.input(PIN_PIR)):
            print("Motion detected.")
        else:
            print("No motion.")
except KeyboardInterrupt:
    print("END")

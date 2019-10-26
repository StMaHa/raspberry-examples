from gpiozero import MotionSensor

PIN_PIR = 23

pir = MotionSensor(PIN_PIR)

try:
    while(True):
        if(pir.motion_detected):
            print("Motion detected.")
        else:
            print("No motion.")
except KeyboardInterrupt:
    print("END")

#!/usr/bin/env python3
# Show preview from camera for 10 seconds and capture picture by using picamera library.
from picamera import PiCamera
from time import sleep

picam = PiCamera()
picam.start_preview(fullscreen=False, window=(50,50,640,480))
sleep(10)
picam.capture("/home/pi/capture.jpg")
picam.stop_preview()

print("Done!")

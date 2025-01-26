#!/usr/bin/env python3
# Show preview from camera for 10 seconds and capture picture by using picamera library.
print("This is not supported on latest Raspberry Pi OS anymore.")
print("I tmight work on Raspberry Pi Legacy OS.")
print("Use picamera2 instead.")

from picamera import PiCamera
from time import sleep

picam = PiCamera()
picam.start_preview(fullscreen=False, window=(50,50,640,480))
sleep(10)
picam.capture("/home/pi/capture.jpg")
picam.stop_preview()

print("Done!")

#!/usr/bin/env python3
# Show preview from camera for 10 seconds and capture picture by using picamera2 library
from picamera2 import Picamera2, Preview
from time import sleep

# Create instance of Picamera2
picam = Picamera2()
# Configure camera
cam_config = picam.create_preview_configuration()
picam.configure(cam_config)
# Initilize preview
picam.start_preview(Preview.QTGL)
# Start preview
picam.start()
# Show preview for 10 seconds
sleep(10)
# Capture preview and store it
picam.capture_file("/home/pi/capture.jpg")
# Stop preview
picam.stop()
# End of preview
picam.stop_preview()

print("Done!")

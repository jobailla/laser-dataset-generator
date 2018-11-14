from time import sleep
from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = (800, 600)
camera.start_preview()
hz = 30

while 42:
    file_name = "dataset:" + time.strftime("%Y-%m-%d") + "_hz:" + str(hz) + ".jpg" 
    input("Press <RETURN> to capture " + str(hz))
    camera.capture("./dataset/" + file_name)
    print ("Capture " + str(hz) + "hz")
    hz = hz + 1

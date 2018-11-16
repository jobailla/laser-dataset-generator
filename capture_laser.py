import pyaudio
import numpy as np
import sys
from time import sleep
from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = (800, 600)
camera.start_preview()
hz = 100

p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 2.0   # in seconds, may be float

while hz < 350:
	samples = (np.sin(2 * np.pi * np.arange(fs * duration) * hz / fs)).astype(np.float32)
    	stream = p.open(format=pyaudio.paFloat32, channels= 1, rate=fs, output=True)
    	file_name = "dataset:" + time.strftime("%Y-%m-%d") + "_hz:" + str(hz) + ".jpg" 
#   input("Press <RETURN> to capture " + str(hz))
    	stream.write(volume * samples)
    	camera.capture("./dataset/" + file_name)
	sys.stdout.write("Capture " + str(hz) + " hz\n")
    	sys.stdout.flush()
        stream.stop_stream()
   	stream.close()
    	hz = hz + 1
p.terminate() 




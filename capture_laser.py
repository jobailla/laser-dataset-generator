import pyaudio
import numpy as np
import sys
import time
import threading
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (800, 600)
camera.start_preview()
hz = 100

p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 44100
duration = 2.5  
stream = p.open(format=pyaudio.paFloat32, channels= 1, rate=fs, output=True)
samples = 0
file_name = 0

class freq_thread(threading.Thread):
    def run(self):
    	stream.write(volume * samples)

class capture_thread(threading.Thread):
    def run(self):
  	camera.capture("./dataset/" + file_name)

while hz < 350:
	samples = (np.sin(2 * np.pi * np.arange(fs * duration) * hz / fs)).astype(np.float32)
    	file_name = "dataset:" + time.strftime("%Y-%m-%d") + "_hz:" + str(hz) + ".jpg"
        play_freq = freq_thread()
        cap_laser = capture_thread()
        play_freq.start()
        time.sleep(0.4)
        cap_laser.start()
        cap_laser.join()
        play_freq.join()
	sys.stdout.write("Capture " + str(hz) + " hz\n")
    	sys.stdout.flush()
    	hz = hz + 1
stream.stop_stream()
stream.close()
p.terminate() 

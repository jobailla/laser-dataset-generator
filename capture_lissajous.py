import pyaudio
import numpy as np
import sys
import time
import threading
from picamera import PiCamera
from fractions import Fraction

camera = PiCamera()
camera.resolution = (800, 600)
camera.framerate = 60
camera.start_preview()


f1 = 120.0
f2 = 0.0        # f2 = n+1/n * f1
a = 2.0

volume = 0.2    # range [0.0, 1.0]
fs = 44100
duration = 10.0
samples_1 = 0.0
samples_2 = 0.0
file_name = 0

p = pyaudio.PyAudio()
stream_1 = p.open(format=pyaudio.paFloat32, channels = 1, rate=fs, output = True)
stream_2 = p.open(format=pyaudio.paFloat32, channels = 1, rate=fs, output = True)

class freq_1_thread(threading.Thread):
    def run(self):
    	stream_1.write(volume * samples_1)

class freq_2_thread(threading.Thread):
    def run(self):
    	stream_2.write(volume * samples_2)

class capture_thread(threading.Thread):
    def run(self):
  	camera.capture("./dataset_lissajous/" + file_name)

def start_threads():
    play_freq_1 = freq_1_thread()
    play_freq_2 = freq_2_thread()
    cap_laser = capture_thread()
    play_freq_1.start()
    play_freq_2.start()
    time.sleep(0.5)
    cap_laser.start()
    cap_laser.join()
    play_freq_1.join()
    play_freq_2.join()
    
def stop_stream():
    stream_1.stop_stream()
    stream_2.stop_stream()
    stream_1.close()
    stream_2.close()
    stream.stop_stream()
    stream.close()
    p.terminate()

while f1 <= 300.0:
	f2 = (a + 1.0) / a * f1
	camera.shutter_speed = int(1000000 / f2 - f1)
        samples_1 = (np.sin(2 * np.pi * np.arange(fs * duration) * f1 / fs)).astype(np.float32)
        samples_2 = (np.sin(2 * np.pi * np.arange(fs * duration) * f2 / fs)).astype(np.float32)
        file_name = "dataset:" + time.strftime("%d-%m-%Y") + "_hz:" + str(round(f1, 1)) + "_" + str(round(f2,3)) + "_lsj:" + str(int(a + 1)) + "." + str(int(a)) + ".jpg"
        start_threads()
        sys.stdout.write("Capture " + str(f1) + " + " + str(f2) + " hz - lissajous : " + str(int(a + 1)) + "/" + str(int(a)) + "\n")
    	sys.stdout.flush()
        a += 1
	if a == 10.0:
	    f1 += 10.0
	    a = 1
stop_stream()

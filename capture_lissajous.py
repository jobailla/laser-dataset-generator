import pyaudio
import numpy as np
import sys
import time
import threading
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (800, 600)
camera.start_preview()

f1 = 30
f2 = 31


volume = 0.5     # range [0.0, 1.0]
fs = 44100
duration = 3.5
samples = 0
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

i = 0
while i < 10:
    samples_1 = (np.sin(2 * np.pi * np.arange(fs * duration) * f1 / fs)).astype(np.float32)
    samples_2 = (np.sin(2 * np.pi * np.arange(fs * duration) * f2 / fs)).astype(np.float32)
    file_name = "dataset:" + time.strftime("%Y-%m-%d") + "_hz:" + str(f1) + "_" + str(f2) + ".jpg"
    play_freq_1 = freq_1_thread()
    play_freq_2 = freq_2_thread()
    cap_laser = capture_thread()
    play_freq_1.start()
    play_freq_2.start()
    time.sleep(0.4)
    cap_laser.start()
    cap_laser.join()
    play_freq_1.join()
    play_freq_2.join()
    sys.stdout.write("Capture " + str(f1) + " + " + str(f2) + " hz\n")
    sys.stdout.flush()
    stream_1.stop_stream()
    stream_2.stop_stream()
    stream_1.close()
    stream_2.close()
    i = i - i
p.terminate()

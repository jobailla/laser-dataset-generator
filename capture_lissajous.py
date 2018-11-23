import pyaudio
import numpy as np
import sys
import time
import threading
from picamera import PiCamera
from fractions import Fraction

###################### CAPTURE INFO #####################
ampli_info = "Little Devil"
ampli_volume = "3"
laser_info = "Green class 2"
camera_info = "Sony IMX219 V2.1 8 MPX 1080p30 - 720p60"
mambrane_info = "10 day"
#########################################################

camera = PiCamera()
camera.resolution = (1280, 720)
camera.start_preview()


f1 = 60.0
f2 = 0.0        # f2 = n+1/n * f1
a = 2.0

volume = 0.1    # range [0.0, 1.0]
fs = 44100
duration = 3
samples_1 = 0.0
samples_2 = 0.0
file_name = 0

date = time.strftime("%d-%m-%Y") 

csv =  open("./dataset_lissajous/" + date + ".info.csv", "w")
csv =  open("./dataset_lissajous/" + date + ".info.csv", "a")
csv.write("ampli : " + ampli_info + ",\nampli_volume : " + ampli_volume + ",\ncode_volume : " + str(volume) + ",\nlaser : " + laser_info + ",\ncamera : " + camera_info + ",\nmambrane_old : " + mambrane_info)
csv.close()

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
        samples_1 = (np.sin(2 * np.pi * np.arange(fs * duration) * f1 / fs)).astype(np.float32)
        samples_2 = (np.sin(2 * np.pi * np.arange(fs * duration) * f2 / fs)).astype(np.float32)
        file_name = "dataset:" + date + "_hz:" + str(round(f1, 1)) + "_" + str(round(f2,3)) + "_lsj:" + str(int(a + 1)) + "." + str(int(a)) + ".jpg"
        start_threads()
        sys.stdout.write("Capture " + str(f1) + " + " + str(f2) + " hz - lissajous : " + str(int(a + 1)) + "/" + str(int(a)) + "\n")
    	sys.stdout.flush()
        a += 1
	if a == 10.0:
	    f1 += 1.0
	    a = 1
stop_stream()

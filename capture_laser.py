import os
import sys
import time
import pyaudio
import threading
import numpy as np
from datetime import datetime
from picamera import PiCamera

mambrane_fix_date = "13-11-2018"
date = time.strftime("%d-%m-%Y")
mambrane_age = datetime.strptime(date, "%d-%m-%Y") - datetime.strptime(mambrane_fix_date, "%d-%m-%Y")

###################### CAPTURE INFO #####################
ampli_info = "Little Devil"
ampli_volume = "3"
laser_info = "Green class 2"
camera_info = "Sony IMX219 V2.1 8 MPX 1080p30 - 720p60"
mambrane_info = str(mambrane_age.days) + " days"
#########################################################

camera = PiCamera()
camera.resolution = (1280, 720)
camera.start_preview()

hz = 30

p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 44100
duration = 2.5
stream = p.open(format = pyaudio.paFloat32, channels = 1, rate = fs, output = True)
samples = 0
file_name = 0

path = "./dataset/"
if not  os.path.exists(path):
    os.mkdir(path)
csv =  open(path + date + ".info.csv", "w")
csv.write("ampli : " + ampli_info + ",\nampli_volume : " + ampli_volume + ",\ncode_volume : " + str(volume) + ",\nlaser : " + laser_info + ",\ncamera : " + camera_info + ",\nmambrane_old : " + mambrane_info + ",\n")
csv.close()

class freq_thread(threading.Thread):
    def run(self):
        stream.write(volume * samples)

class capture_thread(threading.Thread):
    def run(self):
        camera.capture(path + file_name)

def start_threads():
    play_freq = freq_thread()
    cap_laser = capture_thread()
    play_freq.start()
    time.sleep(0.4)
    cap_laser.start()
    cap_laser.join()
    play_freq.join()

def stop_stream():
    stream.stop_stream()
    stream.close()

if (len(sys.argv) > 1):
    while hz <= float(sys.argv[1]):
        samples = (np.sin(2 * np.pi * np.arange(fs * duration) * hz / fs)).astype(np.float32)
        file_name = "dataset:" + time.strftime("%Y-%m-%d") + "_hz:" + str(hz) + ".jpg"
        start_threads()
        sys.stdout.write("\033[1;32;40m" + str(hz) + " hz\n\033[0;37;40m")
        sys.stdout.flush()
        hz = hz + 1
else:
    sys.stdout.write("\033[1;31;40musage: frequence_max\n\033[0;37;40m")
    sys.stdout.flush()
stop_stream()
p.terminate()

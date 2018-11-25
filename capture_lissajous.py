import os
import sys
import time
import pyaudio
import threading
from datetime import datetime
import numpy as np
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

nb_f = 2
f = [] * nb_f
if (len(sys.argv) > 1):
    f.insert(0, float(sys.argv[1]))
f.insert(1, 0.0)
a = 2.0

volume = 0.1    # range [0.0, 1.0]
fs = 44100
duration = 3.0
samples = [0.0] * nb_f
file_name = 0

path = "./dataset_lissajous/"
if not  os.path.exists(path):
    os.mkdir(path)
csv =  open(path + date + ".info.csv", "w")
csv.write("ampli : " + ampli_info + ",\nampli_volume : " + ampli_volume + ",\ncode_volume : " + str(volume) + ",\nlaser : " + laser_info + ",\ncamera : " + camera_info + ",\nmambrane_old : " + mambrane_info + ",\n")
csv.close()

p = pyaudio.PyAudio()
stream = [] * nb_f
for x in range(nb_f):
    stream.insert(x, p.open(format = pyaudio.paFloat32, channels = 1, rate = fs, output = True))

class freq_1_thread(threading.Thread):
    def run(self):
        stream[0].write(volume * samples[0])

class freq_2_thread(threading.Thread):
    def run(self):
        stream[1].write(volume * samples[1])

class capture_thread(threading.Thread):
    def run(self):
        camera.capture(path + file_name)

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
    for x in range(nb_f):
        stream[x].stop_stream()
        stream[x].close()
        stream.stop_stream()
        stream.close()

if (len(sys.argv) > 1):
    while f[0] <= float(sys.argv[2]):
        try:
            f[1] = (a + 1.0) / a * f[0]
            for x in range(nb_f):
                samples.insert(0, (np.sin(2 * np.pi * np.arange(fs * duration) * f[x] / fs)).astype(np.float32))
            file_name = "dataset:" + date + "_hz:" + str(round(f[0], 1)) + "_" + str(round(f[1],3)) + "_lsj:" + str(int(a + 1)) + "." + str(int(a)) + ".jpg"
            start_threads()
            sys.stdout.write("\033[1;32;40m" + str(f[0]) +  "\033[0;37;40m + " + "\033[1;34;40m" +  str(round(f[1], 3)) + "\t\033[0;37;40m hz\t" + "\033[1;33;40m" + str(int(a + 1)) + "/" + str(int(a)) + "\n\033[0;37;40m")
            sys.stdout.flush()
            a += 1
            if a == 10.0:
                sys.stdout.write("\n")
                sys.stdout.flush()
                a = 1
                f[0] += 1.0
        except KeyboardInterrupt:
            exit(0)
    stop_stream()
else:
    sys.stdout.write("\033[1;31;40musage: frequence_min frequence_max\n\033[0;37;40m")
    sys.stdout.flush()
p.terminate()

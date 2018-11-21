import pyaudio
import numpy as np
import sys

p = pyaudio.PyAudio()

volume = 0.3     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 30.0   # in seconds, may be float
f = float(sys.argv[1])

samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)
stream = p.open(format= pyaudio.paFloat32, channels = 1, rate = fs, output = True)
stream.write(volume * samples)
stream.stop_stream()
stream.close()
p.terminate()

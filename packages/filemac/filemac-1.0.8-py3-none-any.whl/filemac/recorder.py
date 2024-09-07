import os
import playsound
import time

import pyaudio
p
# Set up the audio stream
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1,
                    rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# time.sleep(10)
# stream.stop_stream()

aud = stream.write(8000, 2000)
data = stream.read(8000)

playsound.playsound(aud)

import math
import os
import crepe
import time
import numpy
from record_loopback import Recorder
import pyaudiowpatch as pyaudio
import queue
import struct
import _thread
import array

recorder = Recorder(pyaudio.paInt16)

sample_rate = recorder.get_sample_rate()
channels = recorder.get_channels()

process_per_sec = 10

num_sample_to_process = sample_rate // process_per_sec

q = queue.Queue()

buffer = bytearray()


def callback(in_data, frame_count, time_info, status):
    """Write frames and return PA flag"""
    global buffer
    buffer += in_data
    if len(buffer) // 2 // channels > num_sample_to_process:
        q.put(buffer)
        buffer = bytearray()
    # open("debug.log", "+w").write()
    return (in_data, pyaudio.paContinue)

def freq_to_note(freq):
    notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

    note_number = 12 * math.log2(freq / 440) + 49  
    note_number = round(note_number)
        
    note = (note_number - 1 ) % len(notes)
    note = notes[note]
    
    octave = (note_number + 8 ) // len(notes)
    
    return note, octave

def process():
    while True:
        data = q.get()
        N = len(data)
        fmt = "<" + ("h" * (N // 2))
        data_s = array.array("h", struct.unpack(fmt, data))
        N = len(data_s)
        # print(N)
        assert N % channels == 0
        data_s = numpy.reshape(data_s, (N // channels, channels))
        (_, f, confidence, _) = crepe.predict(
            data_s, sample_rate, step_size=1000 // process_per_sec, center=False, verbose = 0
        )
        if confidence > 0.2:
            os.system('cls')
            print(freq_to_note(f))


recorder.start(callback)
_thread.start_new_thread(process, ())
time.sleep(100)
# crepe.predict()

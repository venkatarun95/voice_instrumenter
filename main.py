# import pyaudio
import array
import math
import numpy as np
import re
import scipy.fftpack
import sys
import wave


def read_music_file(filename):
    res = [(0.0, None)]
    in_file = open(filename, 'r')
    re_split = re.compile(r'\s+')
    for line in in_file.readlines():
        x, y = re_split.split(line)[:2]
        x = float(x)
        try:
            y = float(y)
        except ValueError:
            y = None
        res.append((x, y))

    if res[1][0] == 0.0:
        res = res[1:]
    return res

def note_number(freq):
    return 12 * math.log(freq / 440.0, 2) + 49
def note_freq(note):
    return (2**((note - 49) / 12)) * 440

def generate_music(music, out_filename):
    frame_rate = 32000

    time = 0.0 # in sec
    music_pos = 0
    phase = 0.0 # in radians
    sound = []

    while True:
        freq = music[music_pos][1]

        if freq != None:
            # n = note_number(freq)
            # if abs(freq - note_freq(n)) < abs(freq - note_freq(n+1)):
            #     freq = note_freq(n)
            # else:
            #     freq = note_freq(n+1)
            sound.append(math.sin(time * 2 * math.pi * freq + phase))
        else:
            sound.append(0)
        print time, freq

        time += 1.0 / frame_rate
        if music[music_pos][0] < time: # and (time > prev_time + 0.1 or freq == None):
            music_pos += 1
            if music_pos >= len(music):
                break
            if music[music_pos][1] != None and music[music_pos-1][1] != None:
                phase += 2 * math.pi * time * \
                    (music[music_pos - 1][1] - music[music_pos][1])
            # prev_time = time
            # while music_pos < len(music) and music[music_pos][0] < time:
            #     music_pos += 1


    # Filter out the high frequency noise
    # freq_cutoff = 1000.0 # Hz
    #
    # sound = np.array(sound)
    # spectrum = scipy.fftpack.rfft(sound)
    # temp_freqs = scipy.fftpack.rfftfreq(len(sound), 1.0 / frame_rate)
    #
    # tmp = spectrum[0]
    # spectrum[0] = 0
    # cutoff_mag = spectrum.max() / 10
    # spectrum[0] = tmp
    #
    # print spectrum.max()
    # for i in range(len(sound)):
    #     # print spectrum[i]
    #     if temp_freqs[i] > freq_cutoff: # or abs(spectrum[i]) < cutoff_mag:
    #         spectrum[i] = 0
    # sound = scipy.fftpack.irfft(spectrum)

    sample_width = 1

    # Write to array
    wf = wave.open(out_filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(frame_rate)

    data = array.array('B')
    assert(data.itemsize == sample_width)

    print len(sound)
    for x in sound:
        x = min(1.0, max(-1.0, x))
        # print x, ((2**16 - 1) * (x + 1.0))
        # data.append(int((2**16 - 1) * (x + 1.0)))
        # data.append(x)
        data.append(int(127*(x + 1.0)))

    wf.setnframes(time * frame_rate)
    wf.writeframes(data)
    wf.close()

if __name__ == "__main__":
    assert(len(sys.argv) == 3)
    music = read_music_file(sys.argv[1])
    generate_music(music, sys.argv[2])

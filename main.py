# import pyaudio
import array
import math
import os
import re
import sys
import wave

from instrument import Instrument

def read_music_file(filename):
    res = [(0.0, None, None)]
    in_file = open(filename, 'r')
    re_split = re.compile(r'\s+')
    max_intensity = 0.0
    for line in in_file.readlines():
        x, y, z = re_split.split(line)[:3]
        x = float(x)
        try:
            y = float(y)
            z = float(z)
            max_intensity = max(max_intensity, z)
        except ValueError:
            y = None
            z = None
        res.append((x, y, z))
    in_file.close()
    for i in range(len(res)):
        x = res[i]
        if res[i][1] != None:
            res[i] = (x[0], x[1], x[2] / max_intensity)
        else:
            res[i] = (x[0], None, None)

    if res[1][0] == 0.0:
        res = res[1:]
    return res

def note_number(freq):
    return 12 * math.log(freq / 440.0, 2) + 49
def note_freq(note):
    return (2**((note - 49) / 12)) * 440

def generate_music(music, out_filename):
    frame_rate = 32000
    num_harmonics = 4
    pitch_change_factor = 2

    time = 0.0 # in sec
    music_pos = 0
    phase = [0.0 for i in range(num_harmonics+1)] # in radians
    sound = []

    while True:
        freq = music[music_pos][1]
        intensity = music[music_pos][2]

        if freq != None:
            x = 0.0
            intensity = intensity ** 4
            for j in range(1, num_harmonics + 1):
                x += intensity*(0.2-0.03 *j)*(math.sin(time * 2 * math.pi * freq * \
                    (j+pitch_change_factor) + phase[j]))
            print time, intensity
            # x *= (1 + 0.01*math.sin((5 + 3*math.sin(time * 1)) * 2 * math.pi * time) \
            #     * math.sin(5 * 2 * math.pi * time))
            sound.append(x)
        else:
            sound.append(0)

        time += 1.0 / frame_rate
        if music[music_pos][0] < time:
            music_pos += 1
            if music_pos >= len(music):
                break
            if music[music_pos][1] != None and music[music_pos-1][1] != None:
                for j in range(1, num_harmonics + 1):
                    phase[j] += (j + pitch_change_factor) * 2 * math.pi * time * \
                        (music[music_pos - 1][1] - music[music_pos][1])

    sound = violin.apply_filter(sound, 1.0 / frame_rate)

    # Write to array
    sample_width = 1

    wf = wave.open(out_filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(frame_rate)

    data = array.array('B')
    assert(data.itemsize == sample_width)

    ewma = sound[0]
    for i in range(len(sound)):
        x = sound[i]
        # if i > 1.0 * frame_rate:
        #     sound[i] = 0.5*(x + sound[int(i - 1.0 / frame_rate)])
        #     x = sound[i]
        # alpha = 1.0 / (0.5 * frame_rate)
        # ewma = alpha * sound[i] + (1.0 - alpha) * ewma
        # x = ewma
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
    os.system("rm out.txt")
    os.system('touch out.txt')
    os.system("cp " + sys.argv[1] + " tmp.wav")
    os.system("praat listing.praat 60 \"yes\" 0 75 600")
    violin = Instrument('violin.dat')
    music = read_music_file('out.txt')
    generate_music(music, sys.argv[2])

import scipy.fftpack
import numpy as np

class Instrument:
    def __init__(self, data_filename):
        file = open(data_filename, 'r')
        self.filter = []
        max_y = 0
        for line in file.readlines():
            x, y = line.split(' ')
            y = 10.0 ** (float(y) / 20.0)
            self.filter.append((float(x), y))
            max_y = max(max_y, y)

        for i in range(len(self.filter)):
            self.filter[i] = (self.filter[i][0], self.filter[i][1] / max_y)

    def apply_filter(self, sound, time_unit):
        ''' Apply filter to add formant effect to the given sound trail

        sound -- 2D array of variables representing sound amplitude
        time_unit - number representing the number of units of time
            between two elements in the array'''

        sound = np.array(sound)
        spectrum = scipy.fftpack.rfft(sound)
        temp_freqs = scipy.fftpack.rfftfreq(len(sound), time_unit)

        prev, next, filter_pos = (0.0, 0.0), self.filter[0], 0
        for i in range(len(sound)):
            freq = temp_freqs[i]
            if freq > 1500:
                spectrum[i] = 0.0

            # while next[0] < freq:
            #     filter_pos += 1
            #     prev, next = next, self.filter[filter_pos]
            #
            # scale = ((freq - prev[0]) * next[1] + (next[0] - freq) * prev[1]) \
            #     / (next[0] - prev[0])
            # spectrum[i] *= scale


        sound = scipy.fftpack.irfft(spectrum)
        return sound

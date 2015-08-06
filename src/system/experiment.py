#!/usr/bin/env python2

import numpy as np
import matplotlib.pyplot as plt


class Experiment(object):

    """This class holds data and methods for a single frequency of
        electrical impedance spectroscopy. It is initialized with
        arrays of time, corresponding voltage, current, angular frequency
        and an optional dictionary of meta data
        """

    def __init__(self, t, v, i, w, meta={}):
        self.t = np.array(t)
        self.v = np.array(v)
        self.i = np.array(i)
        self.w = w
        self.meta = meta

    def transform(self, signal):
        nfft = signal.size
        n = np.floor(0.5 * nfft)
        s_ft = np.fft.fft(signal)
        idx = np.argmax(np.abs(s_ft[1:n]))
        z = s_ft[idx + 1] / n
        return z

    def impedance(self):
        if not hasattr(self, 'Z'):
            z_v = self.transform(self.v)
            z_i = self.transform(self.i)
            self.Z = z_v / z_i
        return (self.w, self.Z)

    def __str__(self):
        return "%r" % self.impedance()

    def plot(self):
        fig, ax1 = plt.subplots()
        ax1.set_xlabel('time [s]')
        ax1.set_ylabel('Voltage')
        ax2 = ax1.twinx()
        ax2.set_ylabel('Current')
        voltage, = ax1.plot(self.t, self.v, 'r-')
        current, = ax2.plot(self.t, self.i, 'b-')
        plt.legend([voltage, current], ["Voltage", "Current"])
        plt.show()

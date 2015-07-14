#!/usr/bin/env python2

from regionOfInterest import RegionOfInterest
import numpy as np

class ROI_Amplitude(RegionOfInterest):
    """A region of interest is defined by the following rule:
    If the imaginary part of the region is stationary (close to zero) there is nothing of interest in this region and the region can be ommitted.
    """
    def __init__(self):
        pass

    def Process(self, frequency, impedance):
        """This function returns all indices for the regions that are of interest."""
        indices = self.AmplitudeCriteria(frequency, impedance)
        return indices

    def AmplitudeCriteria(self, frequency, impedance):
        """This is equal to 2 decades in frequencydomain when considering a parallel RC-circuit
        The estimated error is around 2.02 %
        """
        operator = np.imag
        maxAmplitude = np.max(np.abs(operator(impedance)))
        indices = np.abs(operator(impedance) ) > 0.010050 * 2 * maxAmplitude
        return indices


#!/usr/bin/env python2
from preprocess import PreProcess
import numpy as np

class RegionOfInterest(PreProcess):
    """This class checks if the impedance can be devided into several parts, so called region of interest.
    A region of interest is defined by the following rule:
    If the imaginary part of the region is stationary (close to zero) there is nothing of interest in this region and the region can be ommitted"""
    def __init__(self):
        pass

    def Process(self, frequency, impedance):
        """This function returns all indices for the regions that are of interest."""
        operator = np.imag
        maxAmplitude = np.max(np.abs(operator(impedance)))
        indices = np.abs(operator(impedance) ) > 0.010050 * 2 * maxAmplitude
        # this is equal to 2 decades in frequencydomain when considering a parallel RC-circuit
        # The estimated error is around 2.02 %

        return indices

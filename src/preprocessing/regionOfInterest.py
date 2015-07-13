#!/usr/bin/env python2
from preprocess import PreProcess
import numpy as np


class RegionOfInterest(PreProcess):

    """This class checks if the impedance can be devided into several parts, so called region of interest.
    The region of interest can be used to reduce the complexity of a fit, by ommitting frequencies that only have a very low impact on the overall impedance, e.g. beeing close to zero.
    """

    def __init__(self):
        pass

    def Process(self, frequency, impedance):
        """This function returns all indices for the regions that are of interest."""
        return []


def PlotRegion(omega, impedance, indices):
    from matplotlib.pyplot import figure, semilogx, show

    op_list = [np.real, np.imag]
    for op in op_list:
        figure()
        semilogx(omega, op(impedance))
        semilogx(omega[indices], op(impedance[indices]), 'rx')
    show()

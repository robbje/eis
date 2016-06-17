#!/usr/bin/env python2

import numpy as np

class ParameterSet(object):
    
    T_POWER = (lambda x: 10.0**float(x), lambda y: np.log10(y))
    T_NEGPOWER = (lambda x: 10.0**float(-x), lambda y: -1.0*np.log10(y))
    T_NANO = (lambda x: x*1e9, lambda y: y*1e-9)
    T_MICRO = (lambda x: x*1e6, lambda y: y*1e-6)
    T_MILLI = (lambda x: x*1e3, lambda y: y*1e-3)
    T_ONE = (lambda x: x, lambda y: y)

    def __init__(self, names, constraints, values):
        self._names = names
        self._constraints = constraints
        self._mask = [True] * len(values)
        self._transform = [self.T_ONE[0]] * len(values)
        self._untransform = [self.T_ONE[1]] * len(values)
        self.updateValues(values)

    @classmethod
    def fromTree(cls, tree, p):
        return cls(tree.pNames, tree.constraints, p)

    def updateValues(self, p):
        self._values = p
        self._tvalues = self.applyTransform(p)

    def updateTransformedValues(self, tp):
        self._tvalues = tp
        self._values = self.applyUntransform(tp)

    def updateUnmaskedTransformedValues(self, param):
        tp = []
        for i, v in enumerate(self._mask):
            if v:
                tp.append(param[0])
                param = param[1:]
            else:
                tp.append(self._tvalues[i])
        self.updateTransformedValues(tp)

    def updateUnmaskedValues(self, param):
        for i, v in enumerate(self._mask):
            if v:
                p.append(param[0])
                param = param[1:]
            else:
                p.append(self._values[i])
        self.updateValues(p)

    def getUnmaskedTransformedValues(self):
        res = []
        for i, v in enumerate(self._mask):
            if v: res.append(self._tvalues[i])
        return res

    def getUnmaskedValues(self):
        res = []
        for i, v in enumerate(self._mask):
            if v: res.append(self._values[i])
        return res

    def setParameterMapping(self, pName, functions):
        for i, v in enumerate(self._names):
            if v == pName:
                self._transform[i] = functions[0]
                self._untransform[i] = functions[1]

    def applyConstraints(self):
        for i, v in enumerate(self._constraints):
            if self._values[i] < v[0]: self._values[i] = v[0]
            if self._values[i] > v[1]: self._values[i] = v[1]
        self.updateValues(self._values)

    def applyTransform(self, p):
        return [self._transform[i](v) for i, v in enumerate(p)]

    def applyUntransform(self, p):
        return [self._untransform[i](v) for i, v in enumerate(p)]

    def setMask(self, mask):
        self._mask = mask

    def maskAll(self):
        self._mask = [False] * len(self._values)

    def unmaskAll(self):
        self.maskAll()
        self.invertMask()

    def maskParameter(self, pName):
        for i, v in enumerate(self._names):
            if v == pName:
                self._mask[i] = False

    def invertMask(self):
        self._mask = map(lambda x: not x, self._mask)
    
    def __str__(self):
        s = ''
        for i, v in enumerate(self._values):
            s += '{}{}\n'.format(self._names[i].ljust(30), v)
        return s

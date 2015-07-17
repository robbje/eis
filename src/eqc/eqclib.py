#!/usr/bin/env python2

import numpy as np
from copy import deepcopy

ZERO = 1e-15


def Warburg(w, p):
    tan = 0
    denom = np.power(1j * w * p[1], 0.5)
    if p[1] * w < 1e5:
        tan = np.tanh(denom)
    else:
        tan = 1.0
    return p[0] * tan / denom


def Warburgni(w, p):
    tan = 0
    denom = np.power(1j * w * p[1], p[2])
    if p[1] * w < 1e5:
        tan = np.tanh(denom)
    else:
        tan = 1.0
    return p[0] * tan / denom


def dWarburg_dp0(w, p):
    tan = 0
    denom = np.power(1j * w * p[1], 0.5)
    if p[1] * w < 1e5:
        tan = np.tanh(denom)
    else:
        tan = 1.0
    return 1 * tan / denom


def dWarburg_dp1(w, p):
    tan = 0
    denom = np.power(1j * w * p[1], 0.5)
    if p[1] * w < 1e5:
        tan = np.tanh(denom)
    else:
        tan = 1.0

    real = p[0] / \
        (2.0 * p[1] * np.power(np.cosh(np.power(1j * w * p[1], 0.5)), 2.0))
    imag = -1j * p[0] * w * tan / (2.0 * np.power(1j * w * p[1], 1.5))
    return real + imag

eqcLib = {
    'R': {
        'inuse': [],
        'def': {
            'eqc': lambda w, p: p[0],
            'pNames': ['R'],
            'constraints': [(ZERO, 1e7), ],
            'jac': [lambda w, p: 1],
        },
    },
    'C': {
        'inuse': [],
        'def': {
            'eqc': lambda w, p: 1.0 / (1j * w * p[0]),
            'pNames': ['C'],
            'constraints': [(ZERO, 1), ],
            'jac': [lambda w, p: -1.0 / (1j * w * np.power(p[0], 2.0))]
        },
    },
    'L': {
        'inuse': [],
        'def': {
            'eqc': lambda w, p: 1j * w * p[0],
            'pNames': ['L'],
            'constraints': [(ZERO, 1), ],
            'jac': [lambda w, p: 1j * w],
        },
    },
    'Zarc': {
        'inuse': [],
        'def': {
            'eqc': lambda w, p: p[0] / (1.0 + np.power(1j * p[1] * w, p[2])),
            'pNames': ['R', 'T', 'n'],
            'constraints': [(ZERO, 1e7), (ZERO, 1), (ZERO, 1)],
            'jac': [lambda w, p: 1.0 / (1.0 + np.power(1j * p[1] * w, p[2])),
                    lambda w, p: -1.0 * p[0] * p[2] * np.power(1j * w * p[1], p[2]) /
                    (1.0 * p[1] * np.power(1.0 + np.power(1j * w * p[1], p[2]), 2.0)),
                    lambda w, p: -1.0 * p[0] * np.power(1j * w * p[1], p[2]) * np.log(1j * w * p[1]) /
                    np.power(1.0 + np.power(1j * w * p[1], p[2]), 2.0)],
        },
    },
    'CPE': {
        'inuse': [],
        'def': {
            'eqc': lambda w, p: 1.0 / (p[0] * np.power(1j * w, p[1])),
            'pNames': ['Q', 'n'],
            'constraints': [(ZERO, 1), (ZERO, 1)],
            'jac': [lambda w, p: -1.0 * np.power(1j * w, -1.0 * p[1]) / np.power(p[0], 2.0),
                    lambda w, p: -1.0 * np.log(1j * w) / (p[0] * np.power(1j * w, p[1]))],
        },
    },
    'Warb': {
        'inuse': [],
        'def': {
            'eqc': Warburg,
            'pNames': ['R', 'T'],
            'constraints': [(ZERO, 1e7), (ZERO, 1)],
            'jac': [dWarburg_dp0,
                    dWarburg_dp1],
        },
    },
    'Warbni': {
        'inuse': [],
        'def': {
            'eqc': Warburgni,
            'pNames': ['R', 'T', 'n'],
            'constraints': [(ZERO, 1e7), (ZERO, 1e4), (0.5, 0.54)],
            'jac': [lambda w, p: Exception("Not implemented"),
                    lambda w, p: Exception("Not implemented"),
                    lambda w, p: Exception("Not implemented")],
        },
    },
    'DC': {
        'inuse': [],
        'def': {
            'eqc': lambda w, p: 1.0 / np.power(1.0 + 1j * w * p[0], 0.5),
            'pNames': ['T', 'n'],
            'constraints': [(ZERO, 1), (ZERO, 1)],
            'jac': [lambda w, p: Exception("Not implemented"),
                    lambda w, p: Exception("Not implemented")],
        },
    },
}


def resetClassDefinition():
    for k in eqcLib:
        eqcLib[k]['inuse'] = []


def getClassDefinition(name):
    el = name
    ln = "1"
    if '_' in name:
        el = name.split('_')[0]
        ln = name.split('_')[1]
    if el not in eqcLib:
        raise ValueError("Unknown element: %s" % el)
        return None
    i = 1
    while ln in eqcLib[el]['inuse']:
        ln = "%i" % i
        i += 1
    eqcLib[el]['inuse'] += [ln]
    classdef = deepcopy(eqcLib[el]['def'])
    classdef['name'] = '%s_%s' % (el, ln)
    classdef['pNames'] = ['%s{%s}' % (classdef['name'], x)
                          for x in classdef['pNames']]
    classdef['params'] = np.array([-1] * len(classdef['pNames']))
    return classdef

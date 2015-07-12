#!/usr/bin/env python2

import numpy as np
from copy import deepcopy

def Warburg(w,p):
    tan = 0
    denom = np.power(1j*w*p[1],0.5)
    if p[1]*w < 1e5:
        tan = np.tanh(denom)
    else:
        tan = 1.0
    return p[0] * tan/denom

eqcLib = {
    'R':{
        'inuse':[],
        'def':{
            'eqc': lambda w,p: p[0],
            'pNames': ['R'],
        },
    },
    'C':{
        'inuse':[],
        'def':{
            'eqc': lambda w,p: 1.0/(1j*w*p[0]),
            'pNames': ['C'],
        },
    },
    'L':{
        'inuse':[],
        'def':{
            'eqc': lambda w,p: 1j*w*p[0],
            'pNames': ['L'],
        },
    },
    'Zarc':{
        'inuse':[],
        'def':{
            'eqc': lambda w,p: p[0]/(1+np.power(1j*p[1]*omega,p[2])),
            'pNames': ['R','T','n']
        },
    },
    'CPE':{
        'inuse':[],
        'def':{
            'eqc': lambda w,p: 1.0/(p[0]*np.power(1j*w,p[1])),
            'pNames': ['Q','n'],
        },
    },
    'Warb':{
        'inuse':[],
        'def':{
            'eqc': Warburg,
            'pNames': ['R','T'],
        },
    },
}

def getClassDefinition(name):
    el = name
    ln = "1"
    if '_' in name:
        el = name.split('_')[0]
        ln = name.split('_')[1]
    if not el in eqcLib:
        raise ValueError("Unknown element: %s" % el)
        return None
    i = 1
    while ln in eqcLib[el]['inuse']:
        ln = "%i" % i
        i += 1
    eqcLib[el]['inuse'] += [ln]
    classdef = deepcopy(eqcLib[el]['def'])
    classdef['name'] = '%s_%s' % (el, ln)
    classdef['pNames'] = ['%s{%s}' % (classdef['name'], x) \
                          for x in classdef['pNames']]
    classdef['params'] = np.array([-1]*len(classdef['pNames']))
    return classdef

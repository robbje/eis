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

def dWarburg_dp1(w,p):
    tan = 0
    denom = np.power(1j*w*p[1],0.5)
    if p[1]*w < 1e5:
        tan = np.tanh(denom)
    else:
        tan = 1.0
    return p[0]/(2*p[1]*np.power(np.cosh(np.power(1j*w*p[1],0.5)),2.0)) \
            - 1j*p[0]*p[1]*tan/(2*np.power(1j*w*p[1],1.5))

eqcLib = {
    'R':{
        'inuse':[],
        'def':{
            'eqc': lambda w,p: p[0],
            'pNames': ['R'],
            'jac': [lambda w,p: 1],
        },
    },
    'C':{
        'inuse':[],
        'def':{
            'eqc': lambda w,p: 1.0/(1j*w*p[0]),
            'pNames': ['C'],
            'jac': [lambda w,p: -1.0/(1j*w*np.power(p[0],2.0))]
        },
    },
    'L':{
        'inuse':[],
        'def':{
            'eqc': lambda w,p: 1j*w*p[0],
            'pNames': ['L'],
            'jac': [lambda w,p: 1j*w],
        },
    },
    'Zarc':{
        'inuse':[],
        'def':{
            'eqc': lambda w,p: p[0]/(1+np.power(1j*p[1]*omega,p[2])),
            'pNames': ['R','T','n'],
            'jac': [lambda w,p: 1,
                    lambda w,p: -1.0*p[0]*p[2]*np.power(1j*w*p[1],p[2])/ \
                                p[1]*np.power(1.0+np.power(1j*w*p[1],p[2]),2.0),
                    lambda w,p: -1.0*p[0]*np.power(1j*w*p[1],p[2])*np.log(1j*w*p[1])/ \
                                np.power(1.0+np.power(1j*w*p[1],p[2]),2.0)],
        },
    },
    'CPE':{
        'inuse':[],
        'def':{
            'eqc': lambda w,p: 1.0/(p[0]*np.power(1j*w,p[1])),
            'pNames': ['Q','n'],
            'jac': [lambda w,p: -1.0/np.power(p[0],2.0),
                    lambda w,p: np.log(1j*w)/(p[0]*np.power(1j*w,p[1]))],
        },
    },
    'Warb':{
        'inuse':[],
        'def':{
            'eqc': Warburg,
            'pNames': ['R','T'],
            'jac': [lambda w,p: 1,
                    dWarburg_dp1],
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

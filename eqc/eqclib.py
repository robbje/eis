#!/usr/bin/env python2

import numpy as np

eqcLib = {
    'R':{
        'inuse':[],
        'def': {
            'eqc': lambda w,p: p[0],
            'params': [-1]*1,
        },
    },
    'C':{
        'inuse':[],
        'def': {
            'eqc': lambda w,p: 1.0/(1j*w*p[0]),
            'params': [-1]*1,
        },
    },
    'L':{
        'inuse':[],
        'def': {
            'eqc': lambda w,p: 1j*w*p[0],
            'params': [-1]*1,
        },
    },
}

def getClassDefinition(name):
    el = name[0]
    if not el in eqcLib:
        return None
    ln = name[2:] if len(name) > 2 else "1"
    i = 1
    while ln in eqcLib[el]['inuse']:
        ln = "%i" % i
        i += 1
    eqcLib[el]['inuse'] += [ln]
    # Technically, we should do a deepcopy here...
    classdef = eqcLib[el]['def']
    classdef['name'] = '%s_%s' % (el, ln)
    return classdef

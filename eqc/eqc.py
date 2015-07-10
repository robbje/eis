#!/usr/bin/env python2

class Eqc(object):
    def __init__(self, *args, **kwargs):
        self.p = []
        self.eqc = lambda omega,p=self.p: 0
        if 'tree' in kwargs:
            self.eqc, self.p = self.fromTree(kwargs['tree'])
        elif 'func' in kwargs:
            self.p = kwargs['params'] if 'params' in kwargs else []
            self.eqc = lambda omega,p=self.p: kwargs['func'](omega,p)

    def fromParseTree(self, root):
        pass

    def fromLibrary(self, identifier, p):
        pass

    def __add__(self,other):
        pu = len(self.p)
        self.p += other.p
        p = self.p[pu:]
        f = self.eqc
        self.eqc = lambda w,p=self.p: f(w,self.p) + other.eqc(w,self.p[pu:])
        return self

    def __or__(self,other):
        pu = len(self.p)
        self.p += other.p
        f = self.eqc
        self.eqc = lambda w,p=self.p: \
            1.0/(1.0/f(w,self.p)+1.0/other.eqc(w,self.p[pu:]))
        return self

if __name__ == "__main__":
    a = Eqc(func=lambda w,p: p[0], params=[1])
    b = Eqc(func=lambda w,p: p[0], params=[4])
    a |= b
    print "R(1)||R(4)=R(%g)" % a.eqc(0)

#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import runtime

FUNC_DEBUG = False

class OException(Exception): pass

class SchemeObject(object): pass

class ONil(SchemeObject):
    def __repr__(self): return '()'
    def __iter__(self):
        if False: yield 0
nil = ONil()

class OPair(SchemeObject):
    def __init__(self, car=nil, cdr=nil): self.car, self.cdr = car, cdr
    def __repr__(self):
        if isinstance(self.cdr, OPair):
            return '(%s)' % ' '.join(map(str, self))
        elif self.cdr is nil: return '(%s)' % self.car
        else: return '(%s . %s)' % (self.car, self.cdr)
    def __getitem__(self, k):
        p = self
        while k > 0 and p != nil: p, k = p.cdr, k-1
        if p == nil: raise IndexError()
        return p.car
    def __iter__(self):
        p = self
        while p is not nil:
            yield p.car
            p = p.cdr
    def __call__(self, stack, envs, objs):
        stack.call(runtime.CallStatus(self), envs)

def to_list(li):
    ''' make python list to scheme list '''
    p = nil
    for i in reversed(li): p = OPair(i, p)
    return p

def reversed_list(li):
    p = nil
    while li != nil: p, li = OPair(li.car, p), li.cdr
    return p

class OSymbol(SchemeObject):
    def __init__(self, name): self.name = name
    def __repr__(self): return "`" + self.name
    def __call__(self, stack, envs, objs): return envs[self.name]

class OString(SchemeObject):
    def __init__(self, v): self.str = v[1:-1]
    def __repr__(self): return '"%s"' % self.str

class OQuota(SchemeObject):
    def __init__(self): self.objs = None
    def __repr__(self): return "'" + str(self.objs)
    def __call__(self, stack, envs, objs): return self.objs

class OFunction(SchemeObject):
    def __init__(self, name, envs, params, objs):
        self.name, self.envs = name, envs.clone()
        self.params, self.objs, self.evaled = params, objs, True
    def __repr__(self): return '<function %s>' % self.name

    def mkenv(self, objs):
        newenv = self.envs.clonedown()
        pn, pv = self.params, objs
        while pn is not nil and pv is not nil:
            if pn.car.name == '.':
                newenv.add(pn.cdr.car.name, pv)
                break
            newenv.add(pn.car.name, pv.car)
            pn, pv = pn.cdr, pv.cdr
        return newenv

    def __call__(self, stack, envs, objs):
        if FUNC_DEBUG: print 'call', self.name, self.mkenv(objs).stack[-1]
        stack.call(runtime.PrognStatus(self.objs), self.mkenv(objs))

def scompile(obj):
    ''' make python objects to scheme objects '''
    if isinstance(obj, (int, long, float)): return obj
    elif isinstance(obj, (list, tuple)):
        l = map(scompile, obj)
        for i, o in enumerate(l):
            if isinstance(o, OQuota): o.objs = l.pop(i+1)
        return to_list(l)
    elif isinstance(obj, (unicode, str)):
        if isinstance(obj, str): obj = obj.decode('utf-8')
        if obj[0] == '#':
            if obj[1] == 't': return True
            elif obj[1] == 'f': return False
            else: raise Exception('boolean name error')
        elif obj[0] == '"': return OString(obj)
        elif obj[0] == "'": return OQuota()
        elif obj[0].isdigit():
            if '.' in obj: return float(obj)
            else: return int(obj)
        else: return OSymbol(obj)

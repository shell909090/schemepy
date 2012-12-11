#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''

FUNC_DEBUG_NAME, FUNC_DEBUG_END = False, False

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
    def __call__(self, envs):
        func = envs.eval(self.car)
        if not func.evaled: params = self.cdr
        else: params = to_list(map(envs.eval, self.cdr))
        return func(envs, params)

def to_list(li):
    ''' make python list to scheme list '''
    p = nil
    for i in reversed(li): p = OPair(i, p)
    return p

class OSymbol(SchemeObject):
    def __init__(self, name): self.name = name
    def __repr__(self): return "`" + self.name
    def __call__(self, envs): return envs[self.name]

class OString(SchemeObject):
    def __init__(self, v): self.str = v[1:-1]
    def __repr__(self): return '"%s"' % self.str

class OQuota(SchemeObject):
    def __init__(self): self.objs = None
    def __repr__(self): return "'" + str(self.objs)
    def __call__(self, envs): return self.objs

class OFunction(SchemeObject):
    def __init__(self, name, envs, params, objs):
        self.name, self.envs = name, envs.clone()
        self.params, self.objs, self.evaled = params, objs, True
    def __repr__(self): return '<function %s>' % self.name
    def __call__(self, envs, objs):
        with self.envs:
            if FUNC_DEBUG_NAME: print self.name, objs
            pn, pv = self.params, objs
            while pn is not nil and pv is not nil:
                if pn.car.name == '.':
                    self.envs.add(pn.cdr.car.name, pv)
                    break
                self.envs.add(pn.car.name, pv.car)
                pn, pv = pn.cdr, pv.cdr
            r = self.envs.evals(self.objs)
            if FUNC_DEBUG_END: print self.name + ' end', r
            return r

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

class Envs(object):

    def __init__(self, builtin=None):
        self.stack = []
        if builtin: self.stack.append(builtin)
    def clone(self):
        sym = Envs()
        sym.stack = self.stack[:]
        return sym
    def __getitem__(self, name):
        for i in reversed(self.stack):
            if name in i: return i[name]
        raise KeyError(name)

    def add(self, name, value): self.stack[-1][name] = value
    def down(self): self.stack.append({})
    def up(self): self.stack.pop()
    def __enter__(self): self.stack.append({})
    def __exit__(self, tp, value, traceback): self.stack.pop()

    # trampoline化
    def eval(self, objs):
        if hasattr(objs, '__call__'): return objs(self)
        return objs
    def evals(self, objs):
        for o in objs: r = self.eval(o)
        return r

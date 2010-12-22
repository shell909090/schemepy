#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''

class OException(Exception): pass

class SchemeObject(object): pass

class ONil(SchemeObject):
    def __repr__(self): return '()'
    def __iter__(self):
        if False: yield 0
nil = ONil()

class OPair(SchemeObject):
    def __init__(self, car = nil, cdr = nil): self.car, self.cdr = car, cdr
    def __repr__(self):
        if isinstance(self.cdr, OPair):
            return '(%s)' % ' '.join(map(str, self))
        elif self.cdr is nil: return '(%s)' % self.car
        else: return '(%s . %s)' % (self.car, self.cdr)
    def __iter__(self):
        p = self
        while p is not nil:
            yield p.car
            p = p.cdr
    def __getitem__(self, k):
        p = self
        while k > 0:
            p = p.cdr
            k -= 1
        return p.car
    def _eval(self, envs):
        func = envs.eval(self.car)
        if not func.evaled: params = self.cdr
        else: params = to_list(map(envs.eval, self.cdr))
        return func(envs, params)

class OSymbol(SchemeObject):
    def __init__(self, name): self.name = name
    def __repr__(self): return "`" + self.name
    def _eval(self, envs): return envs[self.name]

class OString(SchemeObject):
    def __init__(self, v): self.str = v[1:-1]
    def __repr__(self): return '"%s"' % self.str

class OQuota(SchemeObject):
    def __init__(self): self.objs = None
    def __repr__(self): return "'" + str(self.objs)
    def _eval(self, envs): return self.objs

def to_scheme(obj):
    ''' make python objects to scheme objects '''
    if isinstance(obj, (int, long, float)): return obj
    elif isinstance(obj, (list, tuple)): return to_list(map(to_scheme, obj))
    elif isinstance(obj, (unicode, str)): return str_to_scheme(obj)

def to_list(li):
    ''' make python list to scheme list '''
    p = nil
    for i in reversed(li):
        p = OPair(i, p)
        if isinstance(p.car, OQuota) and p.car.objs is None:
            if p.cdr is nil: raise Exception(li)
            p.car.objs = p.cdr.car
            p.cdr = p.cdr.cdr
    return p

number_str = '1234567890'
def str_to_scheme(obj):
    if isinstance(obj, str): obj = obj.decode('utf-8')
    if obj[0] == '#':
        if obj[1] == 't': return True
        elif obj[1] == 'f': return False
        else: raise Exception('boolean name error')
    elif obj[0] == '"': return OString(obj)
    elif obj[0] == "'": return OQuota()
    elif obj[0] in number_str:
        if '.' in obj: return float(obj)
        else: return int(obj)
    else: return OSymbol(obj)

class Envs(object):

    def __init__(self): self.stack = [{},]
    def clone(self):
        sym = Envs()
        sym.stack = self.stack[:]
        return sym
    def __contain__(self, name):
        for i in self.stack:
            if name in i: return True
        return False
    def __getitem__(self, name):
        for i in reversed(self.stack):
            if name in i: return i[name]
        raise KeyError(name)
    def add(self, name, value): self.stack[-1][name] = value
    def down(self): self.stack.append({})
    def up(self): self.stack.pop()
    def __enter__(self): self.stack.append({})
    def __exit__(self, tp, value, traceback): self.stack.pop()
    def decorater(self, name, evaled = None):
        def inner(func):
            if evaled is not None: func.evaled = evaled
            self.add(name, func)
            return func
        return inner

    def eval(self, objs):
        # print 'eval', objs
        if hasattr(objs, '_eval'): return objs._eval(self)
        return objs
    def evals(self, objs):
        for o in objs: r = self.eval(o)
        return r

default_env = Envs()

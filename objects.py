#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''

FUNC_DEBUG = False

class SchemeObject(object): pass

class ONil(SchemeObject):
    def __new__(cls, *p, **kw):
        if not hasattr(cls, 'nil'): cls.nil = object.__new__(cls, *p, **kw)
        return cls.nil
    def __setstate__(self, state): return nil
    def __repr__(self): return '()'
    def __iter__(self):
        if False: yield
nil = ONil()

class OPair(SchemeObject):
    def __init__(self, car=nil, cdr=nil):
        self.car, self.cdr = car, cdr
    def __repr__(self):
        if isinstance(self.cdr, OPair):
            return '(%s)' % ' '.join(map(str, self))
        elif self.cdr is nil: return '(%s)' % self.car
        else: return '(%s . %s)' % (self.car, self.cdr)
    def __getitem__(self, k):
        p = self
        while k > 0 and p is not nil: p, k = p.cdr, k-1
        if p is nil: raise IndexError()
        return p.car
    def __iter__(self):
        p = self
        while p is not nil:
            yield p.car
            p = p.cdr
    def __call__(self, stack, envs, objs):
        raise Exception('this should never happen')

def to_list(li):
    ''' make python list to scheme list '''
    p = nil
    for i in reversed(li): p = OPair(i, p)
    return p

def reversed_list(li):
    p = nil
    while li is not nil: p, li = OPair(li.car, p), li.cdr
    return p

class OSymbol(SchemeObject):
    def __init__(self, name): self.name = name
    def __repr__(self): return "`" + self.name

class OString(SchemeObject):
    def __init__(self, v): self.str = v[1:-1]
    def __repr__(self): return '"%s"' % self.str

class OQuota(SchemeObject):
    def __init__(self): self.objs = None
    def __repr__(self): return "'" + str(self.objs)

class OFunction(SchemeObject):
    def __init__(self, name, envs, params, objs):
        self.name, self.envs = name, envs.clone()
        self.params, self.objs, self.evaled = params, objs, True
    def __repr__(self): return '<function %s>' % self.name

    def __call__(self, stack, envs, objs):
        newenv = self.envs.clonedown()
        pn, pv = self.params, objs
        while pn is not nil and pv is not nil:
            if pn[0].name == '.':
                newenv.add(pn.cdr.car.name, pv)
                break
            newenv.add(pn.car.name, pv.car)
            pn, pv = pn.cdr, pv.cdr
        if FUNC_DEBUG: print 'call', self.name, newenv.stack[-1]
        return stack.jump(PrognStatus(self.objs), newenv)

def scompile(obj):
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

class PrognStatus(object):
    def __init__(self, objs):
        self.objs, self.rslt = objs, None
    def __repr__(self): return 'progn ' + str(self.objs)

    def __call__(self, stack, envs, objs):
        if self.objs.cdr == nil: return stack.jump(self.objs.car, envs)
        t, self.objs = self.objs.car, self.objs.cdr
        return stack.call(t, envs)

class CallStatus(object):
    def __init__(self, objs): self.objs = objs
    def __repr__(self): return 'call ' + str(self.objs)

    def __call__(self, stack, envs, objs):
        if objs is None: return stack.call(self.objs[0], envs)
        if not objs.evaled:
            return stack.jump(ParamStatus(objs, self.objs.cdr, nil), envs)
        return stack.jump(ParamStatus(objs, nil,
                                      reversed_list(self.objs.cdr)), envs)

class ParamStatus(object):
    def __init__(self, func, params, objs):
        self.func, self.params, self.objs = func, params, objs
    def __repr__(self):
        return 'call %s with (%s) <- (%s)' % (self.func, self.params, self.objs)

    def __call__(self, stack, envs, objs):
        if objs is not None: self.params = OPair(objs, self.params)
        if self.objs is nil: return stack.jump(self.func, envs, self.params)
        t, self.objs = self.objs.car, self.objs.cdr
        return stack.call(t, envs)

# class Envs(object):
#     def __init__(self, stack=None, builtin=None):
#         if stack is not None: self.stack = stack
#         else:
#             self.stack = []
#             if builtin: self.stack.append(builtin)
#     def clone(self): return Envs(stack=self.stack[:])
#     def clonedown(self): return Envs(self.stack[:] + [{},])
#     def add(self, name, value): self.stack[-1][name] = value
#     def __getitem__(self, name):
#         for i in reversed(self.stack):
#             if name in i: return i[name]
#         raise KeyError(name)

class Envs(object):
    def __init__(self, e=None, builtin=None):
        if e is not None: self.e = e
        elif builtin is not None: self.e = OPair(builtin)
        else: self.e = nil
    def clone(self): return Envs(e=self.e)
    def clonedown(self): return Envs(OPair({}, self.e))
    def add(self, name, value): self.e.car[name] = value
    def __getitem__(self, name):
        for i in self.e:
            if name in i: return i[name]
        raise KeyError(name)

class Stack(list):

    def save(self, f):
        self[0].envs.e.car = {}
        __import__('cPickle').dump(self, f, 2)
    @classmethod
    def load(cls, f, builtin):
        stack = __import__('cPickle').load(f)
        stack[0].envs.e.car.update(builtin)
        return stack

    def call(self, func, envs, args=None):
        if isinstance(func, OSymbol): return (envs[func.name],)
        if isinstance(func, OQuota): return (func.objs,)
        if not callable(func): return (func,)
        if isinstance(func, OPair):
            self.append((CallStatus(func), envs))
        else: self.append((func, envs))
        return (args,)

    def jump(self, func, envs, args=None):
        if isinstance(func, OSymbol): return (envs[func.name], self.pop(-1))
        if isinstance(func, OQuota): return (func.objs, self.pop(-1))
        if not callable(func): return (func, self.pop(-1))
        if isinstance(func, OPair):
            self[-1] = (CallStatus(func), envs)
        else: self[-1] = (func, envs)
        return (args,)

    def trampoline(self, r=None):
        while self:
            # print 'result:', r
            # __import__('pprint').pprint([i[0] for i in self])
            o = self[-1]
            r = o[0](self, o[1], r)
            if isinstance(r, tuple): r = r[0]
            else: self.pop(-1)
        return r

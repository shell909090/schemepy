#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2012-12-18
@author: shell.xu
'''
from collections import deque
from objects import *

all = ['Stack', 'BreakException', 'ResumeInfo']

class BreakException(StandardError): pass

class ResumeInfo(object):
    def __init__(self, s): self.s = s

class OFunction(object):
    def __init__(self, name, envs, params, objs):
        self.name, self.envs = name, envs
        self.params, self.objs, self.evaled = params, objs, True

    def __repr__(self):
        return '<function %s>' % self.name

    def __call__(self, stack, envs, objs):
        r, pn, pv = {}, self.params, objs
        while pn is not nil and pv is not nil:
            if pn[0].name == '.':
                r[pn[1].name] = pv
                break
            r[pn[0].name] = pv[0]
            pn, pv = pn.cdr, pv.cdr
        newenv = self.envs.fork(r)
        if FUNC_DEBUG: print 'call', self.name, newenv.stack[-1]
        return stack.jump(PrognStatus(self.objs), newenv)

class PrognStatus(object):
    def __init__(self, objs):
        self.objs, self.rslt = objs, None

    def __repr__(self):
        return 'progn ' + str(self.objs)

    def __call__(self, stack, envs, objs):
        if self.objs.cdr == nil: return stack.jump(self.objs.car, envs)
        t, self.objs = self.objs.car, self.objs.cdr
        return stack.call(t, envs)

class FuncStatus(object):
    def __init__(self, objs):
        self.objs = objs

    def __repr__(self):
        return str(self.objs)

    def __call__(self, stack, envs, objs):
        if objs is None:
            return stack.call(self.objs[0], envs)
        if not objs.evaled:
            return stack.jump(CallStatus(objs, self.objs.cdr, nil), envs)
        return stack.jump(CallStatus(objs, nil, reversed_list(self.objs.cdr)),
                envs)

class CallStatus(object):
    def __init__(self, func, params, objs):
        self.func, self.params, self.objs = func, params, objs

    def __repr__(self):
        return 'call %s with (%s) <- (%s)' % (self.func, self.params, self.objs)

    def __call__(self, stack, envs, objs):
        if objs is not None: self.params = OCons(objs, self.params)
        if self.objs is nil: return stack.jump(self.func, envs, self.params)
        t, self.objs = self.objs.car, self.objs.cdr
        return stack.call(t, envs)

class Envs(object):
    def __init__(self, e=None):
        self.e, self.fast = e, {}
        self.genfast()

    def __getstate__(self):
        return self.e

    def __setstate__(self, state):
        self.e, self.fast = state, {}

    def __repr__(self):
        return objects.format_list(self.e)

    def genfast(self):
        for i in reversed_list(self.e):
            self.fast.update(i)

    def fork(self, r=None):
        if r is None: r = {}
        return Envs(OCons(r, self.e))

    def add(self, name, value):
        self.fast[name] = value
        self.e.car[name] = value

    def __getitem__(self, name):
        return self.fast[name]

class Stack(deque):
    def save(self, r, f):
        self[0][1].e[1] = {}
        __import__('cPickle').dump((self, r), f, 2)

    @classmethod
    def load(cls, f, builtin):
        stack, r = __import__('cPickle').load(f)
        stack[0][1].e[1] = builtin
        for s in stack: s[1].genfast()
        return stack, ResumeInfo(r)

    def func_call(self, func, envs):
        o = func[0]
        if not isinstance(o, OSymbol): return FuncStatus(func)
        objs = envs[o.name]
        if not objs.evaled: return CallStatus(objs, func.cdr, nil)
        return CallStatus(objs, nil, reversed_list(func.cdr))

    def call(self, func, envs, args=None):
        if isinstance(func, OSymbol):
            return (envs[func.name],)
        if isinstance(func, OQuote):
            return (func.objs,)
        if isinstance(func, OCons):
            self.append((self.func_call(func, envs), envs))
        elif not callable(func):
            return (func,)
        else:
            self.append((func, envs))
        return (args,)

    def jump(self, func, envs, args=None):
        if isinstance(func, OSymbol):
            return (envs[func.name], self.pop())
        if isinstance(func, OQuote):
            return (func.objs, self.pop())
        if isinstance(func, OCons):
            self[-1] = (self.func_call(func, envs), envs)
        elif not callable(func):
            return (func, self.pop())
        else:
            self[-1] = (func, envs)
        return (args,)

    def trampoline(self, r=None, debug=None, coredump=None):
        try:
            while self:
                if debug is not None: debug(self, r)
                o = self[-1]
                r = o[0](self, o[1], r)
                if isinstance(r, tuple): r = r[0]
                else: self.pop()
            return r
        except Exception, err:
            if coredump:
                if isinstance(coredump, basestring):
                    with open(coredump, 'wb') as cd:
                        self.save(r, cd)
                else:
                    self.save(r, coredump)
            raise

def init(code, builtin):
    stack = Stack()
    stack.append((PrognStatus(code), Envs(to_list([{}, builtin,]))))
    return stack

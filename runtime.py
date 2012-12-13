#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2012-12-11
@author: shell.xu
'''
from pprint import pprint
import objects

class Envs(object):

    def __init__(self, stack=None, builtin=None):
        if stack is not None: self.stack = stack
        else:
            self.stack = []
            if builtin: self.stack.append(builtin)
    def clone(self): return Envs(stack=self.stack[:])
    def clonedown(self): return Envs(self.stack[:] + [{},])

    def add(self, name, value): self.stack[-1][name] = value
    def __getitem__(self, name):
        for i in reversed(self.stack):
            if name in i: return i[name]
        raise KeyError(name)

# class ControlBreak(StandardError):
#     def __init__(self, 

class Frame(object):
    def __init__(self, func, envs):
        self.func, self.envs = func, envs
        if hasattr(self.func, 'next'):
            self.next = lambda stack, r: self.func.next(stack, self.envs, r)
    def __repr__(self): return str(self.func)
    def __call__(self, stack, r):
        if not callable(self.func): return self.func
        return self.func(stack, self.envs, r)

class Stack(list):
    def call(self, o, env): self.append(Frame(o, env))
    def trampoline(self):
        r = None
        while self:
            # pprint(self)
            o = self[-1]
            if hasattr(o, 'next') and o.next(self, r): r = None
            else: r = self.pop(-1)(self, r)
        return r

class PrognStatus(object):
    def __init__(self, objs):
        self.objs, self.rslt = objs, None
    def __repr__(self): return 'progn ' + str(self.objs)

    def next(self, stack, env, objs):
        if self.objs.cdr == objects.nil: return False
        stack.call(self.objs.car, env)
        self.objs = self.objs.cdr
        return True
    def __call__(self, stack, env, objs):
        stack.call(self.objs.car, env)

class CallStatus(object):
    def __init__(self, objs): self.objs = objs
    def __repr__(self): return 'call ' + str(self.objs)
    def next(self, stack, envs, objs):
        if objs is None:
            stack.call(self.objs[0], envs)
            return True
        if not objs.evaled:
            self.ps = ParamStatus(objs, self.objs.cdr, objects.nil)
        else:
            self.ps = ParamStatus(objs, objects.nil,
                                  objects.reversed_list(self.objs.cdr))
        return False
    def __call__(self, stack, env, objs): stack.call(self.ps, env)

class ParamStatus(object):
    def __init__(self, func, params, objs):
        self.func, self.params, self.objs = func, params, objs
    def __repr__(self):
        return 'call %s with (%s) <- (%s)' % (self.func, self.params, self.objs)
    def next(self, stack, envs, objs):
        if objs is not None: self.params = objects.OPair(objs, self.params)
        if self.objs == objects.nil: return False
        stack.call(self.objs.car, envs)
        self.objs = self.objs.cdr
        return True
    def __call__(self, stack, envs, objs):
        stack.call(self.func, envs)
        return self.params


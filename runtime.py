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

    # trampoline化
    # def eval(self, stack, objs):
    #     if hasattr(objs, 'next'): raise Exception("env.eval with a stackful obj")
    #     if hasattr(objs, '__call__'): return objs(stack, self, None)
    #     return objs

class PrognFrame(object):
    def __init__(self, objs):
        self.objs, self.rslt = objs, None
    def __repr__(self): return 'progn ' + str(self.objs)

    def next(self, stack, env, objs):
        if self.objs.cdr == objects.nil:
            return False
        stack.call(self.objs.car, env)
        self.objs = self.objs.cdr
        return True
    def __call__(self, stack, env, objs):
        stack.call(self.objs.car, env)

class CallFrame(object):
    def __init__(self, objs):
        self.func, self.params, self.objs = None, objects.nil, objs
    def __repr__(self):
        return 'call %s with (%s) <- (%s)' % (self.func, self.params, self.objs)

    def next(self, stack, env, objs):
        if objs is None: stack.call(self.objs[0], env)
        elif self.func is None:
            self.func = objs
            if not self.func.evaled:
                self.params = self.objs.cdr
                return False
            self.objs = objects.reversed_list(self.objs.cdr)
        else:
            self.params = objects.OPair(objs, self.params)
            if self.objs == objects.nil: return False
            stack.call(self.objs.car, env)
            self.objs = self.objs.cdr
        return True

    def __call__(self, stack, env, objs):
        stack.call(self.func, env)
        return self.params

class EvalFrame(object):
    def __init__(self, objs, envs):
        self.objs, self.envs = objs, envs
        if hasattr(objs, 'next'):
            self.next = lambda stack, r: objs.next(stack, envs, r)
    def __repr__(self): return str(self.objs)
    def __call__(self, stack, r):
        if not hasattr(self.objs, '__call__'): return self.objs
        return self.objs(stack, self.envs, r)

class Stack(list):
    def call(self, o, env): self.append(EvalFrame(o, env))
    def trampoline(self):
        r = None
        while self:
            # pprint(self)
            o = self[-1]
            if hasattr(o, 'next') and o.next(self, r): r = None
            else: r = self.pop(-1)(self, r)
        return r

def run(ast, builtin):
    stack = Stack()
    stack.call(PrognFrame(ast), Envs(builtin=builtin))
    return stack.trampoline()

#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2012-12-11
@author: shell.xu
'''
import parser, objects

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

class ControlBreak(StandardError): pass

class Frame(object):
    def __init__(self, func, envs): self.func, self.envs = func, envs
    def __repr__(self): return str(self.func)
    def __call__(self, stack, r):
        if not callable(self.func): return self.func
        return self.func(stack, self.envs, r)

from pprint import pprint
class Stack(list):
    def call(self, func, envs, args=None):
        self.append(Frame(func, envs))
        raise ControlBreak(args)
    def jump(self, func, envs, args=None):
        self[-1] = Frame(func, envs)
        raise ControlBreak(args)
    def trampoline(self):
        r = None
        while self:
            # print 'result:', r
            # pprint(self)
            try:
                r = self[-1](self, r)
                self.pop(-1)
            except ControlBreak, cb: r = cb.args[0]
        return r

def run(src, builtin):
    code = objects.scompile(parser.split_code_tree(src))
    stack = Stack()
    stack.append(Frame(PrognStatus(code), Envs(builtin=builtin)))
    return stack.trampoline()

class PrognStatus(object):
    def __init__(self, objs):
        self.objs, self.rslt = objs, None
    def __repr__(self): return 'progn ' + str(self.objs)

    def __call__(self, stack, envs, objs):
        if self.objs.cdr == objects.nil: stack.jump(self.objs.car, envs)
        t, self.objs = self.objs.car, self.objs.cdr
        stack.call(t, envs)

class CallStatus(object):
    def __init__(self, objs): self.objs = objs
    def __repr__(self): return 'call ' + str(self.objs)

    def __call__(self, stack, envs, objs):
        if objs is None: stack.call(self.objs[0], envs)
        if not objs.evaled:
            stack.jump(ParamStatus(objs, self.objs.cdr, objects.nil), envs)
        stack.jump(ParamStatus(objs, objects.nil,
                               objects.reversed_list(self.objs.cdr)), envs)

class ParamStatus(object):
    def __init__(self, func, params, objs):
        self.func, self.params, self.objs = func, params, objs
    def __repr__(self):
        return 'call %s with (%s) <- (%s)' % (self.func, self.params, self.objs)

    def __call__(self, stack, envs, objs):
        if objs is not None: self.params = objects.OPair(objs, self.params)
        if self.objs == objects.nil: stack.jump(self.func, envs, self.params)
        t, self.objs = self.objs.car, self.objs.cdr
        stack.call(t, envs)


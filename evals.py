#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import objects

class Envs(object):

    def __init__(self): self.stack = [{},]
    def clone(self):
        sym = Envs()
        sym.stack = self.stack[:]
        return sym
    def __contain__(self, name):
        for i in reversed(self.stack):
            if name in i: return True
        return False
    def __getitem__(self, name):
        for i in reversed(self.stack):
            if name in i: return i[name]
        raise KeyError(name)
    def add(self, name, value): self.stack[-1][name] = value
    def down(self): self.stack.append({})
    def up(self): self.stack.pop()

    def eval(self, objs):
        if objs is None: return None
        # print 'eval', objs
        if isinstance(objs, objects.OQuota): return objs.objs
        elif isinstance(objs, objects.OSymbol): return self[objs.name]
        elif isinstance(objs, objects.OPair):
            function = self.eval(objs.car)
            if function.e:
                evaled = []
                for o in objs.cdr: evaled.append(self.eval(o))
                params = objects.make_list(evaled)
            else: params = objs.cdr
            return function(self, params)
        return objs
    def evals(self, objs):
        for o in objs: r = self.eval(o)
        return r


default_env = Envs()

#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2013-06-25
@author: shell.xu
'''
import objects, interrupter
from symbol import define

# list functions
@define(u'list', True)
def list_list(stack, envs, objs): return objs

@define(u'null?', True)
def list_null(stack, envs, objs): return objs[0] is objects.nil

@define(u'pair?', True)
def list_pair(stack, envs, objs): return isinstance(objs[0], objects.OCons)

@define(u'cons', True)
def list_cons(stack, envs, objs): return objects.OCons(objs[0], objs[1])

@define(u'car', True)
def list_car(stack, envs, objs): return objs[0].car

@define(u'cdr', True)
def list_cdr(stack, envs, objs): return objs[0].cdr

@define(u'caar', True)
def list_caar(stack, envs, objs): return objs[0].car.car

@define(u'cadr', True)
def list_cadr(stack, envs, objs): return objs[0].cdr.car

@define(u'cdar', True)
def list_cdar(stack, envs, objs): return objs[0].car.cdr

@define(u'caddr', True)
def list_caddr(stack, envs, objs): return objs[0].cdr.cdr.car

@define(u'append', True)
def list_append(stack, envs, objs):
    r = []
    for obj in objs: r.extend(obj)
    return objects.to_list(r)

class MapStatus(object):
    def __init__(self, func, params):
        self.func, self.params, self.r = func, params, []
    def __repr__(self): return u'map %s -> (%s)' % (self.func, self.params)

    def __call__(self, stack, envs, objs):
        if objs is not None: self.r.append(objs)
        if self.params[0] is objects.nil: return objects.to_list(self.r)
        t = map(lambda i: i.car, self.params)
        self.params = map(lambda i: i.cdr, self.params)
        return stack.call(interrupter.CallStatus(
                self.func, objects.to_list(t), objects.nil), envs)

@define(u'map', True)
def list_map(stack, envs, objs):
    return stack.jump(MapStatus(objs.car, objs.cdr), envs)

class FilterStatus(object):
    def __init__(self, func, params):
        self.func, self.params, self.r = func, params, []
    def __repr__(self): return u'filter %s -> (%s)' % (self.func, self.params)

    def __call__(self, stack, envs, objs):
        if objs is not None:
            if objs: self.r.append(self.params.car)
            self.params = self.params.cdr
        if self.params is objects.nil: return objects.to_list(self.r)
        return stack.call(interrupter.CallStatus(
                self.func, objects.OCons(self.params.car), objects.nil), envs)

@define(u'filter', True)
def list_filter(stack, envs, objs):
    return stack.jump(FilterStatus(objs[0], objs[1]), envs)

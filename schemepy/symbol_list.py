#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@date: 2013-06-25
@author: shell.xu
'''
from schemepy import objects, interrupter, symbol
define = symbol.define

# list functions
@define('list', True)
def list_list(_, _1, objs):
    return objs

@define('null?', True)
def list_null(_, _1, objs):
    return objs[0] is objects.nil

@define('pair?', True)
def list_pair(_, _1, objs):
    return isinstance(objs[0], objects.OCons)

@define('cons', True)
def list_cons(_, _1, objs):
    return objects.OCons(objs[0], objs[1])

@define('car', True)
def list_car(_, _1, objs):
    return objs[0].car

@define('cdr', True)
def list_cdr(_, _1, objs):
    return objs[0].cdr

@define('caar', True)
def list_caar(_, _1, objs):
    return objs[0].car.car

@define('cadr', True)
def list_cadr(_, _1, objs):
    return objs[0].cdr.car

@define('cdar', True)
def list_cdar(_, _1, objs):
    return objs[0].car.cdr

@define('caddr', True)
def list_caddr(_, _1, objs):
    return objs[0].cdr.cdr.car

@define('append', True)
def list_append(_, _1, objs):
    r = []
    for obj in objs:
        r.extend(obj)
    return objects.to_list(r)

class MapStatus(object):
    def __init__(self, func, params):
        self.func, self.params, self.r = func, params, []

    def __repr__(self):
        return 'map %s -> (%s)' % (self.func, self.params)

    def __call__(self, stack, envs, objs):
        if objs is not None:
            self.r.append(objs)
        if self.params[0] is objects.nil:
            return objects.to_list(self.r)
        t = [i.car for i in self.params]
        self.params = [i.cdr for i in self.params]
        return stack.call(interrupter.CallStatus(
                self.func, objects.to_list(t), objects.nil), envs)

@define('map', True)
def list_map(stack, envs, objs):
    return stack.jump(MapStatus(objs.car, objs.cdr), envs)

class FilterStatus(object):
    def __init__(self, func, params):
        self.func, self.params, self.r = func, params, []

    def __repr__(self):
        return 'filter %s -> (%s)' % (self.func, self.params)

    def __call__(self, stack, envs, objs):
        if objs is not None:
            if objs:
                self.r.append(self.params.car)
            self.params = self.params.cdr
        if self.params is objects.nil:
            return objects.to_list(self.r)
        return stack.call(interrupter.CallStatus(
                self.func, objects.OCons(self.params.car), objects.nil), envs)

@define('filter', True)
def list_filter(stack, envs, objs):
    return stack.jump(FilterStatus(objs[0], objs[1]), envs)

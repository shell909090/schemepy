#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import objects

@objects.default_env.decorater('list', True)
def list_list(symbols, objs):
    return objs

@objects.default_env.decorater('null?', True)
def list_null(symbols, objs):
    return objs.car is None

@objects.default_env.decorater('pair?', True)
def list_pair(symbols, objs):
    return isinstance(objs.car, objects.OPair)

@objects.default_env.decorater('cons', True)
def list_cons(symbols, objs):
    return objects.OPair(objs[0], objs[1])

@objects.default_env.decorater('car', True)
def list_car(symbols, objs):
    return objs.car.car

@objects.default_env.decorater('cdr', True)
def list_cdr(symbols, objs):
    return objs.car.cdr

@objects.default_env.decorater('caar', True)
def list_caar(symbols, objs):
    return objs.car.car.car

@objects.default_env.decorater('cadr', True)
def list_cadr(symbols, objs):
    return objs.car.cdr.car

@objects.default_env.decorater('cdar', True)
def list_cdar(symbols, objs):
    return objs.car.car.cdr

@objects.default_env.decorater('caddr', True)
def list_caddr(symbols, objs):
    return objs.car.cdr.cdr.car

@objects.default_env.decorater('append', True)
def list_append(symbols, objs):
    r = []
    for obj in objs:
        if obj is None: continue
        for o in obj: r.append(o)
    return objects.make_list(r)

@objects.default_env.decorater('map', True)
def list_map(symbols, objs):
    # TODO: to_python似乎不应当用
    l, r = objects.to_python(objs.cdr), []
    while l[0]:
        t = map(lambda i: i.car, l)
        r.append(objs.car(symbols, objects.make_list(t)))
        l = map(lambda i: i.cdr, l)
    return objects.make_list(r)

@objects.default_env.decorater('filter', True)
def list_filter(symbols, objs):
    if objs[1] is None: return None
    r = []
    for o in objs[1]:
        if objs.car(symbols, objects.make_list([o,])): r.append(o)
    return objects.make_list(r)

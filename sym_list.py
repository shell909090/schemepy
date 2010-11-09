#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import objects
import evals

def list_list(symbols, objs):
    return objs
evals.default_env.add('list', list_list, True)

def list_null(symbols, objs):
    return objs.car is None
evals.default_env.add('null?', list_null, True)

def list_pair(symbols, objs):
    return isinstance(objs.car, objects.OPair)
evals.default_env.add('pair?', list_pair, True)

def list_cons(symbols, objs):
    return objects.OPair(objs[0], objs[1])
evals.default_env.add('cons', list_cons, True)

def list_car(symbols, objs):
    return objs.car.car
evals.default_env.add('car', list_car, True)

def list_cdr(symbols, objs):
    return objs.car.cdr
evals.default_env.add('cdr', list_cdr, True)

def list_caar(symbols, objs):
    return objs.car.car.car
evals.default_env.add('caar', list_caar, True)

def list_cadr(symbols, objs):
    return objs.car.cdr.car
evals.default_env.add('cadr', list_cadr, True)

def list_cdar(symbols, objs):
    return objs.car.car.cdr
evals.default_env.add('cdar', list_cdar, True)

def list_caddr(symbols, objs):
    return objs.car.cdr.cdr.car
list_caddr.e = True
evals.default_env.add('caddr', list_caddr)

def list_append(symbols, objs):
    r = []
    for obj in objs:
        if obj is None: continue
        for o in obj: r.append(o)
    return objects.make_list(r)
evals.default_env.add('append', list_append, True)

def list_map(symbols, objs):
    l, r = objects.load_list(objs.cdr), []
    while l[0]:
        t = map(lambda i: i.car, l)
        r.append(objs.car(symbols, objects.make_list(t)))
        l = map(lambda i: i.cdr, l)
    return objects.make_list(r)
evals.default_env.add('map', list_map, True)

def list_filter(symbols, objs):
    if objs[1] is None: return None
    r = []
    for o in objs[1]:
        if objs.car(symbols, objects.make_list([o,])): r.append(o)
    return objects.make_list(r)
evals.default_env.add('filter', list_filter, True)

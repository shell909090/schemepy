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
list_list.e = True
evals.default_env.add('list', list_list)

def list_null(symbols, objs):
    return objs.car is None
list_null.e = True
evals.default_env.add('null?', list_null)

def list_cons(symbols, objs):
    return objects.OPair(objs.car, objs.cdr.car)
list_cons.e = True
evals.default_env.add('cons', list_cons)

def list_car(symbols, objs):
    return objs.car.car
list_car.e = True
evals.default_env.add('car', list_car)

def list_cdr(symbols, objs):
    return objs.car.cdr
list_cdr.e = True
evals.default_env.add('cdr', list_cdr)

#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import evals

def num_add(symbols, objs):
    p, s = objs, 0
    while p:
        s += p.car
        p = p.cdr
    return s
num_add.e = True
evals.default_env.add('+', num_add)

def num_dec(symbols, objs):
    p, s = objs.cdr, objs.car
    while p:
        s -= p.car
        p = p.cdr
    return s
num_dec.e = True
evals.default_env.add('-', num_dec)

def num_eq(symbols, objs):
    assert(isinstance(objs.car, (int, long, float)))
    assert(isinstance(objs.cdr.car, (int, long, float)))
    return objs.car == objs.cdr.car
num_eq.e = True
evals.default_env.add('=', num_eq)

def num_lt(symbols, objs):
    assert(isinstance(objs.car, (int, long, float)))
    assert(isinstance(objs.cdr.car, (int, long, float)))
    return objs.car < objs.cdr.car
num_lt.e = True
evals.default_env.add('<', num_lt)

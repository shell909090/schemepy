#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import evals

def num_number(symbols, objs):
    return isinstance(objs.car, (int, long, float))
num_number.e = True
evals.default_env.add('number?', num_number)

def num_add(symbols, objs):
    return sum(objs)
num_add.e = True
evals.default_env.add('+', num_add)

def num_dec(symbols, objs):
    s = objs.car
    for o in objs.cdr: s -= o
    return s
num_dec.e = True
evals.default_env.add('-', num_dec)

def num_mul(symbols, objs):
    return reduce(lambda x, y: x*y, objs)
num_mul.e = True
evals.default_env.add('*', num_mul)

def num_eq(symbols, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] == objs[1]
num_eq.e = True
evals.default_env.add('=', num_eq)

def num_lt(symbols, objs):
    assert(isinstance(objs[0], (int, long, float)))
    assert(isinstance(objs[1], (int, long, float)))
    return objs[0] < objs[1]
num_lt.e = True
evals.default_env.add('<', num_lt)

def num_remainder(symbols, objs):
    return objs[0] % objs[1]
num_remainder.e = True
evals.default_env.add('remainder', num_remainder)

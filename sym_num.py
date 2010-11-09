#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import evals

def num_number(symbols, objs):
    return isinstance(objs.car, (int, long, float))
evals.default_env.add('number?', num_number, True)

def num_add(symbols, objs):
    return sum(objs)
evals.default_env.add('+', num_add, True)

def num_dec(symbols, objs):
    s = objs.car
    for o in objs.cdr: s -= o
    return s
evals.default_env.add('-', num_dec, True)

def num_mul(symbols, objs):
    return reduce(lambda x, y: x*y, objs)
evals.default_env.add('*', num_mul, True)

def num_eq(symbols, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] == objs[1]
evals.default_env.add('=', num_eq, True)

def num_lt(symbols, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] < objs[1]
evals.default_env.add('<', num_lt, True)

def num_gt(symbols, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] > objs[1]
evals.default_env.add('>', num_gt, True)

def num_nlt(symbols, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] >= objs[1]
evals.default_env.add('>=', num_nlt, True)

def num_remainder(symbols, objs):
    return objs[0] % objs[1]
evals.default_env.add('remainder', num_remainder, True)

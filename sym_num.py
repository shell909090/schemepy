#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import objects

@objects.default_env.decorater('number?', True)
def num_number(symbols, objs):
    return isinstance(objs.car, (int, long, float))

@objects.default_env.decorater('+', True)
def num_add(symbols, objs):
    return sum(objs)

@objects.default_env.decorater('-', True)
def num_dec(symbols, objs):
    s = objs.car
    for o in objs.cdr: s -= o
    return s

@objects.default_env.decorater('*', True)
def num_mul(symbols, objs):
    return reduce(lambda x, y: x*y, objs)

@objects.default_env.decorater('=', True)
def num_eq(symbols, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] == objs[1]

@objects.default_env.decorater('<', True)
def num_lt(symbols, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] < objs[1]

@objects.default_env.decorater('>', True)
def num_gt(symbols, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] > objs[1]

@objects.default_env.decorater('>=', True)
def num_nlt(symbols, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] >= objs[1]

@objects.default_env.decorater('remainder', True)
def num_remainder(symbols, objs):
    return objs[0] % objs[1]

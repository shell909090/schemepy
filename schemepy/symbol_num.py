#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@date: 2013-06-25
@author: shell.xu
'''
from schemepy import symbol
from functools import reduce
define = symbol.define

# number functions
@define('number?', True)
def num_number(_, _1, objs):
    return isinstance(objs[0], (int, float))

@define('+', True)
def num_add(_, _1, objs):
    return sum(objs)

@define('-', True)
def num_dec(_, _1, objs):
    s = objs[0]
    for o in objs.cdr:
        s -= o
    return s

@define('*', True)
def num_mul(_, _1, objs):
    return reduce(lambda x, y: x*y, objs)

@define('/', True)
def num_div(_, _1, objs):
    s = objs[0]
    for o in objs.cdr:
        s = s // o if isinstance(s, int) and isinstance(o, int) else s / o
    return s

@define('=', True)
def num_eq(_, _1, objs):
    return isinstance(objs[0], (int, float)) and \
        type(objs[0]) == type(objs[1]) and objs[0] == objs[1]

@define('!=', True)
def num_noteq(_, _1, objs):
    return not isinstance(objs[0], (int, float)) or \
        type(objs[0]) != type(objs[1]) and objs[0] != objs[1]

@define('<', True)
def num_lt(_, _1, objs):
    return isinstance(objs[0], (int, float)) and \
        isinstance(objs[1], (int, float)) and objs[0] < objs[1]

@define('>', True)
def num_gt(_, _1, objs):
    return isinstance(objs[0], (int, float)) and \
        isinstance(objs[1], (int, float)) and objs[0] > objs[1]

@define('>=', True)
def num_nlt(_, _1, objs):
    return isinstance(objs[0], (int, float)) and \
        isinstance(objs[1], (int, float)) and objs[0] >= objs[1]

@define('<=', True)
def num_ngt(_, _1, objs):
    return isinstance(objs[0], (int, float)) and \
        isinstance(objs[1], (int, float)) and objs[0] <= objs[1]

@define('remainder', True)
def num_remainder(_, _1, objs):
    return objs[0] % objs[1]

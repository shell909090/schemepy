#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2013-06-25
@author: shell.xu
'''
from schemepy import objects, interrupter
from symbol import define

# number functions
@define(u'number?', True)
def num_number(_, __, objs):
    return isinstance(objs[0], (int, long, float))

@define(u'+', True)
def num_add(_, __, objs):
    return sum(objs)

@define(u'-', True)
def num_dec(_, __, objs):
    s = objs[0]
    for o in objs.cdr:
        s -= o
    return s

@define(u'*', True)
def num_mul(_, __, objs):
    return reduce(lambda x, y: x*y, objs)

@define(u'/', True)
def num_div(_, __, objs):
    s = objs[0]
    for o in objs.cdr:
        s /= o
    return s

@define(u'=', True)
def num_eq(_, __, objs):
    return isinstance(objs[0], (int, long, float)) and \
        type(objs[0]) == type(objs[1]) and objs[0] == objs[1]

@define(u'!=', True)
def num_eq(_, __, objs):
    return not isinstance(objs[0], (int, long, float)) or \
        type(objs[0]) != type(objs[1]) and objs[0] != objs[1]

@define(u'<', True)
def num_lt(_, __, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] < objs[1]

@define(u'>', True)
def num_gt(_, __, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] > objs[1]

@define(u'>=', True)
def num_nlt(_, __, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] >= objs[1]

@define(u'<=', True)
def num_ngt(_, __, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] <= objs[1]

@define(u'remainder', True)
def num_remainder(_, __, objs):
    return objs[0] % objs[1]

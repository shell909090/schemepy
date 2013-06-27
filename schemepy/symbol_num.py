#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2013-06-25
@author: shell.xu
'''
import objects, interrupter
from symbol import define

# number functions
@define(u'number?', True)
def num_number(stack, envs, objs): return isinstance(objs[0], (int, long, float))

@define(u'+', True)
def num_add(stack, envs, objs): return sum(objs)

@define(u'-', True)
def num_dec(stack, envs, objs):
    s = objs[0]
    for o in objs.cdr: s -= o
    return s

@define(u'*', True)
def num_mul(stack, envs, objs): return reduce(lambda x, y: x*y, objs)

@define(u'/', True)
def num_div(stack, envs, objs):
    s = objs[0]
    for o in objs.cdr: s /= o
    return s

@define(u'=', True)
def num_eq(stack, envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        type(objs[0]) == type(objs[1]) and objs[0] == objs[1]

@define(u'!=', True)
def num_eq(stack, envs, objs):
    return not isinstance(objs[0], (int, long, float)) or \
        type(objs[0]) != type(objs[1]) and objs[0] != objs[1]

@define(u'<', True)
def num_lt(stack, envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] < objs[1]

@define(u'>', True)
def num_gt(stack, envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] > objs[1]

@define(u'>=', True)
def num_nlt(stack, envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] >= objs[1]

@define(u'<=', True)
def num_ngt(stack, envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] <= objs[1]

@define(u'remainder', True)
def num_remainder(stack, envs, objs):
    return objs[0] % objs[1]

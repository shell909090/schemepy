#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import objects

@objects.default_env.decorater('not', True)
def logic_not(symbols, objs):
    return not objs[0]

@objects.default_env.decorater('and', True)
def logic_and(symbols, objs):
    return objs[0] and objs[1]

@objects.default_env.decorater('or', True)
def logic_or(symbols, objs):
    return objs[0] or objs[1]

@objects.default_env.decorater('cond', False)
def logic_cond(symbols, objs):
    elsecase = None
    for o in objs:
        assert(isinstance(o, objects.OPair)), '%s format error' % o
        if isinstance(o.car, objects.OSymbol) and o.car.name == 'else':
            elsecase = o.cdr
        elif symbols.eval(o.car): return symbols.evals(o.cdr)
    if elsecase: return symbols.evals(elsecase)
    return None

@objects.default_env.decorater('if', False)
def logic_if(symbols, objs):
    if symbols.eval(objs[0]): return symbols.eval(objs[1])
    elif objs.cdr.cdr is not None: return symbols.eval(objs[2])
    else: return None

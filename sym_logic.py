#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import objects
import evals

def logic_not(symbols, objs):
    return not objs[0]
logic_not.e = True
evals.default_env.add('not', logic_not)

def logic_and(symbols, objs):
    return objs[0] and objs[1]
logic_and.e = True
evals.default_env.add('and', logic_and)

def logic_or(symbols, objs):
    return objs[0] or objs[1]
logic_or.e = True
evals.default_env.add('or', logic_or)

def logic_cond(symbols, objs):
    elsecase = None
    for o in objs:
        assert(isinstance(o, objects.OPair)), '%s format error' % o
        if isinstance(o.car, objects.OSymbol) and o.car.name == 'else':
            elsecase = o.cdr
        elif symbols.eval(o.car): return symbols.evals(o.cdr)
    if elsecase: return symbols.evals(elsecase)
    return None
logic_cond.e = False
evals.default_env.add('cond', logic_cond)

def logic_if(symbols, objs):
    if symbols.eval(objs[0]): return symbols.eval(objs[1])
    elif objs.cdr.cdr is not None: return symbols.eval(objs[2])
    else: return None
logic_if.e = False
evals.default_env.add('if', logic_if)

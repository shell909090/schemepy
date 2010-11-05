#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import objects
import evals

class Function(object):

    def __init__(self, symbols, name, params, objs):
        self.symbols, self.name = symbols.clone(), name
        self.params, self.objs = params, objs
        self.e = True

    def __call__(self, symbols, objs):
        self.symbols.down()
        pn, pv = self.params, objs
        while pn or pv:
            self.symbols.add(pn.car.name, pv.car)
            pn, pv = pn.cdr, pv.cdr
        r = self.symbols.evals(self.objs)
        self.symbols.up()
        return r

def define(symbols, objs):
    symbols.add(objs.car.car.name,
                Function(symbols, objs.car.car, objs.car.cdr, objs.cdr))
define.e = False
evals.default_env.add('define', define)

def eee(symbols, objs):
    symbols.down()
    r = symbols.evals(objs)
    symbols.up()
    return r
eee.e = False
evals.default_env.add('eee', eee)

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
    assert(isinstance(objs.car, (int, long)))
    assert(isinstance(objs.cdr.car, (int, long)))
    return objs.car == objs.cdr.car
num_eq.e = True
evals.default_env.add('=', num_eq)

def num_lt(symbols, objs):
    assert(isinstance(objs.car, (int, long)))
    assert(isinstance(objs.cdr.car, (int, long)))
    return objs.car < objs.cdr.car
num_lt.e = True
evals.default_env.add('<', num_lt)

def logic_or(symbols, objs):
    return objs.car or objs.cdr.car
logic_or.e = True
evals.default_env.add('or', logic_or)

def cond(symbols, objs):
    p, elsecase = objs, None
    while p:
        assert(isinstance(p.car, objects.OPair)), '%s format error' % p.car
        if isinstance(p.car.car, objects.OSymbol) and p.car.car.name == 'else':
            elsecase = p.car.cdr
        elif symbols.eval(p.car.car): return symbols.evals(p.car.cdr)
        p = p.cdr
    if elsecase: return symbols.evals(elsecase)
    return None
cond.e = False
evals.default_env.add('cond', cond)

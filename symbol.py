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

def logic_and(symbols, objs):
    return objs.car and objs.cdr.car
logic_and.e = True
evals.default_env.add('and', logic_and)

def logic_or(symbols, objs):
    return objs.car or objs.cdr.car
logic_or.e = True
evals.default_env.add('or', logic_or)

def logic_cond(symbols, objs):
    p, elsecase = objs, None
    while p:
        assert(isinstance(p.car, objects.OPair)), '%s format error' % p.car
        if isinstance(p.car.car, objects.OSymbol) and p.car.car.name == 'else':
            elsecase = p.car.cdr
        elif symbols.eval(p.car.car): return symbols.evals(p.car.cdr)
        p = p.cdr
    if elsecase: return symbols.evals(elsecase)
    return None
logic_cond.e = False
evals.default_env.add('cond', logic_cond)

def logic_if(symbols, objs):
    if symbols.eval(objs.car): return symbols.eval(objs.cdr.car)
    elif objs.cdr.cdr.car: return symbols.eval(objs.cdr.cdr.car)
    else: return None
logic_if.e = False
evals.default_env.add('if', logic_if)

def display(symbols, objs):
    print objs.car
display.e = True
evals.default_env.add('display', display)

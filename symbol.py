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
        self.symbols, self.name = symbols.clone(), name.name
        self.params, self.objs = params, objs
        self.e = True

    def __call__(self, symbols, objs):
        # print self.name, objs
        self.symbols.down()
        pn, pv = self.params, objs
        while pn or pv:
            if pn.car.name == '.':
                self.symbols.add(pn.cdr.car.name, pv)
                break
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

def begin(symbols, objs):
    symbols.down()
    r = symbols.evals(objs)
    symbols.up()
    return r
begin.e = False
evals.default_env.add('begin', begin)

def display(symbols, objs):
    print ' '.join(map(str, list(objs)))
display.e = True
evals.default_env.add('display', display)
evals.default_env.add('error', display)

def is_symbol(symbols, objs):
    return isinstance(objs.car, objects.OSymbol)
is_symbol.e = True
evals.default_env.add('symbol?', is_symbol)

def is_eq(symbols, objs):
    return isinstance(objs[0], objects.OSymbol) and \
        isinstance(objs[1], objects.OSymbol) and objs[0].name == objs[1].name
is_eq.e = True
evals.default_env.add('eq?', is_eq)

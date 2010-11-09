#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import objects
import evals

class Function(object):

    def __init__(self, name, symbols, params, objs):
        self.name, self.symbols = name, symbols.clone()
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
        # print self.name + ' end', r
        return r

def define(symbols, objs):
    symbols.add(objs.car.car.name,
                Function(objs.car.car.name, symbols, objs.car.cdr, objs.cdr))
evals.default_env.add('define', define, False)

def sym_lambda(symbols, objs):
    return Function('lambda function', symbols, objs.car, objs.cdr)
evals.default_env.add('lambda', sym_lambda, False)

def begin(symbols, objs):
    symbols.down()
    r = symbols.evals(objs)
    symbols.up()
    return r
evals.default_env.add('begin', begin, False)

def display(symbols, objs):
    print ' '.join(map(str, list(objs)))
evals.default_env.add('display', display, True)
evals.default_env.add('error', display, True)

def is_symbol(symbols, objs):
    return isinstance(objs.car, objects.OSymbol)
evals.default_env.add('symbol?', is_symbol, True)

def is_eq(symbols, objs):
    return isinstance(objs[0], objects.OSymbol) and \
        isinstance(objs[1], objects.OSymbol) and objs[0].name == objs[1].name
evals.default_env.add('eq?', is_eq, True)

def let(symbols, objs):
    symbols.down()
    for p in objs.car:
        assert(isinstance(p.car, objects.OSymbol))
        symbols.add(p.car.name, symbols.evals(p.cdr))
    r = symbols.evals(objs.cdr)
    symbols.up()
    return r
evals.default_env.add('let', let, False)

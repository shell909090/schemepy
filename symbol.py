#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import objects

class Function(object):

    def __init__(self, name, symbols, params, objs):
        self.name, self.symbols = name, symbols.clone()
        self.params, self.objs, self.evaled = params, objs, True

    def __call__(self, symbols, objs):
        # print self.name, objs
        self.symbols.down()
        pn, pv = self.params, objs
        while pn is not objects.nil and pv is not objects.nil:
            if pn.car.name == '.':
                self.symbols.add(pn.cdr.car.name, pv)
                break
            self.symbols.add(pn.car.name, pv.car)
            pn, pv = pn.cdr, pv.cdr
        r = self.symbols.evals(self.objs)
        self.symbols.up()
        # print self.name + ' end', r
        return r

@objects.default_env.decorater('define', False)
def define(symbols, objs):
    if isinstance(objs[0], objects.OPair):
        func = Function(objs.car.car.name, symbols, objs.car.cdr, objs.cdr)
        symbols.add(objs[0].car.name, func)
    elif isinstance(objs[0], objects.OSymbol):
        symbols.add(objs[0].name, symbols.eval(objs[1]))
    else: raise Exception('define format error')

@objects.default_env.decorater('lambda', False)
def sym_lambda(symbols, objs):
    return Function('lambda function', symbols, objs.car, objs.cdr)

@objects.default_env.decorater('begin', False)
def begin(symbols, objs):
    symbols.down()
    r = symbols.evals(objs)
    symbols.up()
    return r

@objects.default_env.decorater('display', True)
@objects.default_env.decorater('error', True)
def display(symbols, objs):
    print ' '.join(map(str, list(objs)))

@objects.default_env.decorater('symbol?', True)
def is_symbol(symbols, objs):
    return isinstance(objs.car, objects.OSymbol)

@objects.default_env.decorater('eq?', True)
def is_eq(symbols, objs):
    return isinstance(objs[0], objects.OSymbol) and \
        isinstance(objs[1], objects.OSymbol) and objs[0].name == objs[1].name

@objects.default_env.decorater('let', False)
def let(symbols, objs):
    symbols.down()
    for p in objs.car:
        assert(isinstance(p.car, objects.OSymbol))
        symbols.add(p.car.name, symbols.evals(p.cdr))
    r = symbols.evals(objs.cdr)
    symbols.up()
    return r

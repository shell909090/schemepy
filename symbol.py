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

def eee(symbols, objs):
    symbols.down()
    r = symbols.evals(objs)
    symbols.up()
    return r
eee.e = False
evals.default_env.add('eee', eee)

def display(symbols, objs):
    print objs.car
display.e = True
evals.default_env.add('display', display)

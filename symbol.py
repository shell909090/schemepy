#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''

class Symbols(object):

    def __init__(self): self.sym_stack = [{},]
    def clone(self):
        sym = Symbols()
        sym.sym_stack = self.sym_stack[:]
        return sym
    def __contain__(self, name):
        for i in reversed(self.sym_stack):
            if name in i: return True
        return False
    def __getitem__(self, name):
        for i in reversed(self.sym_stack):
            if name in i: return i[name]
        raise KeyError
    def add(self, name, value): self.sym_stack[-1][name] = value
    def down(self): self.sym_stack.append({})
    def up(self): self.sym_stack.pop()

default_symbol = Symbols()

class Function(object):

    def __init__(self, name, params, codes):
        self.name, self.params, self.codes = name, params, codes
        self.e = True

    def __call__(self, code, symbols):
        print 'function', self.name, self.codes
        print dict(zip(self.params, code))
        print symbols.sym_stack

def define(code, symbols):
    print 'define', code
    symbols.sym_stack[-2][code[0][0]] = \
        Function(code[0][0], code[0][1:], code[1:])
define.e = False
default_symbol.add('define', define)

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

    def __init__(self, name, params):
        self.name, self.params = name, params

    def __run__(self, *params):
        pass

def define(code, symbols):
    print 'define', code
    symbols.sym_stack[-2][code[0][0]] = Function(code[0][0], code[0][1:])
default_symbol.add('define', define)

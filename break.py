#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2012-12-14
@author: shell.xu
'''
import os, sys, cPickle
import parser, objects, interrupter, symbol
from os import path

src = '''
(display "abc")
(pause)
(display "resume1")
(pause)
(+ 1 2)
'''

@symbol.define('pause', True)
def sym_pause(stack, envs, objs):
    if isinstance(objs, interrupter.ResumeInfo):
        print objs.s
        return objects.nil
    raise interrupter.BreakException(objs)

def main():
    r = None
    if path.exists(sys.argv[1]):
        with open(sys.argv[1], 'rb') as fi:
            stack, r = interrupter.Stack.load(fi, symbol.builtin)
    else:
        code = objects.scompile(parser.split_code_tree(src))
        stack = interrupter.init(code, symbol.builtin)
    try: print stack.trampoline(r, coredump=sys.argv[1])
    except interrupter.BreakException, be: pass

if __name__ == '__main__': main()

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

class BreakException(StandardError): pass
class ResumeInfo(object):
    def __init__(self, s): self.s = s

@symbol.define('pause', True)
def sym_pause(stack, envs, objs):
    if isinstance(objs, ResumeInfo):
        print objs.s
        return objects.nil
    raise BreakException(objs)

def main():
    r = None
    if path.exists(sys.argv[1]):
        with open(sys.argv[1], 'rb') as fi:
            stack, r = interrupter.Stack.load(fi, symbol.builtin)
        r = ResumeInfo(r)
    else:
        code = objects.scompile(parser.split_code_tree(src))
        stack = interrupter.init(code, symbol.builtin)
    try: print stack.trampoline(r, coredump=sys.argv[1])
    except BreakException, be: pass

if __name__ == '__main__': main()

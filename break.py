#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2012-12-14
@author: shell.xu
'''
import os, sys, cPickle
import schemepy
from os import path

src = '''
(display "abc")
(pause)
(display "resume1")
(pause)
(+ 1 2)
'''

@schemepy.define('pause', True)
def sym_pause(stack, envs, objs):
    if isinstance(objs, schemepy.ResumeInfo):
        print objs.s
        return schemepy.nil
    raise schemepy.BreakException(objs)

def main():
    r = None
    if path.exists(sys.argv[1]):
        with open(sys.argv[1], 'rb') as fi:
            stack, r = schemepy.Stack.load(fi.read(), schemepy.builtin)
    else:
        code = schemepy.scompile(schemepy.split_code_tree(src))
        stack = schemepy.init(code, schemepy.builtin)
    def coredump(data):
        with open(sys.argv[1], 'wb') as fi: fi.write(data)
    try: print stack.trampoline(r, coredump=coredump)
    except schemepy.BreakException, be: pass

if __name__ == '__main__': main()

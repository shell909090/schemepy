#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import sys
import parser, objects, symbol

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f: data = f.read()
    code = objects.scompile(parser.split_code_tree(data.decode('utf-8')))
    stack = objects.Stack()
    stack.append(objects.Frame(objects.PrognStatus(code),
                               objects.Envs(builtin=symbol.builtin)))
    print stack.trampoline()

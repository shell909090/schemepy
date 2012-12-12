#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import sys
import parser, objects, runtime, symbol

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f: data = f.read()
    code_tree = parser.split_code_tree(data.decode('utf-8'))
    ast = objects.scompile(code_tree)
    print runtime.run(ast, symbol.builtin)

#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import sys
import parser
import symbol

def scheme_eval(codes, symbols):
    symbols.down()
    if symbols[codes[0]].e:
        objs = []
        for code in codes:
            if isinstance(code, list):
                objs.append(scheme_eval(code, symbols))
            else: objs.append(code)
        r = symbols[objs[0]](objs[1:], symbols)
    else: r = symbols[codes[0]](codes[1:], symbols)
    symbols.up()
    return r

if __name__ == '__main__':
    f = open(sys.argv[1], 'r')
    data = f.read()
    f.close()
    sym = symbol.default_symbol.clone()
    for block in parser.split_code_tree(data.decode('utf-8')):
        print scheme_eval(block, sym)
    print sym.sym_stack

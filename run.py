#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import sys
import parser
import objects
import evals
import symbol
import sym_list
import sym_logic
import sym_num

if __name__ == '__main__':
    f = open(sys.argv[1], 'r')
    data = f.read()
    f.close()
    code_tree = parser.split_code_tree(data.decode('utf-8'))
    obj_tree = objects.make_scheme(code_tree)
    run_objs = objects.OPair(objects.OSymbol('begin'), obj_tree)
    print evals.default_env.eval(run_objs)

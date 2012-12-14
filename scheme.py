#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import sys, getopt
import parser, objects, symbol

def main():
    optlist, argv = getopt.getopt(sys.argv[1:], 'hprs:')
    optdict = dict(optlist)
    if '-h' in optdict:
        print main.__doc__
        return
    if '-p' in optdict:
        with open(argv[0], 'r') as f: data = f.read()
        code = parser.split_code_tree(data.decode('utf-8'))
        __import__('pprint').pprint(code)
        return
    if '-r' not in optdict: 
        with open(sys.argv[1], 'r') as f: data = f.read()
        code = objects.scompile(parser.split_code_tree(data.decode('utf-8')))
    else: code = marshal.load(argv[0])
    if '-s' in optdict:
        marshal.dump(optdict['-s'])
        return
    stack = objects.Stack()
    stack.append(objects.Frame(objects.PrognStatus(code),
                               objects.Envs(builtin=symbol.builtin)))
    print stack.trampoline()

if __name__ == '__main__': main()

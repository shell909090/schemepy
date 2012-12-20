#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import sys, cmd, getopt, cPickle
import parser, objects, interrupter, symbol, debug
from os import path

def print_src(filename):
    with open(filename, 'r') as f: data = f.read()
    code = parser.split_code_tree(data.decode('utf-8'))
    __import__('pprint').pprint(code)

def compile_src(filename):
    with open(filename, 'r') as f: data = f.read()
    code = interrupter.scompile(parser.split_code_tree(data.decode('utf-8')))
    with open(path.splitext(filename)[0]+'.scc', 'wb') as fo:
        cPickle.dump(code, fo, 2)

def indent_src(filename, stream):
    with open(filename, 'r') as f: data = f.read()
    code = interrupter.scompile(parser.split_code_tree(data.decode('utf-8')))
    for i in code: stream.write(str(i)+'\n')

class REPL(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '> '
        self.env = interrupter.Envs(objects.to_list([{}, symbol.builtin,]))

    def do_quit(self, line):
        ''' quit system '''
        print 'quit'
        sys.exit(-1)
    do_EOF = do_quit

    def default(self, line):
        code = interrupter.scompile(parser.split_code_tree(line))
        stack = interrupter.Stack()
        stack.append((interrupter.PrognStatus(code), self.env))
        print stack.trampoline()

def main():
    optlist, argv = getopt.getopt(sys.argv[1:], 'cdhiprt')
    optdict = dict(optlist)
    if '-h' in optdict:
        print main.__doc__
        return
    if '-c' in optdict: return compile_src(argv[0])
    if '-p' in optdict: return print_src(argv[0])
    if '-i' in optdict: return indent_src(argv[0], sys.stdout)

    if len(argv) == 0: return REPL().cmdloop()

    if path.splitext(argv[0])[1] == '.scc':
        with open(argv[0], 'rb') as fi: code = cPickle.load(fi)
    else:
        with open(argv[0], 'r') as f: data = f.read()
        code = interrupter.scompile(parser.split_code_tree(data.decode('utf-8')))
    stack = interrupter.init(code, symbol.builtin)
    dbg = debug.Debuger() if '-d' in optdict else None
    print stack.trampoline(
        debug=dbg, coredump=path.splitext(argv[0])[0]+'.cdp')

if __name__ == '__main__': main()

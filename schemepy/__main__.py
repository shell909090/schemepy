#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import sys, cmd, getopt, cPickle
import schemepy
from os import path

def print_src(filename):
    with open(filename, 'r') as f: data = f.read()
    code = schemepy.split_code_tree(data.decode('utf-8'))
    __import__('pprint').pprint(code)

def compile_src(filename):
    with open(filename, 'r') as f: data = f.read()
    for i in xrange(100):
        code = schemepy.scompile(schemepy.split_code_tree(data.decode('utf-8')))
    __import__('pprint').pprint(code)
    # with open(path.splitext(filename)[0]+'.scc', 'wb') as fo:
    #     cPickle.dump(code, fo, 2)

def indent_src(filename, stream):
    with open(filename, 'r') as f: data = f.read()
    code = schemepy.scompile(schemepy.split_code_tree(data.decode('utf-8')))
    for i in code: stream.write(unicode(i)+u'\n')

class REPL(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = u'> '
        self.env = schemepy.Envs(schemepy.to_list([{}, schemepy.builtin,]))

    def do_quit(self, line):
        ''' quit system '''
        print u'quit'
        sys.exit(-1)
    do_EOF = do_quit

    def default(self, line):
        code = schemepy.scompile(schemepy.split_code_tree(line))
        stack = schemepy.Stack()
        stack.append((schemepy.PrognStatus(code), self.env))
        print stack.trampoline()

def main():
    '''
    -c: compile file
    -d: debug mode
    -h: help
    -i: indent file
    -n: no coredump
    -p: print source file after parse

    cdp: coredump file
    scc: scheme compiled
    '''
    optlist, argv = getopt.getopt(sys.argv[1:], 'cdhinp')
    optdict = dict(optlist)
    if '-h' in optdict:
        print main.__doc__
        return
    if '-c' in optdict: return compile_src(argv[0])
    if '-p' in optdict: return print_src(argv[0])
    if '-i' in optdict: return indent_src(argv[0], sys.stdout)

    if len(argv) == 0: return REPL().cmdloop()
    fname, extname = path.splitext(argv[0])

    if extname == '.cdp':
        with open(argv[0], 'rb') as fi:
            stack, r = schemepy.Stack.load(fi.read(), symbol.builtin)
    elif extname == '.scc':
        with open(argv[0], 'rb') as fi: code = cPickle.load(fi)
        stack = schemepy.init(code, symbol.builtin)
    else:
        with open(argv[0], 'r') as f: data = f.read()
        code = schemepy.scompile(schemepy.split_code_tree(data.decode('utf-8')))
        stack = schemepy.init(code, schemepy.builtin)
    dbg = schemepy.Debuger() if '-d' in optdict else None
    def coredump(data):
        with open(fname+'.cdp', 'wb') as fo: fo.write(data)
    if '-n' in optdict: coredump = None
    print stack.trampoline(debug=dbg, coredump=coredump)

if __name__ == '__main__': main()

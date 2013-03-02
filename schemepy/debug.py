#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2012-12-15
@author: shell.xu
'''
import sys, cmd, pdb
import objects, interrupter

def print_step(stack, r):
    print u'result:', r
    for i in stack: print i[0]

# TODO: breakpoint, cond breakpoint, clear, exec
class Debuger(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.step, self.next, self.callstop = True, None, None

    def default(self, line): print u'unknown command'
    def do_quit(self, line):
        ''' quit system '''
        print u'quit'
        sys.exit(-1)
    do_EOF = do_quit
    def do_python(self, line): pdb.set_trace()

    def do_stack(self, line):
        ''' print full stack '''
        for i in self.stack: print i[0]
    def do_result(self, line):
        ''' print step result '''
        print u'result:', self.r

    def do_all(self, line):
        ''' print all variable '''
        for k, v in self.stack[-1][1].fast.iteritems():
            print k, v
    def do_var(self, line):
        ''' print variables in this environment '''
        for k, v in self.stack[-1][1].e[0].iteritems():
            print k, v
    do_v = do_var
    def do_print(self, line):
        ''' print value of a name '''
        print self.stack[-1][1][line.strip()]
    # TODO: auto-complete?
    do_p = do_print

    def do_up(self, line):
        ''' stop when return to up stack '''
        self.step, self.next, self.callstop = None, len(self.stack)-1, None
        return True
    def do_down(self, line):
        ''' stop when stack down '''
        self.step, self.next, self.callstop = None, len(self.stack)+1, None
        return True
    def do_call(self, line):
        ''' stop when call '''
        self.step, self.next, self.callstop = None, None, True
        return True
    do_c = do_call
    def do_next(self, line):
        ''' stop when back to this stack '''
        self.step, self.next, self.callstop = None, len(self.stack), None
        return True
    do_n = do_next
    def do_step(self, line):
        ''' stop next step '''
        self.step, self.next, self.callstop = True, None, None
        return True
    do_s = do_step
    def do_continue(self, line):
        ''' run '''
        self.step, self.next, self.callstop = None, None, None
        return True
    do_cont = do_continue

    def __call__(self, stack, r):
        if not (self.callstop and isinstance(stack[-1][0], interrupter.OFunction))\
                and not self.step and \
                not (self.next and len(stack) == self.next): return
        self.prompt = u'%d > ' % len(stack)
        self.stack, self.r = stack, r
        print u'result:', self.r
        print stack[-1][0]
        self.cmdloop()

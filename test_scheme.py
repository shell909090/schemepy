#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import sys, types, unittest
import schemepy

def run_scheme(filepath):
    with open(filepath, 'r') as f: data = f.read()
    code = schemepy.scompile(schemepy.split_code_tree(data.decode('utf-8')))
    stack = schemepy.init(code, schemepy.builtin)
    return stack.trampoline()

class TestScheme(unittest.TestCase):

    def test_change_money(self):
        self.assertEqual(run_scheme('code/change-money.scm'), 9)

    def test_change_money_list(self):
        self.assertEqual(run_scheme('code/change-money-list.scm'), 9)

    def test_church(self):
        self.assertEqual(run_scheme('code/church.scm'), 2)

    def test_last_pair(self):
        self.assertEqual(run_scheme('code/last-pair.scm'), 5)

    def test_mobile(self):
        self.assertEqual(run_scheme('code/mobile.scm'), True)

    def test_reverse_tree(self):
        li = list(run_scheme('code/reverse-tree.scm'))
        self.assertEqual(list(li[0]), [4, 3])
        self.assertEqual(list(li[1]), [2, 1])

    def test_reverse(self):
        self.assertEqual(list(run_scheme('code/reverse.scm')),
                         [10, 9, 8, 7, 6, 5, 4, 3, 2, 1])

    def test_same_partiy(self):
        self.assertEqual(list(run_scheme('code/same-partiy.scm')), [3, 5, 7])

    def test_subset(self):
        subset = str(run_scheme('code/subset.scm'))
        self.assertEqual(subset,
                         '(() (3) (2) (2 3) (1) (1 3) (1 2) (1 2 3))')

def unfold_code(code):
    l = []
    for i in code:
        if not isinstance(i, tuple):
            l.append(unfold_code(i))
        else: l.append(i[0])
    return l

class TestParser(unittest.TestCase):

    def test_code_tree(self):
        with open('code/same-partiy.scm', 'r') as f: data = f.read()
        code = schemepy.split_code_tree(data.decode('utf-8'))
        self.assertEqual(
            unfold_code(code),
            [[u'define', [u'same-partiy', u'a', u'.', u'l'], [u'define', [u'same-even', u'a', u'l'], [u'cond', [[u'null?', u'l'], u"'", []], [[u'=', u'a', [u'remainder', [u'car', u'l'], u'2']], [u'cons', [u'car', u'l'], [u'same-even', u'a', [u'cdr', u'l']]]], [u'else', [u'same-even', u'a', [u'cdr', u'l']]]]], [u'same-even', [u'remainder', u'a', u'2'], u'l']], [u'same-partiy', u'1', u'3', u'4', u'5', u'6', u'7']])

    def test_compiled_code(self):
        with open('code/same-partiy.scm', 'r') as f: data = f.read()
        code = schemepy.scompile(schemepy.split_code_tree(data.decode('utf-8')))
        self.assertEqual(
            str(code),
            '''((define (same-partiy a . l)
  (define (same-even a l)
    (cond
      ((null? l) '())
      ((= a (remainder (car l) 2))
        (cons (car l) (same-even a (cdr l))))
      (else (same-even a (cdr l))))
  (same-even (remainder a 2) l)
  (same-partiy 1 3 4 5 6 7))''')

@schemepy.define('pause', True)
def sym_pause(stack, envs, objs):
    if isinstance(objs, schemepy.ResumeInfo):
        return schemepy.nil
    raise schemepy.BreakException(objs)

class TestBreak(unittest.TestCase):

    src = u'''
(pause "abc")
(pause "resume1")
(+ 1 2)
'''

    def test_break(self):
        builtin_ = schemepy.builtin.copy()
        sym_pause.evaled = True
        builtin_['pause'] = sym_pause

        r = None
        code = schemepy.scompile(schemepy.split_code_tree(self.src))
        stack = schemepy.init(code, builtin_)

        breakcode = []
        with self.assertRaises(schemepy.BreakException) as be:
            stack.trampoline(r, coredump=breakcode.append)
        self.assertEqual(be.exception.args[0][0], 'abc')

        stack, r = schemepy.Stack.load(''.join(breakcode), builtin_)
        breakcode = []
        with self.assertRaises(schemepy.BreakException) as be:
            stack.trampoline(r, coredump=breakcode.append)
        self.assertEqual(be.exception.args[0][0], 'resume1')

        stack, r = schemepy.Stack.load(''.join(breakcode), builtin_)
        breakcode = []
        r = stack.trampoline(r, coredump=breakcode.append)
        self.assertEqual(r, 3)

if __name__ == '__main__': unittest.main()

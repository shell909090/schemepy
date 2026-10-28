#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import sys, types, unittest
import schemepy

def run_scheme(filepath):
    with open(filepath, 'r') as f: data = f.read()
    code = schemepy.scompile(schemepy.split_code_tree(data))
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
        code = schemepy.split_code_tree(data)
        self.assertEqual(
            unfold_code(code),
            [['define', ['same-partiy', 'a', '.', 'l'],
              ['define', ['same-even', 'a', 'l'],
               ['cond',
                [['null?', 'l'], "'", []],
                [['=', 'a', ['remainder', ['car', 'l'], '2']],
                 ['cons', ['car', 'l'], ['same-even', 'a', ['cdr', 'l']]]],
                ['else', ['same-even', 'a', ['cdr', 'l']]]]],
              ['same-even', ['remainder', 'a', '2'], 'l']],
             ['same-partiy', '1', '3', '4', '5', '6', '7']])

    def test_compiled_code(self):
        with open('code/same-partiy.scm', 'r') as f: data = f.read()
        code = schemepy.scompile(schemepy.split_code_tree(data))
        self.assertEqual(
            str(code),
            '''((define (same-partiy a . l)
  (define (same-even a l)
    (cond
      ((null? l) '())
      ((= a (remainder (car l) 2))
        (cons (car l) (same-even a (cdr l))))
      (else (same-even a (cdr l)))))
  (same-even (remainder a 2) l))
  (same-partiy 1 3 4 5 6 7))''')

@schemepy.define('pause', True)
def sym_pause(stack, envs, objs):
    if isinstance(objs, schemepy.ResumeInfo):
        return schemepy.nil
    raise schemepy.BreakException(objs)

class TestBreak(unittest.TestCase):

    src = '''
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

        stack, r = schemepy.Stack.load(b''.join(breakcode), builtin_)
        breakcode = []
        with self.assertRaises(schemepy.BreakException) as be:
            stack.trampoline(r, coredump=breakcode.append)
        self.assertEqual(be.exception.args[0][0], 'resume1')

        stack, r = schemepy.Stack.load(b''.join(breakcode), builtin_)
        breakcode = []
        r = stack.trampoline(r, coredump=breakcode.append)
        self.assertEqual(r, 3)

class TestMigration(unittest.TestCase):
    def evaluate(self, source):
        return schemepy.init(schemepy.scompile(schemepy.split_code_tree(source)), schemepy.builtin).trampoline()

    def test_division(self):
        self.assertEqual(self.evaluate('(/ 7 2)'), 3)
        self.assertEqual(self.evaluate('(/ -7 2)'), -4)
        self.assertEqual(self.evaluate('(/ 7.0 2)'), 3.5)

    def test_apply_order(self):
        self.assertEqual(self.evaluate("(apply - '(10 3 2))"), 5)

    def test_queens(self):
        from pathlib import Path
        source = Path('code/queens.scm').read_text().replace('(display (queens 8))', '').replace('(newline)', '')
        solutions = list(self.evaluate(source + '\n(queens 8)'))
        self.assertEqual(len(solutions), 92)
        seen = set()
        for solution in solutions:
            pairs = [(p.car, p.cdr) for p in solution]
            self.assertEqual(len(pairs), 8)
            for values in ([x for x,y in pairs], [y for x,y in pairs],
                           [x+y for x,y in pairs], [x-y for x,y in pairs]):
                self.assertEqual(len(set(values)), 8)
            seen.add(tuple(pairs))
        self.assertEqual(len(seen), 92)

    def test_compiled_cli(self):
        import subprocess
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / '中文.scm'
            source.write_text('(display "你好") (+ 1 2)', encoding='utf-8')
            def run(*args):
                return subprocess.check_output([sys.executable, '-m', 'schemepy', *map(str,args)], text=True)
            run('-c', source)
            self.assertEqual(run(source), run(source.with_suffix('.scc')))
            self.assertEqual(run(source), '你好\n3\n')

if __name__ == '__main__': unittest.main()

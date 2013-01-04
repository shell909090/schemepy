#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import sys, unittest
import schemepy

def run_scheme(filepath):
    with open(filepath, 'r') as f: data = f.read()
    code = schemepy.scompile(schemepy.split_code_tree(data.decode('utf-8')))
    stack = schemepy.init(code, schemepy.builtin)
    return stack.trampoline()

class TestScheme(unittest.TestCase):

    def test_change_money(self):
        self.assertEqual(run_scheme('test/change-money.scm'), 9)

    def test_change_money_list(self):
        self.assertEqual(run_scheme('test/change-money-list.scm'), 9)

    def test_church(self):
        self.assertEqual(run_scheme('test/church.scm'), 2)

    def test_last_pair(self):
        self.assertEqual(run_scheme('test/last-pair.scm'), 5)

    def test_mobile(self):
        self.assertEqual(run_scheme('test/mobile.scm'), True)

    def test_reverse_tree(self):
        li = list(run_scheme('test/reverse-tree.scm'))
        self.assertEqual(list(li[0]), [4, 3])
        self.assertEqual(list(li[1]), [2, 1])

    def test_reverse(self):
        self.assertEqual(list(run_scheme('test/reverse.scm')),
                         [10, 9, 8, 7, 6, 5, 4, 3, 2, 1])

    def test_same_partiy(self):
        self.assertEqual(list(run_scheme('test/same-partiy.scm')), [3, 5, 7])

    def test_subset(self):
        subset = str(run_scheme('test/subset.scm'))
        self.assertEqual(subset,
                         '(() (3) (2) (2 3) (1) (1 3) (1 2) (1 2 3))')

if __name__ == '__main__': unittest.main()

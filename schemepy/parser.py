#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import re

split_code_re = re.compile('([() \n\r\t])')
string_cutter_re = re.compile('(".*?(?<!\\\\)"|;.*?\n)', re.S)
replace_tab = [(u'\\t', u'\t'), (u'\\n', u'\n'), (u'\\', u'')]
def split_code(code):
    for s in string_cutter_re.split(code):
        if not s: continue
        if s[0] == ';': yield s.strip()
        elif s[0] == '"':
            if s[-1] != '"': raise Exception('string not closed: %s' % s)
            for k, v in replace_tab: s = s.replace(k, v)
            yield s
        else:
            for c in split_code_re.split(s):
                if c and c not in ' \t\n\r': yield c

symbol_pairs = {u'(': u')',}
def build_block(chunks, igcmt, term=None):
    l = []
    for c in chunks:
        if igcmt and c.startswith(u';'): continue
        elif term and c == term: return
        elif c in symbol_pairs:
            yield list(build_block(chunks, igcmt, symbol_pairs[c]))
            continue
        if c[0] == "'":
            yield "'"
            c = c[1:]
        if c: yield c
    if term: raise Exception('symbol %s dismatch' % term)

def split_code_tree(code, igcmt=True):
    return list(build_block(split_code(code), igcmt))

#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import re

split_code_re = re.compile("([()' \n\r\t])")
string_cutter_re = re.compile('(".*?(?<!\\\\)"|;.*?\n)', re.S)
replace_tab = [(u'\\t', u'\t'), (u'\\n', u'\n'), (u'\\', u'')]
def split_code(code):
    line = 1
    for s in string_cutter_re.split(code):
        if not s: continue
        if s[0] == ';': yield s.strip(), line
        elif s[0] == '"':
            n = s.count('\n')
            for k, v in replace_tab: s = s.replace(k, v)
            yield s, line
            line += n
        else:
            for c in split_code_re.split(s):
                if not c: continue
                if c == '\n': line += 1
                elif c not in ' \t\n\r': yield c, line

symbol_pairs = {u'(': u')',}
def build_block(chunks, igcmt, term=True):
    for c, line in chunks:
        if igcmt and c.startswith(u';'): continue
        elif term and c == ')': return
        elif c == '(':
            yield build_block(chunks, igcmt)
            continue
        if c: yield c, line
    if term: raise Exception('parenthesis not close')

def split_code_tree(code, igcmt=True):
    assert type(code) == unicode, 'input not unicode'
    return build_block(split_code(code), igcmt, False)

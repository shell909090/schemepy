#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''

replace_tab = [('\\t', '\t'), ('\\n', '\n'), ('\\', '')]
def find_quote_end(code, start):
    idx = start
    while True:
        idx = code.find(u'"', idx+1)
        if code[idx-1] != u'\\':
            code = code[start:idx+1]
            for k, v in replace_tab: code = code.replace(k, v)
            return code, idx
    raise Exception()

def find_str(s, start, charset):
    for i, c in enumerate(s[start:]):
        if c in charset: return i+start
    return -1

control_code = '()\'";'
def split_code(code):
    start = 0
    while start < len(code):
        idx = find_str(code, start, control_code)
        if idx == -1: break
        if code[start:idx]:
            for c in code[start: idx].split(): yield c
        if code[idx] == '"':
            c, idx = find_quote_end(code, idx)
            yield c
        elif code[idx] == ';':
            idxend = code.find('\n', idx)
            if idxend == -1: idxend = len(code)
            yield code[idx:idxend]
            idx = idxend
        else: yield code[idx]
        start = idx+1

symbol_pairs = {'(':')',}
def build_block(chunks, igcmt, header = None):
    l = []
    for c in chunks:
        if igcmt and c.startswith(';'): continue
        elif c in symbol_pairs: l.append(build_block(chunks, igcmt, c))
        elif header and c == symbol_pairs[header]: return l
        else: l.append(c)
    if header: raise Exception('symbol %s dismatch' % header)
    return l

def split_code_tree(code, igcmt=True):
    return build_block(split_code(code), igcmt)

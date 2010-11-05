#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import sys

def find_quote_end(code, start):
    start += 1
    idx, codelist = start, [u'"']
    while idx < len(code):
        if code[idx] == u'\\':
            codelist.append(code[start:idx+1])
            idx += 2
            start = idx
        elif code[idx] == u'"':
            codelist.append(code[start:idx])
            return ''.join(codelist), idx
        else: idx += 1
    raise Exception()

control_code = '()\'";'
def split_code(code):
    start = 0
    while start < len(code):
        idxes = map(lambda c: code.find(c, start), control_code)
        idxes = filter(lambda i: i != -1, idxes)
        if not idxes: break
        idx = min(idxes)
        if code[start: idx]:
            for c in code[start: idx].split(): yield c
        if code[idx] == '"':
            c, idx = find_quote_end(code, idx)
            yield c
        elif code[idx] == ';': idx = code.find('\n', idx)
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

def split_code_tree(code, igcmt = True):
    chunks = split_code(code)
    return build_block(chunks, igcmt)

def show_level(code, lv):
    if isinstance(code, (tuple, list)) and \
            len(filter(lambda x: isinstance(x, (tuple, list)), code)):
        for c in code: show_level(c, lv + 1)
    else: print '  ' * lv, code

if __name__ == '__main__':
    f = open(sys.argv[1], 'r')
    data = f.read()
    f.close()
    code_tree = split_code_tree(data.decode('utf-8'))
    show_level(code_tree, 0)
    # print code_tree


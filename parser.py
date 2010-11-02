#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import sys

def find_line_comment_end(code):
    if code.find('\n') == -1: raise LookupError()
    info = code.partition('\n')
    return info[0] + info[1], info[2]

def find_quote_end(code):
    idx, codelist = 1, [u'"']
    while idx < len(code):
        if code[idx] == u'\\':
            codelist.append(code[idx+1])
            idx += 2
        elif code[idx] == u'"':
            codelist.append(code[idx])
            return ''.join(codelist), code[idx+1:]
        else:
            codelist.append(code[idx])
            idx += 1
    raise Exception()

match_pair = {';':find_line_comment_end, '"':find_quote_end}
def split_match(code):
    for k, v in match_pair.items():
        if code.startswith(k): return v(code)
    return None, code

symbol_blank = ' \r\n'
symbol1 = '()[]{};,'
symbol2 = ['++']
def split_header(code):
    if code[0] in symbol_blank: return code[0], code[1:]
    if code[:2] in symbol2: return code[:2], code[2:]
    return code[:1], code[1:]

def split_code(code):
    chunk = ''
    while code:
        # print code
        c, code = split_match(code)
        if c:
            if chunk: yield chunk
            chunk = ''
            yield c
            continue
        c, code = split_header(code)
        if c in symbol_blank:
            if chunk: yield chunk
            chunk = ''
            continue
        elif c in symbol1 or c in symbol2:
            if chunk: yield chunk
            chunk = ''
            yield c
        else: chunk += c
    if chunk: yield chunk

symbol_pairs = {'(':')', '[':']', '{':'}'}
def build_block(chunks, igcmt, header = None):
    l = []
    for c in chunks:
        if igcmt and c.startswith(';'): continue
        if c in symbol_pairs: l.append(build_block(chunks, igcmt, c))
        else:
            if header and c == symbol_pairs[header]: return l
            l.append(c)
    if header: raise Exception('symbol %s dismatch' % header)
    return l

def split_code_tree(code, igcmt = True):
    chunks = split_code(code)
    return build_block(chunks, igcmt)

if __name__ == '__main__':
    f = open(sys.argv[1], 'r')
    data = f.read()
    f.close()
    print split_code_tree(data.decode('utf-8'))

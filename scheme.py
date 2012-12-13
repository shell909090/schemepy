#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import sys
import runtime, symbol

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f: data = f.read()
    print runtime.run(data.decode('utf-8'), symbol.builtin)

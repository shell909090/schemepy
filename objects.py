#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''

class OPair(object):
    def __init__(self, car = None, cdr = None):
        self.car, self.cdr = car, cdr
    def __repr__(self):
        if isinstance(self.cdr, OPair): return list_tostr(self)
        elif self.cdr is None: return '(%s)' % self.car
        else: return '(%s . %s)' % (self.car, self.cdr)

class OSymbol(object):
    def __init__(self, name): self.name = name
    def __repr__(self): return "`" + self.name

class OString(object):
    def __init__(self, v): self.str = v[1:-1]
    def __repr__(self): return '"%s"' % self.str

class OQuota(object):
    def __init__(self): self.objs = None
    def __repr__(self): return "'" + str(self.objs)

def make_scheme(obj):
    ''' make python objects to scheme objects '''
    if isinstance(obj, (int, long, float)): return obj
    elif isinstance(obj, (list, tuple)): return make_list(obj)
    elif isinstance(obj, (unicode, str)): return make_str(obj)

def make_list(li):
    ''' make python list to scheme list '''
    if not li: return None
    p = None
    for i in reversed(li):
        p = OPair(make_scheme(i), p)
        if isinstance(p.car, OQuota):
            p.car.objs = p.cdr.car
            p.cdr = p.cdr.cdr
    return p

number_str = '1234567890'
def make_str(obj):
    if isinstance(obj, str): obj = obj.decode('utf-8')
    if obj[0] == '#':
        if obj[1] == 't': return True
        elif obj[1] == 'f': return False
        else: raise Exception('boolean name error')
    elif obj[0] == '"': return OString(obj)
    elif obj[0] == "'": return OQuota()
    elif obj[0] in number_str:
        if '.' in obj: return float(obj)
        else: return int(obj)
    else: return OSymbol(obj)

def list_tostr(li):
    ''' translate scheme list to str '''
    p, buf = li, []
    while p:
        buf.append(str(p.car))
        p = p.cdr
    return '(' + ' '.join(buf) + ')'

if __name__ == '__main__':
    print make_scheme(['define', ['abc', '1'], ['display', '"abc"']])

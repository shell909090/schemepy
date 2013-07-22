#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import re

__all__ = ['SchemeObject', 'ONil', 'nil', 'OCons', 'to_list', 'reversed_list',
           'OSymbol', 'OQuote', 'scompile', 'format_list', 'format_obj']

FORMAT_WIDTH = 60
class SchemeObject(object):
    def __repr__(self):
        return format_obj(self)

class ONil(SchemeObject):
    def __new__(cls, *p, **kw):
        if not hasattr(cls, 'nil'):
            cls.nil = object.__new__(cls, *p, **kw)
        return cls.nil

    def __setstate__(self, _):
        return nil

    def __iter__(self):
        if False:
            yield

nil = ONil()

class OCons(SchemeObject):
    def __init__(self, car=nil, cdr=nil):
        self.car, self.cdr = car, cdr

    def get(self, k, d=None):
        p = self
        while k > 0 and p is not nil:
            p, k = p.cdr, k-1
        return d if p is nil else p.car

    def __getitem__(self, k):
        p = self
        while k > 0 and p is not nil:
            p, k = p.cdr, k-1
        if p is nil:
            raise IndexError()
        return p.car

    def __setitem__(self, k, v):
        p = self
        while k > 0 and p is not nil:
            p, k = p.cdr, k-1
        if p is nil:
            raise IndexError()
        p.car = v

    def __iter__(self):
        p = self
        while p is not nil:
            yield p.car
            p = p.cdr

def to_list(li):
    ''' make python list to scheme list '''
    p = nil
    for i in reversed(li):
        p = OCons(i, p)
    return p

def reversed_list(li):
    p = nil
    while li is not nil:
        p, li = OCons(li.car, p), li.cdr
    return p

class OSymbol(SchemeObject):
    cache = {}

    def __init__(self, name):
        self.name = name

    def __getnewargs__(self):
        return (self.name,)

    def __new__(cls, name):
        o = cls.cache.get(name)
        if o is not None:
            return o
        o = object.__new__(cls)
        cls.cache[name] = o
        return o

class OQuote(SchemeObject):
    def __init__(self):
        self.objs = None

is_num_re = re.compile('-?[0-9\.]+')
def scompile(obj):
    if not isinstance(obj, tuple):
        l = map(scompile, obj)
        for i, o in enumerate(l):
            if isinstance(o, OQuote):
                o.objs = l.pop(i+1)
        return to_list(l)
    obj, line = obj
    if isinstance(obj, str):
        obj = obj.decode('utf-8')
    if obj[0] == u'#':
        r = {u't': True, u'f': False}.get(obj[1:])
        assert r is not None, 'boolean name error: %s' % obj
        return r
    elif obj[0] == u'"':
        assert obj[-1] == '"', 'quote not close in line %d' % line
        return obj[1:-1]
    elif obj == u"'":
        return OQuote()
    elif is_num_re.match(obj):
        if obj == u'.':
            return OSymbol(obj)
        if u'.' in obj:
            return float(obj)
        return int(obj)
    else:
        return OSymbol(obj)

def format_list(o, lv=0):
    if o.cdr is nil:
        return u'(%s)' % format_obj(o.car)
    elif not isinstance(o.cdr, OCons):
        return u'(%s . %s)' % (format_obj(o.car), format_obj(o.cdr))
    if isinstance(o[0], OSymbol) and o[0].name == u'define':
        s = u'(%s %s\n' % (format_obj(o[0], lv), format_obj(o[1], lv))
        for i in o.cdr.cdr:
            s += '  ' * (lv+1) + format_obj(i, lv+1) + '\n'
        return s[:-1] + u')'
    s = u'(%s)' % ' '.join(format_obj(i, lv) for i in o)
    if (2*lv + len(s)) < FORMAT_WIDTH:
        return s
    s = u'(%s\n' % format_obj(o[0], lv)
    for i in o.cdr:
        s += '  ' * (lv+1) + format_obj(i, lv+1) + u'\n'
    return s[:-1]+u')'

def format_obj(o, lv=0):
    return {
        bool: {True: u'#t', False: u'#f'}.get,
        str: lambda o: u'"%s"' % str(o),
        unicode: lambda o: '"%s"' % unicode(o),
        ONil: lambda o: u'()',
        OSymbol: lambda o: o.name,
        OQuote: lambda o: u"'" + format_obj(o.objs),
        OCons: lambda o: format_list(o, lv),
    }.get(o.__class__, str)(o)

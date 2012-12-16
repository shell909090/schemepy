#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''

FUNC_DEBUG = False
FORMAT_WIDTH=60

class SchemeObject(object): pass

class ONil(SchemeObject):
    def __new__(cls, *p, **kw):
        if not hasattr(cls, 'nil'): cls.nil = object.__new__(cls, *p, **kw)
        return cls.nil
    def __setstate__(self, state): return nil
    def __iter__(self):
        if False: yield
nil = ONil()

class OPair(SchemeObject):
    def __init__(self, car=nil, cdr=nil):
        self.car, self.cdr = car, cdr
    def get(self, k, d=None):
        p = self
        while k > 0 and p is not nil: p, k = p.cdr, k-1
        return d if p is nil else p.car
    def __getitem__(self, k):
        p = self
        while k > 0 and p is not nil: p, k = p.cdr, k-1
        if p is nil: raise IndexError()
        return p.car
    def __iter__(self):
        p = self
        while p is not nil:
            yield p.car
            p = p.cdr
    def __call__(self, stack, envs, objs):
        raise Exception('this should never happen')

def to_list(li):
    ''' make python list to scheme list '''
    p = nil
    for i in reversed(li): p = OPair(i, p)
    return p

def reversed_list(li):
    p = nil
    while li is not nil: p, li = OPair(li.car, p), li.cdr
    return p

class OSymbol(SchemeObject):
    def __init__(self, name): self.name = name

class OQuota(SchemeObject):
    def __init__(self): self.objs = None

class OFunction(SchemeObject):
    def __init__(self, name, envs, params, objs):
        self.name, self.envs = name, envs
        self.params, self.objs, self.evaled = params, objs, True
    def __repr__(self): return '<function %s>' % self.name

    def __call__(self, stack, envs, objs):
        r, pn, pv = {}, self.params, objs
        while pn is not nil and pv is not nil:
            if pn[0].name == '.':
                r[pn[1].name] = pv
                break
            r[pn[0].name] = pv[0]
            pn, pv = pn.cdr, pv.cdr
        newenv = self.envs.fork(r)
        if FUNC_DEBUG: print 'call', self.name, newenv.stack[-1]
        return stack.jump(PrognStatus(self.objs), newenv)

def scompile(obj):
    if isinstance(obj, (int, long, float)): return obj
    elif isinstance(obj, (list, tuple)):
        l = map(scompile, obj)
        for i, o in enumerate(l):
            if isinstance(o, OQuota): o.objs = l.pop(i+1)
        return to_list(l)
    elif isinstance(obj, (unicode, str)):
        if isinstance(obj, str): obj = obj.decode('utf-8')
        if obj[0] == '#':
            if obj[1] == 't': return True
            elif obj[1] == 'f': return False
            else: raise Exception('boolean name error')
        elif obj[0] == '"': return obj[1:-1]
        elif obj[0] == "'": return OQuota()
        elif obj[0].isdigit() or (\
            obj[0] == '-' and len(obj) > 1 and obj[1].isdigit()):
            if '.' in obj: return float(obj)
            return int(obj)
        else: return OSymbol(obj)

def format_list(o, lv=0):
    if o.cdr is nil: return '(%s)' % format(o.car)
    elif not isinstance(o.cdr, OPair):
        return '(%s . %s)' % (format(o.car), format(o.cdr))
    if isinstance(o[0], OSymbol) and o[0].name == 'define':
        s = '(%s %s\n' % (format(o[0], lv), format(o[1], lv))
        for i in o.cdr.cdr: s += '  ' * (lv+1) + format(i, lv+1) + '\n'
        return s[:-1]
    s = '(%s)' % ' '.join(map(lambda o: format(o, lv), o))
    if (2*lv + len(s)) < FORMAT_WIDTH: return s
    s = '(%s\n' % format(o[0], lv)
    for i in o.cdr: s += '  ' * (lv+1) + format(i, lv+1) + '\n'
    return s[:-1]

def format(o, lv=0):
    if o is None: return 'nil'
    return {
        int: str, long: str, float: str,
        bool: lambda o: '#t' if o else '#f',
        basestring: lambda o: '"%s"' % str(o),
        ONil: lambda o: '()',
        OSymbol: lambda o: o.name,
        OQuota: lambda o: "'" + format(o.objs),
        OPair: lambda o: format_list(o, lv),
        OFunction: lambda o: '<function %s>' % o.name
        }[o.__class__](o)

class PrognStatus(object):
    def __init__(self, objs): self.objs, self.rslt = objs, None
    def __repr__(self): return 'progn ' + format(self.objs)

    def __call__(self, stack, envs, objs):
        if self.objs.cdr == nil: return stack.jump(self.objs.car, envs)
        t, self.objs = self.objs.car, self.objs.cdr
        return stack.call(t, envs)

class CallStatus(object):
    def __init__(self, objs): self.objs = objs
    def __repr__(self): return 'call ' + format(self.objs)

    def __call__(self, stack, envs, objs):
        if objs is None: return stack.call(self.objs[0], envs)
        if not objs.evaled:
            return stack.jump(ParamStatus(objs, self.objs.cdr, nil), envs)
        return stack.jump(ParamStatus(objs, nil,
                                      reversed_list(self.objs.cdr)), envs)

class ParamStatus(object):
    def __init__(self, func, params, objs):
        self.func, self.params, self.objs = func, params, objs
    def __repr__(self):
        return 'call %s with (%s) <- (%s)' % (
            self.func, format(self.params), format(self.objs))

    def __call__(self, stack, envs, objs):
        if objs is not None: self.params = OPair(objs, self.params)
        if self.objs is nil: return stack.jump(self.func, envs, self.params)
        t, self.objs = self.objs.car, self.objs.cdr
        return stack.call(t, envs)

class Envs(object):
    def __init__(self, e=None, regenfast=True):
        self.e, self.fast = e, {}
        for i in reversed_list(self.e): self.fast.update(i)
    # FIXME: getstate/setstate, otherwise save/load will not work
    # TODO: regen fast?
    # in func, we need regen, otherwise don't
    def fork(self, r=None):
        if r is None: r = {}
        return Envs(OPair(r, self.e))
    def add(self, name, value):
        if self.fast: self.fast[name] = value
        self.e.car[name] = value
    def __getitem__(self, name): return self.fast[name]

class Stack(list):
    @classmethod
    def init(cls, code, builtin):
        stack = cls()
        stack.append((PrognStatus(code), Envs(to_list([{}, builtin,]))))
        return stack

    def save(self, r, f):
        self[0].envs.e.car = {}
        __import__('cPickle').dump((self, r), f, 2)
    @classmethod
    def load(cls, f, builtin):
        stack, r = __import__('cPickle').load(f)
        stack[0].envs.e.car.update(builtin)
        return stack, r

    def func_call(self, func, envs):
        o = func[0]
        if not isinstance(o, OSymbol): return CallStatus(func)
        objs = envs[o.name]
        if not objs.evaled: return ParamStatus(objs, func.cdr, nil)
        return ParamStatus(objs, nil, reversed_list(func.cdr))

    def call(self, func, envs, args=None):
        if isinstance(func, OSymbol): return (envs[func.name],)
        if isinstance(func, OQuota): return (func.objs,)
        if not callable(func): return (func,)
        if isinstance(func, OPair):
            self.append((self.func_call(func, envs), envs))
        else: self.append((func, envs))
        return (args,)

    def jump(self, func, envs, args=None):
        if isinstance(func, OSymbol): return (envs[func.name], self.pop(-1))
        if isinstance(func, OQuota): return (func.objs, self.pop(-1))
        if not callable(func): return (func, self.pop(-1))
        if isinstance(func, OPair):
            self[-1] = (self.func_call(func, envs), envs)
        else: self[-1] = (func, envs)
        return (args,)

    def trampoline(self, r=None, debug=None):
        while self:
            if debug is not None: debug(self, r)
            o = self[-1]
            r = o[0](self, o[1], r)
            if isinstance(r, tuple): r = r[0]
            else: self.pop(-1)
        return r

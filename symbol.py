#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import objects, runtime

builtin={}
def define(name, evaled=None):
    def inner(func):
        if evaled is not None: func.evaled = evaled
        builtin[name] = func
        return func
    return inner

class DefineStatus(object):
    def __init__(self, name, objs):
        self.name, self.objs = name, objs
    def __repr__(self): return 'define %s' % self.name

    def __call__(self, stack, envs, objs):
        if objs is None: stack.call(self.objs, envs)
        else: envs.add(self.name, objs)
        return objects.nil

@define('define', False)
def sym_define(stack, envs, objs):
    if isinstance(objs[0], objects.OPair):
        envs.add(objs[0].car.name,
                 objects.OFunction(objs.car.car.name, envs, objs.car.cdr, objs.cdr))
        return objects.nil
    elif isinstance(objs[0], objects.OSymbol):
        stack.jump(DefineStatus(objs[0].name, objs[1]), envs)
    raise Exception('define format error')

@define('lambda', False)
def sym_lambda(stack, envs, objs):
    return objects.OFunction('<lambda>', envs, objs.car, objs.cdr)

@define('progn', False)
def progn(stack, envs, objs):
    stack.jump(runtime.PrognStatus(objs), envs.clonedown())

@define('display', True)
@define('error', True)
def display(stack, envs, objs):
    print ' '.join(map(str, list(objs)))
    return objects.nil

@define('symbol?', True)
def is_symbol(stack, envs, objs): return isinstance(objs.car, objects.OSymbol)

@define('eq?', True)
def is_eq(stack, envs, objs):
    if isinstance(objs[0], objects.OSymbol) and isinstance(objs[1], objects.OSymbol):
        return objs[0].name == objs[1].name
    else: return objs[0] is objs[1]

class LetStatus(object):
    def __init__(self, func, syms, envs, ast):
        self.func, self.syms, self.envs, self.ast = func, syms, envs.clonedown(), ast
    def __repr__(self): return 'let ' + str(self.func)

    def __call__(self, stack, envs, objs):
        if objs is not None:
            assert(isinstance(self.syms.car[0], objects.OSymbol))
            self.envs.add(self.syms.car[0].name, objs)
            self.syms = self.syms.cdr
        if self.syms is objects.nil:
            stack.jump(runtime.PrognStatus(self.func), self.envs)
        stack.call(self.syms.car[1], self.envs if self.ast else envs)

@define('let', False)
def sym_let(stack, envs, objs):
    stack.jump(LetStatus(objs.cdr, objs.car, envs, False), envs)

@define('let*', False)
def sym_letA(stack, envs, objs):
    stack.jump(LetStatus(objs.cdr, objs.car, envs, True), envs)

# list functions
@define('list', True)
def list_list(stack, envs, objs): return objs

@define('null?', True)
def list_null(stack, envs, objs): return objs.car is objects.nil

@define('pair?', True)
def list_pair(stack, envs, objs): return isinstance(objs.car, objects.OPair)

@define('cons', True)
def list_cons(stack, envs, objs): return objects.OPair(objs[0], objs[1])

@define('car', True)
def list_car(stack, envs, objs): return objs.car.car

@define('cdr', True)
def list_cdr(stack, envs, objs): return objs.car.cdr

@define('caar', True)
def list_caar(stack, envs, objs): return objs.car.car.car

@define('cadr', True)
def list_cadr(stack, envs, objs): return objs.car.cdr.car

@define('cdar', True)
def list_cdar(stack, envs, objs): return objs.car.car.cdr

@define('caddr', True)
def list_caddr(stack, envs, objs): return objs.car.cdr.cdr.car

@define('append', True)
def list_append(stack, envs, objs):
    r = []
    for obj in objs: r.extend(obj)
    return objects.to_list(r)

class MapStatus(object):
    def __init__(self, func, params):
        self.func, self.params, self.r = func, params, []
    def __repr__(self): return 'map %s -> (%s)' % (str(self.func), str(self.params))

    def __call__(self, stack, envs, objs):
        if objs is not None: self.r.append(objs)
        if self.params[0] == objects.nil: return objects.to_list(self.r)
        t = map(lambda i: i.car, self.params)
        self.params = map(lambda i: i.cdr, self.params)
        stack.call(runtime.ParamStatus(
                self.func, objects.to_list(t), objects.nil), envs)

@define('map', True)
def list_map(stack, envs, objs): stack.jump(MapStatus(objs.car, objs.cdr), envs)

class FilterStatus(object):
    def __init__(self, func, params):
        self.func, self.params, self.r = func, params, []
    def __repr__(self): return 'filter %s -> (%s)' % (str(self.func), str(self.params))

    def __call__(self, stack, envs, objs):
        if objs is not None:
            if objs: self.r.append(self.params.car)
            self.params = self.params.cdr
        if self.params == objects.nil: return objects.to_list(self.r)
        stack.call(runtime.ParamStatus(
                self.func, objects.OPair(self.params.car), objects.nil), envs)

@define('filter', True)
def list_filter(stack, envs, objs): stack.jump(FilterStatus(objs[0], objs[1]), envs)

# logic functions
@define('not', True)
def logic_not(stack, envs, objs): return not objs[0]

@define('and', True)
def logic_and(stack, envs, objs): return reduce(lambda x, y: x and y, objs)

@define('or', True)
def logic_or(stack, envs, objs): return reduce(lambda x, y: x or y, objs)

class CondStatus(object):
    def __init__(self, conds, dft=None): self.conds, self.dft = conds, dft

    def __call__(self, stack, envs, objs):
        if objs is not None:
            if objs:
                stack.jump(self.conds.car[1], envs)
            self.conds = self.conds.cdr
        if self.conds == objects.nil:
            if self.dft is None: return objects.nil
            stack.jump(self.dft, envs)
        if isinstance(self.conds.car[0], objects.OSymbol) and \
                self.conds.car[0].name == u'else':
            stack.jump(self.conds.car[1], envs)
        stack.call(self.conds.car[0], envs)

@define('cond', False)
def logic_cond(stack, envs, objs): stack.jump(CondStatus(objs), envs)

@define('if', False)
def logic_if(stack, envs, objs):
    stack.jump(CondStatus(
            objects.OPair(objs),
            objs[2] if objs.cdr.cdr != objects.nil else None), envs)

# number functions
@define('number?', True)
def num_number(stack, envs, objs): return isinstance(objs.car, (int, long, float))

@define('+', True)
def num_add(stack, envs, objs): return sum(objs)

@define('-', True)
def num_dec(stack, envs, objs):
    s = objs.car
    for o in objs.cdr: s -= o
    return s

@define('*', True)
def num_mul(stack, envs, objs): return reduce(lambda x, y: x*y, objs)

@define('/', True)
def num_div(stack, envs, objs):
    s = objs.car
    for o in objs.cdr: s /= o
    return s

@define('=', True)
def num_eq(stack, envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] == objs[1]

@define('<', True)
def num_lt(stack, envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] < objs[1]

@define('>', True)
def num_gt(stack, envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] > objs[1]

@define('>=', True)
def num_nlt(stack, envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] >= objs[1]

@define('<=', True)
def num_ngt(stack, envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] <= objs[1]

@define('remainder', True)
def num_remainder(stack, envs, objs):
    return objs[0] % objs[1]

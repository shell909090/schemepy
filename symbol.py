#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import objects

builtin={}
def define(name, evaled=None):
    def inner(func):
        if evaled is not None: func.evaled = evaled
        builtin[name] = func
        return func
    return inner

class Function(object):
    DEBUG_NAME, DEBUG_END = False, False

    def __init__(self, name, envs, params, objs):
        self.name, self.envs = name, envs.clone()
        self.params, self.objs, self.evaled = params, objs, True

    def __call__(self, envs, objs):
        with self.envs:
            if self.DEBUG_NAME: print self.name, objs
            pn, pv = self.params, objs
            while pn is not objects.nil and pv is not objects.nil:
                if pn.car.name == '.':
                    self.envs.add(pn.cdr.car.name, pv)
                    break
                self.envs.add(pn.car.name, pv.car)
                pn, pv = pn.cdr, pv.cdr
            r = self.envs.evals(self.objs)
            if self.DEBUG_END: print self.name + ' end', r
            return r

@define('define', False)
def sym_define(envs, objs):
    if isinstance(objs[0], objects.OPair):
        func = Function(objs.car.car.name, envs, objs.car.cdr, objs.cdr)
        envs.add(objs[0].car.name, func)
    elif isinstance(objs[0], objects.OSymbol):
        envs.add(objs[0].name, envs.eval(objs[1]))
    else: raise Exception('define format error')

@define('lambda', False)
def sym_lambda(envs, objs):
    return Function('<lambda>', envs, objs.car, objs.cdr)

@define('begin', False)
def begin(envs, objs):
    with envs: return envs.evals(objs)

@define('display', True)
@define('error', True)
def display(envs, objs): print ' '.join(map(str, list(objs)))

@define('symbol?', True)
def is_symbol(envs, objs): return isinstance(objs.car, objects.OSymbol)

@define('eq?', True)
def is_eq(envs, objs):
    if isinstance(objs[0], objects.OSymbol) and \
            isinstance(objs[1], objects.OSymbol):
        return objs[0].name == objs[1].name
    else: return objs[0] is objs[1]

@define('let', False)
def let(envs, objs):
    with envs:
        for p in objs.car:
            assert(isinstance(p.car, objects.OSymbol))
            envs.add(p.car.name, envs.evals(p.cdr))
        return envs.evals(objs.cdr)

# list functions
@define('list', True)
def list_list(envs, objs): return objs

@define('null?', True)
def list_null(envs, objs): return objs.car is objects.nil

@define('pair?', True)
def list_pair(envs, objs): return isinstance(objs.car, objects.OPair)

@define('cons', True)
def list_cons(envs, objs): return objects.OPair(objs[0], objs[1])

@define('car', True)
def list_car(envs, objs): return objs.car.car

@define('cdr', True)
def list_cdr(envs, objs): return objs.car.cdr

@define('caar', True)
def list_caar(envs, objs): return objs.car.car.car

@define('cadr', True)
def list_cadr(envs, objs): return objs.car.cdr.car

@define('cdar', True)
def list_cdar(envs, objs): return objs.car.car.cdr

@define('caddr', True)
def list_caddr(envs, objs): return objs.car.cdr.cdr.car

@define('append', True)
def list_append(envs, objs):
    r = []
    for obj in objs: r.extend(obj)
    return objects.to_list(r)

@define('map', True)
def list_map(envs, objs):
    l, r = objs.cdr, []
    while l[0] is not objects.nil:
        t = map(lambda i: i.car, l)
        r.append(objs.car(envs, objects.to_list(t)))
        l = map(lambda i: i.cdr, l)
    return objects.to_list(r)

@define('filter', True)
def list_filter(envs, objs):
    f = lambda o: objs.car(envs, objects.OPair(o, objects.nil))
    return objects.to_list(filter(f, objs[1]))

# logic functions
@define('not', True)
def logic_not(envs, objs): return not objs[0]

@define('and', True)
def logic_and(envs, objs): return reduce(lambda x, y: x and y, objs)

@define('or', True)
def logic_or(envs, objs): return reduce(lambda x, y: x or y, objs)

@define('cond', False)
def logic_cond(envs, objs):
    elsecase = None
    for o in objs:
        assert(isinstance(o, objects.OPair)), '%s format error' % o
        if isinstance(o.car, objects.OSymbol) and o.car.name == 'else':
            elsecase = o.cdr
        elif envs.eval(o.car): return envs.evals(o.cdr)
    if elsecase: return envs.evals(elsecase)

@define('if', False)
def logic_if(envs, objs):
    if envs.eval(objs[0]): return envs.eval(objs[1])
    elif objs.cdr.cdr is not objects.nil: return envs.eval(objs[2])

# number functions
@define('number?', True)
def num_number(envs, objs): return isinstance(objs.car, (int, long, float))

@define('+', True)
def num_add(envs, objs): return sum(objs)

@define('-', True)
def num_dec(envs, objs):
    s = objs.car
    for o in objs.cdr: s -= o
    return s

@define('*', True)
def num_mul(envs, objs): return reduce(lambda x, y: x*y, objs)

@define('/', True)
def num_div(envs, objs):
    s = objs.car
    for o in objs.cdr: s /= o
    return s

@define('=', True)
def num_eq(envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] == objs[1]

@define('<', True)
def num_lt(envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] < objs[1]

@define('>', True)
def num_gt(envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] > objs[1]

@define('>=', True)
def num_nlt(envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] >= objs[1]

@define('<=', True)
def num_ngt(envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] <= objs[1]

@define('remainder', True)
def num_remainder(envs, objs):
    return objs[0] % objs[1]

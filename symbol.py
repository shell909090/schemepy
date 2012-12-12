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

@define('define', False)
def sym_define(stack, envs, objs):
    if isinstance(objs[0], objects.OPair):
        func = objects.OFunction(objs.car.car.name, envs, objs.car.cdr, objs.cdr)
        envs.add(objs[0].car.name, func)
    elif isinstance(objs[0], objects.OSymbol):
        raise Exception('not impl')
        envs.add(objs[0].name, envs.eval(objs[1]))
    else: raise Exception('define format error')
    return objects.nil

@define('lambda', False)
def sym_lambda(stack, envs, objs):
    return objects.OFunction('<lambda>', envs, objs.car, objs.cdr)

@define('progn', False)
def begin(stack, envs, objs):
    return stack.call(objects.PrognFrame(objs), envs.clonedown())

@define('display', True)
@define('error', True)
def display(stack, envs, objs): print ' '.join(map(str, list(objs)))

@define('symbol?', True)
def is_symbol(stack, envs, objs): return isinstance(objs.car, objects.OSymbol)

@define('eq?', True)
def is_eq(stack, envs, objs):
    if isinstance(objs[0], objects.OSymbol) and \
            isinstance(objs[1], objects.OSymbol):
        return objs[0].name == objs[1].name
    else: return objs[0] is objs[1]

# TODO: complex
# @define('let', False)
# def let(stack, envs, objs):
#     with envs:
#         for p in objs.car:
#             assert(isinstance(p.car, objects.OSymbol))
#             envs.add(p.car.name, envs.evals(p.cdr))
#         return envs.evals(objs.cdr)

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

# @define('map', True)
# def list_map(stack, envs, objs):
#     l, r = objs.cdr, []
#     while l[0] is not objects.nil:
#         t = map(lambda i: i.car, l)
#         r.append(objs.car(envs, objects.to_list(t)))
#         l = map(lambda i: i.cdr, l)
#     return objects.to_list(r)

@define('filter', True)
def list_filter(stack, envs, objs):
    f = lambda o: objs.car(envs, objects.OPair(o, objects.nil))
    return objects.to_list(filter(f, objs[1]))

# logic functions
@define('not', True)
def logic_not(stack, envs, objs): return not objs[0]

@define('and', True)
def logic_and(stack, envs, objs): return reduce(lambda x, y: x and y, objs)

@define('or', True)
def logic_or(stack, envs, objs): return reduce(lambda x, y: x or y, objs)

# @define('cond', False)
# def logic_cond(stack, envs, objs):
#     elsecase = None
#     for o in objs:
#         assert(isinstance(o, objects.OPair)), '%s format error' % o
#         if isinstance(o.car, objects.OSymbol) and o.car.name == 'else':
#             elsecase = o.cdr
#         elif envs.eval(o.car): return envs.evals(o.cdr)
#     if elsecase: return envs.evals(elsecase)

class IfFrame(object):
    def __init__(self, cond, objs):
        self.cond, self.objs = cond, objs
    def next(self, stack, envs, objs):
        if objs is None:
            stack.call(self.cond, envs)
            return True
        self.rslt = objs
        return False
    def __call__(self, stack, envs, objs):
        stack.call(self.objs[0 if self.rslt else 1], envs)

@define('if', False)
def logic_if(stack, envs, objs): return stack.call(IfFrame(objs[0], objs.cdr), envs)

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

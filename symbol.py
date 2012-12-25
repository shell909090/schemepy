#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import objects, interrupter

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
        if objs is None: return stack.call(self.objs, envs)
        envs.add(self.name, objs)
        return objects.nil

@define('define', False)
def sym_define(stack, envs, objs):
    # FIXME:
    if isinstance(objs[0], objects.OCons):
        envs.add(objs[0][0].name,
                 interrupter.OFunction(objs[0][0].name, envs,
                                       objs[0].cdr, objs.cdr))
        return objects.nil
    elif isinstance(objs[0], objects.OSymbol):
        return stack.jump(DefineStatus(objs[0].name, objs[1]), envs)
    raise Exception('define format error')

@define('lambda', False)
def sym_lambda(stack, envs, objs):
    # FIXME:
    return interrupter.OFunction('<lambda>', envs, objs.car, objs.cdr)

@define('begin', False)
def sym_begin(stack, envs, objs):
    return stack.jump(interrupter.PrognStatus(objs), envs)

@define('compile', True)
def sym_compile(stack, envs, objs):
    return interrupter.scompile(parser.split_code_tree(objs[0]))

@define('eval', True)
def sym_eval(stack, envs, objs):
    env = objs.get(1)
    if env is None: env = envs
    return stack.jump(objs[0], env)

@define('apply', True)
def sym_apply(stack, envs, objs):
    assert isinstance(objs[0], objects.OSymbol)
    func = envs[objs[0].name]
    return stack.jump(interrupter.CallStatus(
            func, objects.nil, objs[1]), envs)

@define('user-init-environment', True)
def user_init_env(stack, envs, objs): return stack[0][1]

@define('current-environment', True)
def cur_env(stack, envs, objs): return stack[-1][1]

@define('import', True)
def sym_import(stack, envs, objs):
    mod = __import__(objs[0])
    env.fast.update(mod.builtin)
    env.e.car.update(mod.builtin)

class LetStatus(object):
    def __init__(self, func, syms, envs, ast):
        self.func, self.syms, self.envs, self.ast = func, syms, envs.fork(), ast
    def __repr__(self): return 'let ' + str(self.func)

    def __call__(self, stack, envs, objs):
        if objs is not None:
            assert(isinstance(self.syms[0][0], objects.OSymbol))
            self.envs.add(self.syms[0][0].name, objs)
            self.syms = self.syms.cdr
        if self.syms is objects.nil:
            return stack.jump(interrupter.PrognStatus(self.func), self.envs)
        return stack.call(self.syms[0][1], self.envs if self.ast else envs)

@define('let', False)
def sym_let(stack, envs, objs):
    return stack.jump(LetStatus(objs.cdr, objs[0], envs, False), envs)

@define('let*', False)
def sym_letA(stack, envs, objs):
    return stack.jump(LetStatus(objs.cdr, objs[0], envs, True), envs)

@define('symbol?', True)
def is_symbol(stack, envs, objs): return isinstance(objs[0], objects.OSymbol)

@define('eq?', True)
def is_eq(stack, envs, objs):
    if isinstance(objs[0], objects.OSymbol) and isinstance(objs[1], objects.OSymbol):
        return objs[0].name == objs[1].name
    else: return objs[0] is objs[1]

# list functions
@define('list', True)
def list_list(stack, envs, objs): return objs

@define('null?', True)
def list_null(stack, envs, objs): return objs[0] is objects.nil

@define('pair?', True)
def list_pair(stack, envs, objs): return isinstance(objs[0], objects.OCons)

@define('cons', True)
def list_cons(stack, envs, objs): return objects.OCons(objs[0], objs[1])

@define('car', True)
def list_car(stack, envs, objs): return objs[0].car

@define('cdr', True)
def list_cdr(stack, envs, objs): return objs[0].cdr

@define('caar', True)
def list_caar(stack, envs, objs): return objs[0].car.car

@define('cadr', True)
def list_cadr(stack, envs, objs): return objs[0].cdr.car

@define('cdar', True)
def list_cdar(stack, envs, objs): return objs[0].car.cdr

@define('caddr', True)
def list_caddr(stack, envs, objs): return objs[0].cdr.cdr.car

@define('append', True)
def list_append(stack, envs, objs):
    r = []
    for obj in objs: r.extend(obj)
    return objects.to_list(r)

class MapStatus(object):
    def __init__(self, func, params):
        self.func, self.params, self.r = func, params, []
    def __repr__(self): return 'map %s -> (%s)' % (self.func, self.params)

    def __call__(self, stack, envs, objs):
        if objs is not None: self.r.append(objs)
        if self.params[0] is objects.nil: return objects.to_list(self.r)
        t = map(lambda i: i.car, self.params)
        self.params = map(lambda i: i.cdr, self.params)
        return stack.call(interrupter.CallStatus(
                self.func, objects.to_list(t), objects.nil), envs)

@define('map', True)
def list_map(stack, envs, objs):
    return stack.jump(MapStatus(objs.car, objs.cdr), envs)

class FilterStatus(object):
    def __init__(self, func, params):
        self.func, self.params, self.r = func, params, []
    def __repr__(self): return 'filter %s -> (%s)' % (self.func, self.params)

    def __call__(self, stack, envs, objs):
        if objs is not None:
            if objs: self.r.append(self.params.car)
            self.params = self.params.cdr
        if self.params is objects.nil: return objects.to_list(self.r)
        return stack.call(interrupter.CallStatus(
                self.func, objects.OCons(self.params.car), objects.nil), envs)

@define('filter', True)
def list_filter(stack, envs, objs):
    return stack.jump(FilterStatus(objs[0], objs[1]), envs)

# logic functions
@define('not', True)
def logic_not(stack, envs, objs): return not objs[0]

@define('and', True)
def logic_and(stack, envs, objs): return reduce(lambda x, y: x and y, objs)

@define('or', True)
def logic_or(stack, envs, objs): return reduce(lambda x, y: x or y, objs)

class CondStatus(object):
    def __init__(self, conds, dft=None): self.conds, self.dft = conds, dft
    def __repr__(self): return 'cond %s' % self.conds[0]

    def __call__(self, stack, envs, objs):
        if objs is not None:
            if objs: return stack.jump(self.conds[0][1], envs)
            self.conds = self.conds.cdr
        if self.conds is objects.nil:
            if self.dft is None: return objects.nil
            return stack.jump(self.dft, envs)
        if isinstance(self.conds[0][0], objects.OSymbol) and \
                self.conds[0][0].name == u'else':
            return stack.jump(self.conds[0][1], envs)
        return stack.call(self.conds[0][0], envs)

@define('cond', False)
def logic_cond(stack, envs, objs): return stack.jump(CondStatus(objs), envs)

@define('if', False)
def logic_if(stack, envs, objs):
    return stack.jump(CondStatus(objects.OCons(objs), objs.get(2)), envs)

# number functions
@define('number?', True)
def num_number(stack, envs, objs): return isinstance(objs[0], (int, long, float))

@define('+', True)
def num_add(stack, envs, objs): return sum(objs)

@define('-', True)
def num_dec(stack, envs, objs):
    s = objs[0]
    for o in objs.cdr: s -= o
    return s

@define('*', True)
def num_mul(stack, envs, objs): return reduce(lambda x, y: x*y, objs)

@define('/', True)
def num_div(stack, envs, objs):
    s = objs[0]
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

# other functions
@define('display', True)
@define('error', True)
def display(stack, envs, objs):
    print ' '.join(map(str, list(objs)))
    return objects.nil

@define('newline', True)
def display(stack, envs, objs):
    print
    return objects.nil

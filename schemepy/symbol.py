#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
from schemepy import parser, objects, interrupter

builtin = {}
def define(name, evaled=None):
    def inner(func):
        if evaled is not None:
            func.evaled = evaled
        builtin[name] = func
        return func
    return inner

class DefineStatus(object):
    def __init__(self, name, objs):
        self.name, self.objs = name, objs

    def __repr__(self):
        return u'define %s' % self.name

    def __call__(self, stack, envs, objs):
        if objs is None:
            return stack.call(self.objs, envs)
        envs.add(self.name, objs)
        return objects.nil

@define(u'define', False)
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

@define(u'lambda', False)
def sym_lambda(_, envs, objs):
    # FIXME:
    return interrupter.OFunction(u'<lambda>', envs, objs.car, objs.cdr)

@define(u'begin', False)
def sym_begin(stack, envs, objs):
    return stack.jump(interrupter.PrognStatus(objs), envs)

@define(u'compile', True)
def sym_compile(_, _1, objs):
    return interrupter.scompile(parser.split_code_tree(objs[0]))

@define(u'eval', True)
def sym_eval(stack, envs, objs):
    env = objs.get(1)
    if env is None:
        env = envs
    return stack.jump(objs[0], env)

@define(u'apply', True)
def sym_apply(stack, envs, objs):
    assert isinstance(objs[0], objects.OSymbol)
    func = envs[objs[0].name]
    return stack.jump(interrupter.CallStatus(
            func, objects.nil, objs[1]), envs)

@define(u'user-init-environment', True)
def user_init_env(stack, _, _1):
    return stack[0][1]

@define(u'current-environment', True)
def cur_env(stack, _, _1):
    return stack[-1][1]

@define(u'import', True)
def sym_import(_, envs, objs):
    mod = __import__(objs[0])
    envs.fast.update(mod.builtin)
    envs.e.car.update(mod.builtin)

class LetStatus(object):
    def __init__(self, func, syms, envs, ast):
        self.func, self.syms, self.envs, self.ast = func, syms, envs.fork(), ast

    def __repr__(self):
        return u'let ' + str(self.func)

    def __call__(self, stack, envs, objs):
        if objs is not None:
            assert(isinstance(self.syms[0][0], objects.OSymbol))
            self.envs.add(self.syms[0][0].name, objs)
            self.syms = self.syms.cdr
        if self.syms is objects.nil:
            return stack.jump(interrupter.PrognStatus(self.func), self.envs)
        return stack.call(self.syms[0][1], self.envs if self.ast else envs)

@define(u'let', False)
def sym_let(stack, envs, objs):
    return stack.jump(LetStatus(objs.cdr, objs[0], envs, False), envs)

@define(u'let*', False)
def sym_letA(stack, envs, objs):
    return stack.jump(LetStatus(objs.cdr, objs[0], envs, True), envs)

@define(u'symbol?', True)
def is_symbol(_, _1, objs):
    return isinstance(objs[0], objects.OSymbol)

@define(u'eq?', True)
def is_eq(_, _1, objs):
    o = objs[0]
    return all(map(lambda i: i is o, objs))

def obj_equal(l, r):
    if l.__class__ is not l.__class__:
        return False
    if isinstance(l, basestring):
        return l == r
    if hasattr(l, '__iter__'):
        return all(map(lambda i: obj_equal(*i), zip(l, r)))
    return l is r

@define(u'equal?', True)
def is_equal(_, _1, objs):
    o = objs[0]
    return all(map(lambda i: obj_equal(i, o), objs))

# logic functions
@define(u'not', True)
def logic_not(_, _1, objs):
    return not objs[0]

@define(u'and', True)
def logic_and(_, _1, objs):
    return reduce(lambda x, y: x and y, objs)

@define(u'or', True)
def logic_or(_, _1, objs):
    return reduce(lambda x, y: x or y, objs)

class CondStatus(object):
    def __init__(self, conds, dft=None):
        self.conds, self.dft = conds, dft

    def __repr__(self):
        return u'cond %s' % self.conds[0]

    def __call__(self, stack, envs, objs):
        if objs is not None:
            if objs:
                return stack.jump(
                    interrupter.PrognStatus(self.conds[0].cdr), envs)
            self.conds = self.conds.cdr
        if self.conds is objects.nil:
            if self.dft is None:
                return objects.nil
            return stack.jump(self.dft, envs)
        if isinstance(self.conds[0][0], objects.OSymbol)\
                and self.conds[0][0].name == u'else':
            return stack.jump(self.conds[0][1], envs)
        return stack.call(self.conds[0][0], envs)

@define(u'cond', False)
def logic_cond(stack, envs, objs):
    return stack.jump(CondStatus(objs), envs)

@define(u'if', False)
def logic_if(stack, envs, objs):
    return stack.jump(CondStatus(objects.OCons(
                objects.to_list([objs[0], objs[1]])), objs.get(2)), envs)

@define(u'when', False)
def logic_when(stack, envs, objs):
    return stack.jump(CondStatus(objects.OCons(objs)), envs)

# string functions
@define(u'string=?', True)
def str_equal(_, _1, objs):
    o = objs[0]
    for i in objs:
        if not isinstance(i, basestring):
            return False
        if i != o:
            return False
    return True

# other functions
@define(u'display', True)
@define(u'error', True)
def display(_, _1, objs):
    print ' '.join(map(unicode, list(objs)))
    return objects.nil

@define(u'newline', True)
def newline(_, _1, _2):
    print
    return objects.nil

@define(u'exit', True)
def do_exit(_, _1, objs):
    raise interrupter.ExitException(objs)

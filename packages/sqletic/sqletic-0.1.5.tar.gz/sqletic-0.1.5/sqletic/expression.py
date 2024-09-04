from sqlton.ast import Alias, Operation, Column, Select
from sqletic.scope import lookup
import datetime
import operator
from re import sub, match
from functools import partial

def not_implemented(a, b):
    raise NotImplementedError()

def like(a, b):
    for rule, replacement in ((r'\.', r'\.'),
                              (r'%', '.*'),
                              (r'_', '.')):
        b = sub(rule, replacement, b)
    _match = match('^' + b + '$', a)
    return  _match is not None

def exists(_, b):
    return any(b)

def contains(a, b):
    return operator.contains(b, a)

class Evaluator:
    functions = {'concat':lambda *args:''.join((arg
                                                if isinstance(arg, str)
                                                else repr(arg))
                                               for arg in args)}

    def __init__(self, scope, engine):
        self.scope = scope
        self.engine = engine

    def __call__(self, expression):
        if isinstance(expression, Operation):
            return self.operation(expression.operator,
                                  expression.a, expression.b)
        elif isinstance(expression, Column):
            return lookup(self.scope,
                          (expression.table.name, expression.name)
                          if expression.table
                          else expression.name)
        elif isinstance(expression, Select):
            return iter(self.engine.iterate(self.scope, expression))
        else:
            return expression

    def operation(self, operator, a, b):
        method_name = '_'.join(('operator', *operator)).lower()

        operands = self(a), self(b)

        if hasattr(self, method_name):
            operator = getattr(self, method_name)
        else:
            operator = self.operators[operator]

        return operator(*operands)


    def operator_call(self, identifier, parameter):
        arguments = []
        for argument in parameter['arguments']:
            arguments.append(self(argument))

        return self.functions[identifier](*arguments)

    kinds = {'BINARY':bin,
             'CHAR':str,
             'DATE':datetime.date.fromisoformat,
             'DATETIME':datetime.datetime.fromisoformat,
             'DECIMAL':float,
             'DOUBLE':float,
             'INTERGER':int,
             'SIGNED':int,
             'UNSIGNED':lambda value: abs(int(value)),
             'TIME':datetime.time.fromisoformat,
             'VARCHAR':str}

    def operator_cast(self, value, kind):
        return self.kinds[kind](self(value))

    operators = {('=',): operator.eq,
                 ('<>',): operator.ne,
                 ('!=',): operator.ne,
                 ('<=',): operator.le,
                 ('>=',): operator.ge,
                 ('<',): operator.lt,
                 ('>',): operator.gt,
                 ('*',): operator.mul,
                 ('/',): operator.truediv,
                 ('+',): operator.add,
                 ('-',): operator.sub,
                 ('AND',): operator.and_,
                 ('OR',): operator.or_,
                 ('IN',): contains,
                 ('EXISTS',): exists,
                 ('LIKE',): like,
                 ('GLOB',): not_implemented,
                 ('REGEXP',): lambda a, b: match(b, a) is not None,
                 ('MATCH',): not_implemented,
                 ('NOT', 'IN'): lambda a, b: not contains(a, b)}
    

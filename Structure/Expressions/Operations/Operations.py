import sys

sys.path.append('../')

from Structure.Interfaces.Expression import Expression
from enum import Enum


class Operator(Enum):
    SUM = 1
    MULT = 2
    SUBS = 3
    DIV = 4
    POT = 5
    MOD = 6
    LESSTH = 7
    GREATERTH = 8
    LESSOREQ = 9
    GREATOREQ = 10
    EQUALEQUAL = 11
    DIFF = 12
    AND = 13
    OR = 14
    NOT = 15
    UNARY = 16


def getStringOperator(op):
    if op == Operator.SUM:
        return '+'
    elif op == Operator.SUBS:
        return '-'
    elif op == Operator.MULT:
        return '*'
    elif op == Operator.DIV:
        return '/'
    elif op == Operator.POT:
        return '^'
    elif op == Operator.MOD:
        return '%'
    elif op == Operator.LESSTH:
        return '<'
    elif op == Operator.GREATERTH:
        return '>'
    elif op == Operator.LESSOREQ:
        return '<='
    elif op == Operator.GREATOREQ:
        return '>='
    elif op == Operator.EQUALEQUAL:
        return '=='
    elif op == Operator.DIFF:
        return '!='
    elif op == Operator.AND:
        return '&&'
    elif op == Operator.OR:
        return '||'
    elif op == Operator.NOT:
        return '!'
    elif op == Operator.UNARY:
        return 'UNARIO'


class Operation(Expression):

    def __init__(self, exp1, operator, exp2, line, column, expU) -> None:
        super().__init__()
        self.exp1: Expression = exp1
        self.Operator: Operator = self.getOperator(operator)
        self.exp2: Expression = exp2
        self.line: int = line
        self.column: int = column
        self.expU: Expression = expU

    def getOperator(self, op) -> Operator:
        if op == '+':
            return Operator.SUM
        elif op == '-':
            return Operator.SUBS
        elif op == '*':
            return Operator.MULT
        elif op == '/':
            return Operator.DIV
        elif op == '^':
            return Operator.POT
        elif op == '%':
            return Operator.MOD
        elif op == '<':
            return Operator.LESSTH
        elif op == '>':
            return Operator.GREATERTH
        elif op == '<=':
            return Operator.LESSOREQ
        elif op == '>=':
            return Operator.GREATOREQ
        elif op == '==':
            return Operator.EQUALEQUAL
        elif op == '!=':
            return Operator.DIFF
        elif op == '&&':
            return Operator.AND
        elif op == '||':
            return Operator.OR
        elif op == '!':
            return Operator.NOT
        elif op == 'UNARIO':
            return Operator.UNARY

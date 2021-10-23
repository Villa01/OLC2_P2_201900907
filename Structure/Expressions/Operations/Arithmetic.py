import sys

from Structure.AST.Node import Node
from Structure.Instructions.Transference_structures.Return import Return

sys.path.append('../')

from Structure.Expressions.Operations.Operations import Operation, Operator, getStringOperator
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Types
from Structure.Driver import Driver
from Structure.Interfaces.Expression import Expression


class Arithmetic(Operation, Expression):
    """Manages all the aritmethic operations
       Parameters
        ----------
        exp1: Expression 
            first operand
        operator: string
                the string of an operator
        exp2: Expression 
            second operand
        line: number
            line where it was obtained
        column : number
            position where it was obtained
        expU : Expression
            If there is an unary expression this is it.
    """

    def __init__(self, exp1: Expression, operator: Operator, exp2: Expression, line: int, column: int,
                 expU: Expression) -> None:
        Operation.__init__(self=self, exp1=exp1, operator=operator, exp2=exp2, line=line, column=column, expU=expU)

    def getType(self, driver: Driver, ts: SymbolTable):
        value = self.getValue(driver, ts)

        if type(value) == float:
            return Types.FLOAT64
        elif type(value) == int:
            return Types.INT64
        elif type(value) == str and len(value) > 1:
            return Types.STRING
        elif type(value) == str and len(value) < 1:
            return Types.CHAR
        elif type(value) == bool:
            return Types.BOOL
        elif type(value) == range:
            return Types.RANGE
        elif type(value) == list:
            return Types.ARRAY

    def getValue(self, driver: Driver, ts: SymbolTable):

        valor_exp1 = None
        valor_exp2 = None
        valor_expU = None

        if not self.expU:
            valor_exp1 = self.exp1.getValue(driver, ts)
            valor_exp2 = self.exp2.getValue(driver, ts)
        else:
            valor_expU = self.exp1.getValue(driver, ts)

        # Sum
        if self.Operator == Operator.SUM:
            # int64 or float64
            if type(valor_exp1) == int or type(valor_exp1) == float:
                # int64 + int64 or float64 + float64
                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 + valor_exp2
                else:
                    driver.agregarError(f'No se admite la suma con los tipos definidos', self.line, self.column)
            else:
                driver.agregarError(f'No se admite la suma con los tipos definidos', self.line, self.column)
        # Substraction   
        elif self.Operator == Operator.SUBS:
            # int64 or float64
            if type(valor_exp1) == int or type(valor_exp1) == float:
                # int64 - int64 or float64 - float64
                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 - valor_exp2
                else:
                    driver.agregarError(f'No se admite la resta con los tipos definidos', self.line, self.column)
            else:
                driver.agregarError(f'No se admite la resta con los tipos definidos', self.line, self.column)
        # Multiplication
        elif self.Operator == Operator.MULT:
            # int64 or float64
            if type(valor_exp1) == int or type(valor_exp1) == float:
                # int64 - int64 or float64 - float64
                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 * valor_exp2
                else:
                    driver.agregarError(f'No se admite la multiplicacion con los tipos definidos', self.line,
                                        self.column)
            # string 
            if type(valor_exp1) == str:
                # string * string 
                if type(valor_exp2) == str:
                    return valor_exp1 + valor_exp2
                else:
                    driver.agregarError(f'No se admite la multiplicacion con los tipos definidos', self.line,
                                        self.column)
            else:
                driver.agregarError(f'No se admite la multiplicacion con los tipos definidos', self.line, self.column)
        # Division
        elif self.Operator == Operator.DIV:
            # int64 or float64
            if type(valor_exp1) == int or type(valor_exp1) == float:
                # int64 - int64 or float64 / float64
                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 / valor_exp2
                else:
                    driver.agregarError(f'No se admite la division con los tipos definidos', self.line, self.column)
            else:
                driver.agregarError(f'No se admite la division con los tipos definidos', self.line, self.column)
        elif self.Operator == Operator.POT:
            # int64 or float64
            if type(valor_exp1) == int or type(valor_exp1) == float:
                # int64 - int64 or float64 / float64
                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 ** valor_exp2
                else:
                    driver.agregarError(f'No se admite la potencia con los tipos definidos', self.line, self.column)
            # string 
            if type(valor_exp1) == str:
                # string ^ int
                if type(valor_exp2) == int:
                    return valor_exp1 * valor_exp2
                else:
                    driver.agregarError(f'No se admite la potencia con los tipos definidos', self.line, self.column)
            else:
                # TODO: agregar error semantico
                pass
        elif self.Operator == Operator.MOD:
            # int64 or float64
            if type(valor_exp1) == int or type(valor_exp1) == float:
                # int64 - int64 or float64 / float64
                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 % valor_exp2
                else:
                    driver.agregarError(f'No se admite el modulo con los tipos definidos', self.line, self.column)
            else:
                driver.agregarError(f'No se admite el modulo con los tipos definidos', self.line, self.column)

        elif self.Operator == Operator.UNARY:
            if type(valor_expU) == int or type(valor_expU) == float:
                return -valor_expU
            else:
                driver.agregarError(f'No se admite el complemento aritmetico con los tipos definidos', self.line,
                                    self.column)
        else:
            driver.agregarError(f'No se admite la operacion', self.line, self.column)

    def compilar(self, driver, ts, tmp):
        left_value = self.exp1.compilar(driver, ts, tmp)
        right_value = self.exp2.compilar(driver, ts, tmp)

        temp = tmp.new_temp()
        op = getStringOperator(self.Operator)

        if self.Operator == Operator.POT:
            tmp.fPotencia()
            param_temp = tmp.new_temp()

            tmp.add_exp(param_temp, tmp.P, ts.get_size(), '+')
            tmp.add_exp(param_temp, param_temp, '1', '+')
            tmp.set_stack(param_temp, left_value.value)

            tmp.add_exp(param_temp, param_temp, '1', '+')
            tmp.set_stack(param_temp, right_value.value)

            tmp.new_env(ts.get_size())
            tmp.llamar_func('potencia')

            temp = tmp.new_temp()
            tmp.get_stack(temp, tmp.P)
            tmp.ret_env(ts.get_size())

            return Return(temp, Types.INT64, True)
        else:
            tmp.add_exp(temp, left_value.value, right_value.value, op)
            return Return(temp, Types.INT64, True)

    def traverse(self):
        padre = Node("Exp", "")
        temp = Operation(None, None, None, None, None, None)
        sOp = getStringOperator(self.Operator)
        if self.expU:
            padre.AddHijo(Node(sOp, ""))
            padre.AddHijo(self.exp1.traverse())
        else:
            padre.AddHijo(self.exp1.traverse())
            padre.AddHijo(Node(sOp, ""))
            padre.AddHijo(self.exp2.traverse())

        return padre

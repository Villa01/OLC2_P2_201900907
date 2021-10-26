from Structure.AST.Node import Node
import re
import sys

from Structure.Instructions.Transference_structures.Return import Return
from Structure.Instructions.Transference_structures.ReturnStructure import ReturnStructure
from Temporal import Temporal

sys.path.append('../')

from Structure.Expressions.Operations.Operations import Operation, Operator
from Structure.Expressions.Operations.Operations import getStringOperator
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Structure.Interfaces.Expression import Expression
from Structure.SymbolTable.Type import Types


class Relational(Operation, Expression):
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

    def getValue(self, driver: Driver, ts: SymbolTable):

        valor_exp1 = None
        valor_exp2 = None
        valor_expU = None

        if (self.expU == False):
            valor_exp1 = self.exp1.getValue(driver, ts)
            valor_exp2 = self.exp2.getValue(driver, ts)
        else:
            valor_expU = self.exp1.getValue(driver, ts)

        if self.Operator == Operator.LESSTH:
            if type(valor_exp1) == int or type(valor_exp1) == float:

                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 < valor_exp2
                else:
                    driver.agregarError(f'No se admite el < and con los tipos definidos', self.line, self.column)
            elif type(valor_exp1) == str:
                if type(valor_exp2) == str:
                    return valor_exp1 < valor_exp2
                else:
                    driver.agregarError(f'No se admite el operador < con los tipos definidos', self.line, self.column)
            else:
                driver.agregarError(f'No se admite el operador < con los tipos definidos', self.line, self.column)
        elif self.Operator == Operator.GREATERTH:
            if type(valor_exp1) == int or type(valor_exp1) == float:

                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 > valor_exp2
                else:
                    driver.agregarError(f'No se admite el operador > con los tipos definidos', self.line, self.column)

            elif type(valor_exp1) == str:
                if type(valor_exp2) == str:
                    return valor_exp1 > valor_exp2
                else:
                    driver.agregarError(f'No se admite el operador > con los tipos definidos', self.line, self.column)
            else:
                driver.agregarError(f'No se admite el operador > con los tipos definidos', self.line, self.column)

        elif self.Operator == Operator.LESSOREQ:
            if type(valor_exp1) == int or type(valor_exp1) == float:

                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 <= valor_exp2
                elif type(valor_exp2) == bool:
                    return valor_exp1 <= valor_exp2
                else:
                    driver.agregarError(f'No se admite el operador <= con los tipos definidos', self.line, self.column)

            elif type(valor_exp1) == bool:
                if type(valor_exp2) == bool:
                    return valor_exp1 <= valor_exp2
                elif type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 <= valor_exp2
                else:
                    driver.agregarError(f'No se admite el operador <= con los tipos definidos', self.line, self.column)

            elif type(valor_exp1) == str:
                if type(valor_exp2) == str:
                    return valor_exp1 <= valor_exp2
                else:
                    driver.agregarError(f'No se admite el operador <= con los tipos definidos', self.line, self.column)

            else:
                driver.agregarError(f'No se admite el operador <= con los tipos definidos', self.line, self.column)

        elif self.Operator == Operator.GREATOREQ:
            if type(valor_exp1) == int or type(valor_exp1) == float:

                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 >= valor_exp2
                elif type(valor_exp2) == bool:
                    return valor_exp1 >= valor_exp2
                else:
                    driver.agregarError(f'No se admite el operador >= con los tipos definidos', self.line, self.column)

            elif type(valor_exp1) == bool:
                if type(valor_exp2) == bool:
                    return valor_exp1 >= valor_exp2
                elif type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 >= valor_exp2
                else:
                    driver.agregarError(f'No se admite el operador >= con los tipos definidos', self.line, self.column)

            elif type(valor_exp1) == str:
                if type(valor_exp2) == str:
                    return valor_exp1 >= valor_exp2
                else:
                    driver.agregarError(f'No se admite el operador >= con los tipos definidos', self.line, self.column)
            else:
                driver.agregarError(f'No se admite el operador >= con los tipos definidos', self.line, self.column)

        elif self.Operator == Operator.EQUALEQUAL:
            if type(valor_exp1) == int or type(valor_exp1) == float:

                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 == valor_exp2
                elif type(valor_exp2) == bool:
                    return valor_exp1 == valor_exp2
                else:
                    driver.agregarError(f'No se admite el operador == con los tipos definidos', self.line, self.column)

            elif type(valor_exp1) == bool:
                if type(valor_exp2) == bool:
                    return valor_exp1 == valor_exp2
                elif type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 == valor_exp2
                else:
                    driver.agregarError(f'No se admite el operador == con los tipos definidos', self.line, self.column)

            elif type(valor_exp1) == str:
                if type(valor_exp2) == str:
                    return valor_exp1 == valor_exp2
                else:
                    driver.agregarError(f'No se admite el operador == con los tipos definidos', self.line, self.column)

            else:
                driver.agregarError(f'No se admite el operador == con los tipos definidos', self.line, self.column)

        elif self.Operator == Operator.DIFF:
            if type(valor_exp1) == int or type(valor_exp1) == float:

                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 != valor_exp2
                elif type(valor_exp2) == bool:
                    return valor_exp1 != valor_exp2
                else:
                    driver.agregarError(f'No se admite el operador != con los tipos definidos', self.line, self.column)

            elif type(valor_exp1) == bool:
                if type(valor_exp2) == bool:
                    return valor_exp1 != valor_exp2
                elif type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 != valor_exp2
                else:
                    driver.agregarError(f'No se admite el operador != con los tipos definidos', self.line, self.column)

            elif type(valor_exp1) == str:
                if type(valor_exp2) == str:
                    return valor_exp1 != valor_exp2
                else:
                    driver.agregarError(f'No se admite el operador != con los tipos definidos', self.line, self.column)

        else:
            driver.agregarError(f'No se admite la operacion', self.line, self.column)

    def compilar(self, driver: Driver, symbol_table: SymbolTable, tmp: Temporal):

        left = self.exp1.compilar(driver, symbol_table, tmp)

        tmp.add_comment('Inicio de expresion relacional')

        result = Return(None, Types.BOOL, False)

        if left.type != Types.BOOL:

            right = self.exp2.compilar(driver, symbol_table, tmp)
            if (left.type == Types.INT64 or left.type == Types.FLOAT64) and (right.type == Types.INT64 or right.type ==
                                                                             Types.FLOAT64):
                self.checkLabels(tmp)
                tmp.add_if(left.value, getStringOperator(self.Operator), right.value, self.true_label)
                tmp.add_goto(self.false_label)
            else:
                # Agregar comparacion de cadenas
                driver.agregarError(f'No se admite la operacion con los tipos definidos para la expresion relacional', self.line, self.column)
        else:
            goto_right = tmp.new_label()
            tmp.new_label()
            left_temp = tmp.get_label()

            tmp.imprimir_label(left.true_lbl)
            tmp.add_exp(left_temp, '1', '', '')
            tmp.add_goto(goto_right)

            tmp.imprimir_label(left.false_lbl)
            tmp.add_exp(left_temp, '0', '', '')

            tmp.imprimir_label(goto_right)

            right: Return = self.exp2.compilar(driver, symbol_table, tmp)

            if right.type != Types.BOOL:
                driver.agregarError("No se puede comparar", self.line, self.column)
                return
            goto_end = tmp.new_label()
            right_temp = tmp.new_temp()

            tmp.imprimir_label(right.true_lbl)

            tmp.add_exp(right_temp, '1', '', '')
            tmp.add_goto(goto_end)

            tmp.imprimir_label(right.false_lbl)
            tmp.add_exp(right_temp, '0', '', '')

            tmp.imprimir_label(goto_end)

            self.checkLabels(tmp)
            tmp.add_if(left_temp, right_temp, Operation.getOperator(self.Operator), self.true_label)
            tmp.add_goto(self.false_label)

        tmp.add_comment('FIn expresion relacional')
        result.true_lbl = self.true_label
        result.false_lbl = self.false_label
        return result

    def traverse(self):
        padre = Node("RELACIONAL", "");
        temp = Operation(None, None, None, None, None, None)
        sOp = getStringOperator(self.Operator)
        if self.expU:
            padre.AddHijo(Node(sOp, ""))
            padre.AddHijo(self.exp1.traverse());
        else:
            padre.AddHijo(self.exp1.traverse());
            padre.AddHijo(Node(sOp, ""))
            padre.AddHijo(self.exp2.traverse());

        return padre

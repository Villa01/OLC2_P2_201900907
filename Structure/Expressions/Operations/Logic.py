from Structure.AST.Node import Node
from Structure.Instructions.Transference_structures.Return import Return
from Structure.SymbolTable.Type import Types
import re
import sys

from Temporal import Temporal

sys.path.append('../')

from Structure.Expressions.Operations.Operations import Operation, Operator, getStringOperator
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Structure.Interfaces.Expression import Expression


class Logic(Operation, Expression):

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

        if not self.expU:
            valor_exp1 = self.exp1.getValue(driver, ts)
            valor_exp2 = self.exp2.getValue(driver, ts)
        else:
            valor_expU = self.exp1.getValue(driver, ts)

        if self.Operator == Operator.AND:
            if type(valor_exp1) == bool:
                if type(valor_exp2) == bool:
                    return valor_exp1 and valor_exp2
                else:
                    driver.agregarError(f'No se admite el operador and con los tipos definidos', self.line, self.column)
            else:
                driver.agregarError(f'No se admite el operador and con los tipos definidos', self.line, self.column)

        elif self.Operator == Operator.OR:
            if type(valor_exp1) == bool:
                if type(valor_exp2) == bool:
                    return valor_exp1 or valor_exp2
                else:
                    driver.agregarError(f'No se admite el operador or con los tipos definidos', self.line, self.column)
            else:
                driver.agregarError(f'No se admite el operador or con los tipos definidos', self.line, self.column)

        elif self.Operator == Operator.NOT:
            if type(valor_expU) == bool:
                return not valor_expU
            else:
                driver.agregarError(f'No se admite el operador not con los tipos definidos', self.line, self.column)

        else:
            driver.agregarError(f'No se admite la operacion', self.line, self.column)

    def compilar(self, driver: Driver, symbol_table: SymbolTable, tmp: Temporal):
        tmp.add_comment('Inicio Expresion Logica')

        self.checkLabels(tmp)
        lbl_and_or = ''

        if self.Operator == Operator.AND:
            lbl_and_or = self.exp1.true_label = tmp.new_label()
            self.exp2.true_label = self.true_label
            self.exp1.false_label = self.exp2.false_label = self.false_label
        elif self.Operator == Operator.OR:
            self.exp1.true_label = self.exp2.true_label = self.true_label
            lbl_and_or = self.exp1.false_label = tmp.new_label()
            self.exp2.false_label = self.false_label
        else:
            self.exp1.true_label = self.false_label
            self.exp1.false_label = self.true_label

        if not self.expU:
            left = self.exp1.compilar(driver, symbol_table, tmp)
            if left.type != Types.BOOL:
                driver.agregarError('La primera expresion no es booleana', self.line, self.column)
                return
            tmp.imprimir_label(lbl_and_or)
            right = self.exp2.compilar(driver, symbol_table, tmp)
            if right.type != Types.BOOL:
                driver.agregarError('La segunda expresion no es booleana', self.line, self.column)
                return
        else:
            left = self.exp1.compilar(driver, symbol_table, tmp)
            if left.type != Types.BOOL:
                driver.agregarError('La primera expresion no es booleana', self.line, self.column)
                return

        tmp.add_comment('Finaliza expresion logica')
        ret = Return(None, Types.BOOL, False)
        ret.true_lbl = self.true_label
        ret.false_lbl = self.false_label
        return ret

    def traverse(self):
        padre = Node("LOGICA", "");
        temp = Operation(None, None, None, None, None, None)
        sOp = getStringOperator(self.Operator);
        if self.expU:
            padre.AddHijo(Node(sOp, ""))
            padre.AddHijo(self.exp1.traverse());
        else:
            padre.AddHijo(self.exp1.traverse());
            padre.AddHijo(Node(sOp, ""))
            padre.AddHijo(self.exp2.traverse());

        return padre

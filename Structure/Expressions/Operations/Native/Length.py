
from Structure.Instructions.Transference_structures.Return import Return
from Structure.AST.Node import Node
from Structure.Interfaces.Expression import Expression
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Types

import math

from Temporal import Temporal


class Length(Expression):

    def __init__(self, exp: Expression, line: int, column: int) -> None:
        super().__init__()
        self.exp = exp
        self.line = line
        self.column = column

    def getType(self, driver: Driver, ts: SymbolTable):
        return Types.INT64

    def getValue(self, driver: Driver, ts: SymbolTable):
        exp_value = self.exp.getValue(driver, ts)

        if type(exp_value) == str or type(exp_value) == list:
            return len(exp_value)
        else:
            driver.agregarError(f'No se admite la expresion en la funcion Length', self.line, self.column)

    def compilar(self, driver: Driver, symbol_table: SymbolTable, tmp: Temporal) -> Return:

        ret_exp = self.exp.compilar(driver, symbol_table, tmp)

        heap_pos = ret_exp.value
        tamanio_temp = tmp.new_temp()
        tmp.get_heap(tamanio_temp, heap_pos)

        return Return(tamanio_temp, ret_exp.type, True)

    def traverse(self):
        padre = Node("LENGTH", "")
        padre.AddHijo(Node("length", ""))
        padre.AddHijo(Node("(", ""))
        padre.AddHijo(self.exp.traverse())
        padre.AddHijo(Node(")", ""))

        return padre


from Structure.AST.Node import Node
from Structure.Interfaces.Expression import Expression
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Types

import math

class Sin (Expression):

    def __init__(self, exp : Expression, line : int, column : int) -> None:
        super().__init__()
        self.exp = exp
        self.line = line
        self.column = column

    def getType(self, driver: Driver, ts : SymbolTable):
        return Types.FLOAT64

    def getValue(self, driver: Driver, ts : SymbolTable):
        exp_value = self.exp.getValue(driver, ts)


        if type(exp_value) == int or type(exp_value) == float:
            return math.sin(exp_value)
        else:
            driver.agregarError(f'No se admite la expresion en la funcion sin', self.line, self.column)

    def traverse(self):
        padre = Node("SIN","")
        padre.AddHijo(Node("sin",""))
        padre.AddHijo(Node("(",""))
        padre.AddHijo(self.exp.traverse())
        padre.AddHijo(Node(")",""))

        return padre

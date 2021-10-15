
from Structure.AST.Node import Node
from Structure.Interfaces.Expression import Expression
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Types

import math

class Sqrt (Expression):

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
            if(exp_value >= 0):
                return math.sqrt(exp_value)
            else:
                driver.agregarError(f'La expresion de la funcion sqrt debe ser mayor o igual a 0', self.line, self.column)

        else:
            driver.agregarError(f'No se admite la expresion en la funcion sqrt', self.line, self.column)

    def traverse(self):
        padre = Node("SQRT","")
        padre.AddHijo(Node("sqrt",""))
        padre.AddHijo(Node("(",""))
        padre.AddHijo(self.exp.traverse())
        padre.AddHijo(Node(")",""))

        return padre

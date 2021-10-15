
from Structure.AST.Node import Node
from Structure.Interfaces.Expression import Expression
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Types

import math

class Logarithm (Expression):

    def __init__(self, base: Expression, exp : Expression, line : int, column : int) -> None:
        super().__init__()
        self.exp = exp
        self.line = line
        self.base = base
        self.column = column

    def getType(self, driver: Driver, ts : SymbolTable):
        return Types.FLOAT64

    def getValue(self, driver: Driver, ts : SymbolTable):
        exp_value = self.exp.getValue(driver, ts)
        base_value = self.base.getValue(driver, ts)


        if type(exp_value) == int or type(exp_value) == float:
            if type(base_value) == int or type(base_value) == float:
                if exp_value > 0:
                    if base_value > 1:
                        return math.log(exp_value, base_value)
                    else: 
                        driver.agregarError(f'La base debe ser mayor que 1', self.line, self.column)
                else: 
                    driver.agregarError(f'La expresion debe ser mayor que 0', self.line, self.column)

            else: 
                driver.agregarError(f'No se admite la base en la funcion Log', self.line, self.column)
        else:
            driver.agregarError(f'No se admite la expresion en la funcion Log', self.line, self.column)

    def traverse(self):
        padre = Node("LOG","")
        padre.AddHijo(Node("log",""))
        padre.AddHijo(Node("(",""))
        padre.AddHijo(self.base.traverse())
        padre.AddHijo(Node(",",""))
        padre.AddHijo(self.exp.traverse())
        padre.AddHijo(Node(")",""))

        return padre

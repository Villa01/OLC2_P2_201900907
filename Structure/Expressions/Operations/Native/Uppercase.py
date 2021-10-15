
from Structure.AST.Node import Node
from Structure.Interfaces.Expression import Expression
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Types


class Uppercase (Expression):

    def __init__(self, exp : Expression, line : int, column : int) -> None:
        super().__init__()
        self.exp = exp
        self.line = line
        self.column = column

    def getType(self, driver: Driver, ts : SymbolTable):
        return Types.STRING

    def getValue(self, driver: Driver, ts : SymbolTable):
        exp_value = self.exp.getValue(driver, ts)


        if type(exp_value) == str:
            return exp_value.upper()
        else:
            driver.agregarError(f'Solo se admiten valores string en la funcion upper', self.line, self.column)

    def traverse(self):
        padre = Node("UPPERCASE","")
        padre.AddHijo(Node("uppercase",""))
        padre.AddHijo(Node("(",""))
        padre.AddHijo(self.exp.traverse())
        padre.AddHijo(Node(")",""))

        return padre


from Structure.AST.Node import Node
from Structure.Interfaces.Expression import Expression
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Types

class Typeof (Expression):

    def __init__(self, exp : Expression, line : int, column : int) -> None:
        super().__init__()
        self.exp = exp
        self.line = line
        self.column = column

    def getType(self, driver: Driver, ts : SymbolTable):
        return self.exp.getType(driver, ts)

    def getValue(self, driver: Driver, ts : SymbolTable):
        t = self.exp.getType(driver, ts)
        if t == Types.INT64:
            return "Int64"
        elif t == Types.FLOAT64:
            return "Float64"
        elif t == Types.STRING:
            return "String"
        elif t == Types.CHAR:
            return "Char"
        elif t == Types.BOOL:
            return "Bool"
        elif t == Types.NOTHING:
            return "Nothing"
        elif t == Types.RANGE:
            return "Range"
        elif t == Types.ARRAY:
            return "Array"
        else:
            driver.agregarError(f'No se pudo obtener el tipo', self.line, self.column)

    def traverse(self):
        padre = Node("TYPEOF","")
        padre.AddHijo(Node("typoeof",""))
        padre.AddHijo(Node("(",""))
        padre.AddHijo(self.exp.traverse())
        padre.AddHijo(Node(")",""))

        return padre

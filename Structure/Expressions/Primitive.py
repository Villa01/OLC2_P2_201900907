
from Structure.AST.Node import Node
from Structure.Interfaces.Expression import Expression
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Structure.SymbolTable.Type import Types

class Primitive(Expression):

    def __init__(self, primitive, line: int, column : int) -> None:
        self.primitive = primitive
        self.line = line
        self.column = column

    def getType(self, driver : Driver, ts : SymbolTable):
        value = self.getValue(driver, ts)

        if type(value) == float:
            return Types.FLOAT64
        elif type(value) == int:
            return Types.INT64
        elif type(value) == str:
            return Types.STRING
        elif type(value) == bool :
            return Types.BOOL
        elif type(value) == list:
            return Types.ARRAY
        elif type(value) == range:
            return Types.RANGE
        

    def getValue(self, driver : Driver, ts: SymbolTable):
        return self.primitive

    def compilar(self, driver, st, tmp):
        return self.getValue(driver, st)

    def traverse(self):
        padre = Node("Primitivo", "")
        pr = self.primitive
        if not type(self.primitive) == str:
            pr = str(pr)
        padre.AddHijo(Node(pr, ""))

        return padre

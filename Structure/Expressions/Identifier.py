
from Structure.AST.Node import Node
from Structure.Interfaces.Expression import Expression
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Structure.SymbolTable.Type import Types

class Identifier(Expression):

    def __init__(self, id: str, line: int, column: int) -> None:
        self.id = id
        self.line = line
        self.column = column

    def getType(self, driver: Driver, ts: SymbolTable):

        temp_sym = ts.getSymbol(self.id)

        if temp_sym != None:
            return temp_sym.symbol_type.type

    def getValue(self, driver: Driver, ts: SymbolTable):
        temp_sym = ts.getSymbol(self.id)

        if temp_sym != None:
            return temp_sym.value

        else:
            driver.agregarError(f'No se pudo encontrar el simbolo: {self.id}',self.line, self.column)

    def traverse(self):
        padre = Node("ID", "")
        padre.AddHijo(Node(self.id, ""))

        return padre
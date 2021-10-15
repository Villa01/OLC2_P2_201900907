
from Structure.AST.Node import Node
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Structure.Interfaces.Instruction import Instruction
from Structure.Interfaces.Expression import Expression

class ReturnStructure (Instruction):

    def __init__(self, exp: Expression, line: int, column : int) -> None:
        super().__init__()
        self.exp = exp
        self.line = line
        self.column = column

    def ejecutar(self, driver: Driver, ts: SymbolTable):
        
        if self.exp:
            return self.exp.getValue(driver, ts)
        else:
            return self

    def traverse(self):
        padre = Node("RETURN","")

        padre.AddHijo("return","")

        if self.exp:
            padre.AddHijo(self.exp.traverse())
        
        return padre
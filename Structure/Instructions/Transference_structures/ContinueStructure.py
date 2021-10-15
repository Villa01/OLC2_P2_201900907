
from Structure.AST.Node import Node
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Structure.Interfaces.Instruction import Instruction

class ContinueStructure (Instruction):
    
    def __init__(self) -> None:
        pass

    def ejecutar(self, driver: Driver, ts: SymbolTable):
        return self

    def traverse(self):
        padre = Node("continue","")
        return padre

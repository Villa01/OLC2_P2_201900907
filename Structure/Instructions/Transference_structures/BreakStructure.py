
from Structure.AST.Node import Node
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Structure.Interfaces.Instruction import Instruction

class BreakStructure (Instruction):
    
    def __init__(self) -> None:
        pass

    def ejecutar(self, driver: Driver, ts: SymbolTable):
        return self

    def traverse(self):
        padre = Node("break","")
        return padre

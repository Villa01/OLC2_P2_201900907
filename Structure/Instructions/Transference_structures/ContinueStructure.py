
from Structure.AST.Node import Node
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Structure.Interfaces.Instruction import Instruction
from Temporal import Temporal


class ContinueStructure (Instruction):
    
    def __init__(self) -> None:
        pass

    def ejecutar(self, driver: Driver, ts: SymbolTable):
        return self

    def compilar(self, driver: Driver, symbol_table: SymbolTable, tmp: Temporal):
        if symbol_table.continue_lbl == '':
            driver.agregarError('Continue no esperado', 0, 0)
            return

        tmp.add_goto(symbol_table.continue_lbl)

    def traverse(self):
        padre = Node("continue","")
        return padre

from Structure.AST.Node import Node
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Structure.Interfaces.Instruction import Instruction
from Temporal import Temporal


class BreakStructure(Instruction):

    def __init__(self) -> None:
        pass

    def ejecutar(self, driver: Driver, ts: SymbolTable):
        return self

    def compilar(self, driver: Driver, symbol_table: SymbolTable, tmp: Temporal):
        if symbol_table.break_lbl == '':
            driver.agregarError('Break fuera de un ciclo', 0, 0)
            return
        tmp.add_goto(symbol_table.break_lbl)

    def traverse(self):
        padre = Node("break", "")
        return padre

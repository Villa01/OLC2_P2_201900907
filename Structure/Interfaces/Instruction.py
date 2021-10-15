from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Temporal import Temporal


class Instruction:

    def ejecutar(self, driver: Driver, ts: SymbolTable):
        pass

    def compilar(self, driver: Driver, symbol_table: SymbolTable, tmp: Temporal):
        pass

    def traverse(self):
        pass

import sys

from Structure.SymbolTable.Type import Types

sys.path.append('../')

from Structure.SymbolTable.Symbol import Symbol


class SymbolTable:

    def __init__(self, prev, env) -> None:
        self.prev = prev
        self.table = {}
        self.env = env
        self.size = 0
        self.break_lbl = ''
        self.continue_lbl = ''
        self.return_lbl = ''

    def add(self, idd: str, symbol: Symbol):
        symbol.position = self.size
        symbol.in_heap = symbol.symbol_type == Types.STRING or symbol.symbol_type == Types.STRUCT
        symbol.is_global = self.prev is None
        self.table[idd] = symbol
        self.size += 1

    def add_func(self, idd: str, symbol: Symbol):
        symbol.position = self.size
        self.table[idd] = symbol

    def get_size(self):
        return self.size

    def exist(self, idd: str) -> bool:
        ts = self
        while ts is not None:
            exist = ts.table.get(idd)

            if exist is not None:
                return True

            ts = ts.prev
        return False

    def existsInActual(self, idd: str) -> bool:
        ts = self

        exist = ts.table.get(idd)

        if exist is not None:
            return True

        return False

    def getSymbol(self, idd: str) -> Symbol:
        ts = self
        while ts is not None:
            exist = ts.table.get(idd)

            if exist is not None:
                return exist

            ts = ts.prev

        return None

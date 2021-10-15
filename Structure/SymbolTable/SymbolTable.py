import sys

sys.path.append('../')

from Structure.SymbolTable.Symbol import Symbol


class SymbolTable:

    def __init__(self, prev, env) -> None:
        self.prev = prev
        self.table = {}
        self.env = env

    def add(self, id: str, symbol: Symbol):
        self.table[id] = symbol

    def exist(self, id: str) -> bool:
        ts = self
        while ts is not None:
            exist = ts.table.get(id)

            if exist is not None:
                return True

            ts = ts.prev
        return False

    def existsInActual(self, id: str) -> bool:
        ts = self

        exist = ts.table.get(id)

        if exist is not None:
            return True

        return False

    def getSymbol(self, id: str):
        ts = self
        while ts != None:
            exist = ts.table.get(id)

            if exist != None:
                return exist

            ts = ts.prev

        return None

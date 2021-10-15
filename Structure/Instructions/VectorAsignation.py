
from Structure.Interfaces.Expression import Expression
from Structure.Interfaces.Instruction import Instruction
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable

class VectorAsignation(Instruction):

    def __init__(self, id: str, indexes : list, value: Expression, line, column) -> None:
        super().__init__()
        self.id = id
        self.indexes = indexes
        self.value = value
        self.line = line
        self.column = column

    def ejecutar(self, driver: Driver, ts: SymbolTable):

        indexes_values = []
        for e in self.indexes:
            indexes_values.append(e.getValue(driver, ts)-1)

        array =  ts.getSymbol(self.id).value
        self.getVectorValue(array, indexes_values, driver, ts)

        ts.getSymbol(self.id).value = array


    def getVectorValue(self, l:list, indexes : list, driver, st):
        return self.getVectorValueR(l, indexes, driver, st)

    def getVectorValueR(self, l : list, indexes : list, driver, st):
        
        if len(indexes) == 1:
            if len(l) >= indexes[0]:
                l[indexes[0]] = self.value
        else: 
            cont = 0
            for i in l:
                val = i.getValue(driver, st)
                if type(val) == list and cont == indexes[0]:
                    self.getVectorValueR(val, indexes[1:], driver, st)
                cont += 1
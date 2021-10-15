from Structure.AST.Node import Node
from Structure.Interfaces.Expression import Expression
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Structure.SymbolTable.Type import Types


class VectorAccess (Expression):

    def __init__(self, id : str, indexes : list, line: int, column : int) -> None:
        super().__init__()
        self.id = id
        self.indexes = indexes
        self.line = line
        self.column = column

    def getType(self, driver: Driver, ts):
        value = self.getValue(driver, ts)

        if type(value) == float:
            return Types.FLOAT64
        elif type(value) == int:
            return Types.INT64
        elif type(value) == str and len(value)==1:
            return Types.CHAR
        elif type(value) == str and len(value)>1:
            return Types.STRING
        elif type(value) == bool :
            return Types.BOOL
        elif type(value) == list:
            return Types.ARRAY
        elif type(value) == range:
            return Types.RANGE

    def getValue(self, driver: Driver, st : SymbolTable):
        
        exist = st.getSymbol(self.id)
        indexes_values = []
        for e in self.indexes:
            indexes_values.append(e.getValue(driver, st)-1)

        if exist != None:
            vector = exist.value

            value = self.getVectorValue(vector, indexes_values, driver, st)

            if value:
                return value.getValue(driver, st)
            else:
                driver.agregarError(f'No se pudo obtener la posicion requerida del vector', 0, 0)
        else:
            driver.agregarError(f'No se ha definido el vector', 0, 0)

    def getVectorValue(self, l:list, indexes : list, driver, st):
        return self.getVectorValueR(l, indexes, driver, st)

    def getVectorValueR(self, l : list, indexes : list, driver, st):
        
        if len(indexes) == 1:
            if len(l) >= indexes[0]:
                return l[indexes[0]]
            else:
                return None
        else: 
            cont = 0
            for i in l:
                val = i.getValue(driver, st)
                if type(val) == list and cont == indexes[0]:
                    r = self.getVectorValueR(val, indexes[1:], driver, st)
                    if r != None:
                        return r
                cont += 1
                
    def traverse(self):
        padre = Node("VECTOR", "")

        padre.AddHijo(Node(self.id, ""))
        for index in self.indexes:
            padre.AddHijo("[","")
            padre.AddHijo(index.traverse())
            padre.AddHijo("]","")

        return padre
    

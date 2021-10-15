
from Structure.AST.Node import Node
from Structure.Interfaces.Expression import Expression
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Structure.SymbolTable.Type import Types

class TypeRange(Expression):

    def __init__(self, inf : Expression, sup : Expression, line, column) -> None:
        super().__init__()
        self.inf = inf
        self.sup = sup
        self.line = line
        self.column = column

    def getType(self, driver: Driver, symbolTable: SymbolTable):
        return Types.RANGE

    def getValue(self, driver: Driver, symbolTable: SymbolTable):
        
        inf_value = self.inf.getValue(driver, symbolTable)
        inf_type = self.inf.getType(driver, symbolTable)
        sup_value = self.sup.getValue(driver, symbolTable)
        sup_type = self.sup.getType(driver, symbolTable)

        if inf_type == Types.INT64 :
            if sup_type == Types.INT64:
                return range(inf_value, sup_value +1)
            else : 
                driver.agregarError(f'El límite inferior debe ser de tipo entero', self.line, self.column)
        else : 
            driver.agregarError(f'El límite superior debe ser de tipo entero', self.line, self.column)

    def traverse(self):
        padre = Node("RANGE", "")

        padre.AddHijo(self.inf.traverse())
        padre.AddHijo(Node(":",""))
        padre.AddHijo(self.sup.traverse())
        return padre

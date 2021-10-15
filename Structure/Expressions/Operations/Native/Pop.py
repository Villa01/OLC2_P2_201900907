
from Structure.AST.Node import Node
from Structure.Interfaces.Instruction import Instruction
from Structure.Interfaces.Expression import Expression
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Types


class Pop (Expression, Instruction):

    def __init__(self, exp : Expression, line : int, column : int) -> None:
        super().__init__()
        self.exp = exp
        self.line = line
        self.column = column

    def getType(self, driver: Driver, ts : SymbolTable):
        value = self.getValue(driver, ts)

        if type(value) == float:
            return Types.FLOAT64
        elif type(value) == int:
            return Types.INT64
        elif type(value) == str and len(value)> 1:
            return Types.STRING
        elif type(value) == str and len(value) < 1: 
            return Types.CHAR  
        elif type(value) == bool: 
            return Types.BOOL  
        elif type(value) == range:
            return Types.RANGE
        elif type(value) == list: 
            return Types.ARRAY
        else:
            return Types.NOTHING

    def getValue(self, driver: Driver, ts : SymbolTable):
        exp_value = self.exp.getValue(driver, ts)


        if type(exp_value) == str or type(exp_value) == list:
            return exp_value.pop().getValue(driver, ts)
        else: 
            driver.agregarError(f'No se puede usar pop con la expresion dada.', self.line, self.column)

    def ejecutar(self, driver: Driver, ts: SymbolTable):
        self.getValue(driver, ts)


    def traverse(self):
        padre = Node("POP","")
        padre.AddHijo(Node("pop",""))
        padre.AddHijo(Node("(",""))
        padre.AddHijo(self.exp.traverse())
        padre.AddHijo(Node(")",""))

        return padre

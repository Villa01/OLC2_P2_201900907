

from Structure.AST.Node import Node
from Structure.SymbolTable.Symbol import Symbol
from Structure.Interfaces.Expression import Expression
from Structure.Interfaces.Instruction import Instruction
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Types


class Push (Instruction):

    def __init__(self, exp : Expression, exp2: Expression, line : int, column : int) -> None:
        super().__init__()
        self.exp = exp
        self.exp2 = exp2
        self.line = line
        self.column = column
        self.id = id

    def ejecutar(self, driver: Driver, ts: SymbolTable):
        
        value_exp1 = self.exp.getValue(driver, ts)
        

        if(type(value_exp1) == list):
            value_exp1.append(self.exp2)
            new_symbol = Symbol(1, Types.ARRAY, self.exp.id, value_exp1, None, False)
            ts.add(self.exp.id, new_symbol)
        else:
            driver.agregarError(f'No se puede usar push con la expresion dada.', self.line, self.column)


    def traverse(self):
        padre = Node("PUSH","")
        padre.AddHijo(Node("push",""))
        padre.AddHijo(Node("(",""))
        padre.AddHijo(self.exp.traverse())
        padre.AddHijo(Node(",",""))
        padre.AddHijo(self.exp2.traverse())
        padre.AddHijo(Node(")",""))

        return padre

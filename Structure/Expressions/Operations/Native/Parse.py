from Structure.AST.Node import Node
from Structure.Instructions.Transference_structures.Return import Return
from Structure.Interfaces.Expression import Expression
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Type, Types
from Temporal import Temporal


class Parse(Expression):

    def __init__(self, exp: Expression, t: Type, line: int, column: int) -> None:
        super().__init__()
        self.exp = exp
        self.line = line
        self.column = column
        self.t = t

    def getType(self, driver: Driver, ts: SymbolTable):
        return self.t.type

    def getValue(self, driver: Driver, ts: SymbolTable):
        exp_value = self.exp.getValue(driver, ts)

        if type(exp_value) == str:
            if self.t.type == Types.INT64:
                try:
                    return int(exp_value)
                except ValueError:
                    # TODO: agregar error semantico
                    pass
            elif self.t.type == Types.FLOAT64:
                try:
                    return float(exp_value)
                except ValueError:
                    # TODO: agregar error semantico
                    pass
            else:
                driver.agregarError(f'Solo se admiten los valores enteros en el argumento de parse', self.line,
                                    self.column)

        else:
            driver.agregarError(f'Solo se admiten los valores string en la expresion de la funcion Parse', self.line,
                                self.column)

    def compilar(self, driver: Driver, symbol_table: SymbolTable, tmp: Temporal) -> Return:
        pass

    def traverse(self):
        padre = Node("PARSE", "")
        padre.AddHijo(Node("parse", ""))
        padre.AddHijo(Node("(", ""))
        padre.AddHijo(self.exp.traverse())
        padre.AddHijo(Node(",", ""))
        padre.AddHijo(Node(self.t.stype, ""))
        padre.AddHijo(Node(")", ""))

        return padre

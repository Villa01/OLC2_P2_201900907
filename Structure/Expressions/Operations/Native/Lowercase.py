from Structure.AST.Node import Node
from Structure.Instructions.Transference_structures.Return import Return
from Structure.Interfaces.Expression import Expression
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Types
from Temporal import Temporal


class Lowercase(Expression):

    def __init__(self, exp: Expression, line: int, column: int) -> None:
        super().__init__()
        self.exp = exp
        self.line = line
        self.column = column

    def getType(self, driver: Driver, ts: SymbolTable):
        return Types.STRING

    def getValue(self, driver: Driver, ts: SymbolTable):
        exp_value = self.exp.getValue(driver, ts)

        if type(exp_value) == str:
            return exp_value.lower()
        else:
            driver.agregarError(f'Solo se admiten los valores string en la funcion lower', self.line, self.column)

    def compilar(self, driver: Driver, symbol_table: SymbolTable, tmp: Temporal) -> Return:
        value = self.exp.compilar(driver, symbol_table, tmp)

        if value.type == Types.STRING:
            tmp.flowercase()
            tmp_param = tmp.new_temp()
            tmp.add_exp(tmp_param, tmp.P, symbol_table.size + 1, '+')
            tmp.set_stack(tmp_param, value.value)
            tmp.new_env(symbol_table.size)
            tmp.llamar_func('lowercase')
            ret = tmp.new_temp()
            tmp.get_stack(ret, tmp.P)
            tmp.ret_env(symbol_table.size)

            return Return(ret, Types.STRING, True)
        else:
            driver.agregarError(f'Solo se admiten los valores string en la funcion lower', self.line, self.column)
            return value

    def traverse(self):
        padre = Node("LOWERCASE", "")
        padre.AddHijo(Node("lowercase", ""))
        padre.AddHijo(Node("(", ""))
        padre.AddHijo(self.exp.traverse())
        padre.AddHijo(Node(")", ""))

        return padre

from Structure.AST.Node import Node
from Structure.Instructions.Transference_structures.Return import Return
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Structure.Interfaces.Instruction import Instruction
from Structure.Interfaces.Expression import Expression
from Structure.SymbolTable.Type import Types
from Temporal import Temporal


class ReturnStructure(Instruction):

    def __init__(self, exp: Expression, line: int, column: int) -> None:
        super().__init__()
        self.exp = exp
        self.line = line
        self.column = column
        self.true_label = ''
        self.false_label = ''

    def ejecutar(self, driver: Driver, ts: SymbolTable):

        if self.exp:
            return self.exp.getValue(driver, ts)
        else:
            return self

    def compilar(self, driver: Driver, symbol_table: SymbolTable, tmp: Temporal):
        if symbol_table.return_lbl == '':
            driver.agregarError('Return fuera de funcion', self.line, self.column)
            return
        value = self.exp.compilar(driver, symbol_table, tmp)

        if value.type == Types.BOOL:
            tmp_lbl = tmp.new_label()

            tmp.imprimir_label(value.true_lbl)
            tmp.set_stack(tmp.P, '1')
            tmp.add_goto(tmp_lbl)

            tmp.imprimir_label(value.false_lbl)
            tmp.set_stack(tmp.P, '0')
            tmp.imprimir_label(tmp_lbl)
        else:
            tmp.set_stack(tmp.P, value.value)
        tmp.add_goto(symbol_table.return_lbl)

        return Return(value.value, value.type, False)

    def traverse(self):
        padre = Node("RETURN", "")

        padre.AddHijo("return", "")

        if self.exp:
            padre.AddHijo(self.exp.traverse())

        return padre

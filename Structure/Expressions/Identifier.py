from Structure.AST.Node import Node
from Structure.Instructions.Transference_structures.Return import Return
from Structure.Interfaces.Expression import Expression
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Structure.SymbolTable.Type import Types
from Temporal import Temporal


class Identifier(Expression):

    def __init__(self, id: str, line: int, column: int) -> None:
        self.id = id
        self.line = line
        self.column = column

    def getType(self, driver: Driver, ts: SymbolTable):

        temp_sym = ts.getSymbol(self.id)

        if temp_sym is not None:
            try:
                return temp_sym.symbol_type.type
            except:
                return temp_sym.symbol_type

    def getValue(self, driver: Driver, ts: SymbolTable):
        temp_sym = ts.getSymbol(self.id)

        if temp_sym is not None:
            return temp_sym.value

        else:
            driver.agregarError(f'No se pudo encontrar el simbolo: {self.id}', self.line, self.column)

    def compilar(self, driver: Driver, symbol_table: SymbolTable, tmp: Temporal) -> Return:
        var = symbol_table.getSymbol(self.id)
        if var is None:
            driver.agregarError('La variable no ha sido inicializada', self.line, self.column)
            return
        t = None
        try:
            t = var.symbol_type.type
        except AttributeError:
            t = var.symbol_type


        temp = tmp.new_temp()
        temp_pos = var.position
        if not var.is_global:
            temp_pos = tmp.new_temp()
            tmp.add_exp(temp_pos, tmp.P, var.position, '+')
        tmp.get_stack(temp, temp_pos)

        if var.symbol_type != Types.BOOL:
            return Return(temp, t, True)
        self.checkLabels(tmp)

        tmp.add_if(temp, '==', '1', self.true_label)
        tmp.add_goto(self.false_label)

        ret = Return(None, Types.BOOL, False)
        ret.true_lbl = self.true_label
        ret.false_lbl = self.false_label
        return ret

    def traverse(self):
        padre = Node("ID", "")
        padre.AddHijo(Node(self.id, ""))

        return padre

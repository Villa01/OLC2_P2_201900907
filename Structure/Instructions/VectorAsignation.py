from Structure.Instructions.Transference_structures.Return import Return
from Structure.Interfaces.Expression import Expression
from Structure.Interfaces.Instruction import Instruction
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Types, Type
from Temporal import Temporal


class VectorAsignation(Instruction):

    def __init__(self, id: str, indexes: list, value: Expression, line, column) -> None:
        super().__init__()
        self.id = id
        self.indexes = indexes
        self.value = value
        self.line = line
        self.column = column

    def ejecutar(self, driver: Driver, ts: SymbolTable):

        indexes_values = []
        for e in self.indexes:
            indexes_values.append(e.getValue(driver, ts) - 1)

        array = ts.getSymbol(self.id).value
        self.getVectorValue(array, indexes_values, driver, ts)

        ts.getSymbol(self.id).value = array

    def compilar(self, driver: Driver, symbol_table: SymbolTable, tmp: Temporal):
        tmp.add_comment("Inicio asignacion vector")
        var = symbol_table.getSymbol(self.id)
        cont = 0
        temp_pos = var.position
        for indice in self.indexes:
            cont += 1
            ind_val = indice.compilar(driver, symbol_table, tmp)

            t = None
            try:
                t = var.symbol_type.type
            except:
                t = var.symbol_type

            pos_heap = None
            if cont == 1:
                pos_heap = tmp.new_temp()
            else:
                pos_heap = temp_pos

            if cont == 1:
                if not var.is_global:
                    temp_pos = tmp.new_temp()
                    tmp.add_exp(temp_pos, tmp.P, var.position, '+')
                tmp.get_stack(pos_heap, temp_pos)

            pos_valor = tmp.new_temp()
            tmp.add_exp(pos_valor, pos_heap, ind_val.value, '+')
            tmp.add_exp(pos_valor, pos_valor, 1, '+')

            # TODO: verificacion dinamica

            if cont == len(self.indexes):
                valor = self.value.compilar(driver, symbol_table, tmp)
                tmp.set_heap(pos_valor, valor.value)
            else:
                temp = tmp.new_temp()
                tmp.get_heap(temp, pos_valor)
                temp_pos = temp

        tmp.add_comment("Fin asignacion vector")

    def getVectorValue(self, l: list, indexes: list, driver, st):
        return self.getVectorValueR(l, indexes, driver, st)

    def getVectorValueR(self, l: list, indexes: list, driver, st):

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

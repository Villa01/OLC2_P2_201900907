from Structure.AST.Node import Node
from Structure.Instructions.Transference_structures.Return import Return
from Structure.Interfaces.Expression import Expression
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Structure.SymbolTable.Type import Types
from Temporal import Temporal


class VectorAccess(Expression):

    def __init__(self, id: str, indexes: list, line: int, column: int) -> None:
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
        elif type(value) == str and len(value) == 1:
            return Types.CHAR
        elif type(value) == str and len(value) > 1:
            return Types.STRING
        elif type(value) == bool:
            return Types.BOOL
        elif type(value) == list:
            return Types.ARRAY
        elif type(value) == range:
            return Types.RANGE

    def getValue(self, driver: Driver, st: SymbolTable):

        exist = st.getSymbol(self.id)
        indexes_values = []
        for e in self.indexes:
            indexes_values.append(e.getValue(driver, st) - 1)

        if exist is not None:
            vector = exist.value

            value = self.getVectorValue(vector, indexes_values, driver, st)

            if value:
                return value.getValue(driver, st)
            else:
                driver.agregarError(f'No se pudo obtener la posicion requerida del vector', 0, 0)
        else:
            driver.agregarError(f'No se ha definido el vector', 0, 0)

    def getVectorValue(self, l: list, indexes: list, driver, st):
        return self.getVectorValueR(l, indexes, driver, st)

    def getVectorValueR(self, l: list, indexes: list, driver, st):

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

    def compilar(self, driver: Driver, symbol_table: SymbolTable, tmp: Temporal):
        if symbol_table.return_lbl == '':
            symbol_table.return_lbl = tmp.new_label()
        tmp.add_comment("Inicio acceso a vector")
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

            # Verificacion Dinamica
            true_lbl = tmp.new_label()
            false_lbl = tmp.new_label()
            temp = tmp.new_temp()
            tmp.get_heap(temp, pos_heap)
            tmp.add_if(ind_val.value, '>=', temp, true_lbl)
            tmp.add_goto(false_lbl)

            tmp.imprimir_label(true_lbl)
            tmp.print_cadena("Index out of bounds")
            tmp.add_goto(symbol_table.return_lbl)

            tmp.imprimir_label(false_lbl)

            tmp.add_exp(pos_valor, pos_valor, 1, '+')

            if cont == len(self.indexes):
                valor = pos_valor
                tmp.get_heap(pos_valor, valor)

                #tmp.imprimir_label(symbol_table.return_lbl)
                tmp.add_comment("Fin acceso vector")

                return Return(valor, t, True)
            else:
                temp = tmp.new_temp()
                tmp.get_heap(temp, pos_valor)
                temp_pos = temp

    def traverse(self):
        padre = Node("VECTOR", "")

        padre.AddHijo(Node(self.id, ""))
        for index in self.indexes:
            padre.AddHijo("[", "")
            padre.AddHijo(index.traverse())
            padre.AddHijo("]", "")

        return padre

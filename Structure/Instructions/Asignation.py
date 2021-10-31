from Structure.Expressions.Identifier import Identifier
from Structure.AST.Node import Node
from Structure.Instructions.Transference_structures.Return import Return
from Structure.Interfaces.Instruction import Instruction
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Type, Types, get_type
from Structure.SymbolTable.Symbol import Symbol
from Temporal import Temporal


class Asignation(Instruction):

    def __init__(self, id: str, variable: Symbol, t: Type, env: str, line: int, column: int) -> None:
        super().__init__()
        self.id = id
        self.variable = variable
        self.line = line
        self.column = column
        self.type = t
        self.env = env

    def ejecutar(self, driver: Driver, ts: SymbolTable):
        var_value = None
        var_type = None

        if self.variable is not None:
            var_value = self.variable.value.getValue(driver, ts)
            var_type = self.variable.value.getType(driver, ts)

        if self.type is not None:
            # Si trae un tipo definido verificar que sea el mismo tipo que la variable
            if self.type.type == var_type:
                # Si trae un tipo definido y es el mismo que la variable agregar a la tabla de simbolos

                if self.env == 'global':
                    if ts.exist(self.id):
                        ts.getSymbol(self.id).setValue(var_value)
                    else:
                        new_symbol = Symbol(1, self.type, self.id, var_value, None, False)
                        ts.add(self.id, new_symbol)
                else:
                    if ts.existsInActual(self.id):
                        ts.getSymbol(self.id).setValue(var_value)
                    else:
                        new_symbol = Symbol(1, self.type, self.id, var_value, None, False)
                        ts.add(self.id, new_symbol)
            else:
                t = get_type(var_value)
                driver.agregarError(f'No hay conversion entre {self.type.stype} y {t.stype}.', self.line, self.column)
        # Sino agregar a la tabla de simbolos
        else:
            t = get_type(var_value)

            if self.env == 'global':
                if ts.exist(self.id):
                    ts.getSymbol(self.id).setValue(var_value)
                else:
                    new_symbol = Symbol(1, t, self.id, var_value, None, False)
                    ts.add(self.id, new_symbol)
            elif self.env == 'local':
                if ts.existsInActual(self.id):
                    ts.getSymbol(self.id).setValue(var_value)
                else:
                    new_symbol = Symbol(1, t, self.id, var_value, None, False)
                    ts.add(self.id, new_symbol)

            else:
                if ts.exist(self.id):
                    ts.getSymbol(self.id).setValue(var_value)
                else:
                    new_symbol = Symbol(1, t, self.id, var_value, None, False)
                    ts.add(self.id, new_symbol)

    def compilar(self, driver: Driver, symbol_table: SymbolTable, tmp: Temporal):

        val: Return = self.variable.value.compilar(driver, symbol_table, tmp)

        if not symbol_table.exist(self.id):
            symbol_table.add(self.id, Symbol(1, self.type, self.id, val.value, None, False))

        new_var = symbol_table.getSymbol(self.id)

        if not val.type == Types.ARRAY:
            new_var.symbol_type = val.type

        tmp_pos = new_var.position
        if not new_var.is_global:
            tmp_pos = tmp.new_temp()
            tmp.add_exp(tmp_pos, tmp.P, new_var.position, '+')

        if val.type == Types.BOOL:
            tmp_lbl = tmp.new_label()

            tmp.imprimir_label(val.true_lbl)
            tmp.set_stack(tmp_pos, '1')

            tmp.add_goto(tmp_lbl)

            tmp.imprimir_label(val.false_lbl)
            tmp.set_stack(tmp_pos, '0')

            tmp.imprimir_label(tmp_lbl)
        else:
            # tmp.save_string_heap(val.value, symbol_table.size)
            tmp.set_stack(tmp_pos, val.value)

    def traverse(self):
        padre = Node("ASIGNACION", "")

        padre.AddHijo(Node(self.id, ""))
        padre.AddHijo(Node(" = ", ""))
        padre.AddHijo(self.variable.value.traverse())

        return padre

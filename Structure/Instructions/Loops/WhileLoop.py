from Structure.AST.Node import Node
from Structure.Instructions.Transference_structures.ReturnStructure import ReturnStructure
from Structure.Instructions.Transference_structures.ContinueStructure import ContinueStructure
from Structure.Instructions.Transference_structures.BreakStructure import BreakStructure
from Structure.Interfaces.Instruction import Instruction
from Structure.Interfaces.Expression import Expression
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Types
from Temporal import Temporal


class WhileLoop(Instruction):

    def __init__(self, condition: Expression, ins_list, line, column) -> None:
        super().__init__()
        self.condition = condition
        self.ins_list = ins_list
        self.line = line
        self.column = column

    def ejecutar(self, driver: Driver, ts: SymbolTable):

        if self.condition.getType(driver, ts) == Types.BOOL:
            while self.condition.getValue(driver, ts):
                ts_local = SymbolTable(ts, "WHILE")
                driver.agregarTabla(ts_local)
                for ins in self.ins_list:
                    res = ins.ejecutar(driver, ts_local)

                    if isinstance(ins, BreakStructure) or isinstance(res, BreakStructure):
                        return res
                    elif isinstance(ins, ReturnStructure) or isinstance(res, ReturnStructure):
                        return res
                    elif isinstance(ins, ContinueStructure) or isinstance(res, ContinueStructure):
                        break
                else:
                    pass
                continue
        else:
            driver.agregarError(f'La condicion del while debe ser del tipo bool', self.line, self.column)

    def compilar(self, driver: Driver, symbol_table: SymbolTable, tmp: Temporal):
        continue_lbl = tmp.new_label()
        tmp.imprimir_label(continue_lbl)

        condition = self.condition.compilar(driver, symbol_table, tmp)

        # Agregar un nuevo entorno
        ts_local = SymbolTable(symbol_table, "WHILE")
        driver.agregarTabla(ts_local)
        ts_local.break_lbl = condition.false_lbl
        ts_local.continue_lbl = continue_lbl
        if symbol_table.return_lbl == '':
            symbol_table.return_lbl = tmp.new_label()
        ts_local.return_lbl = symbol_table.return_lbl

        tmp.imprimir_label(condition.true_lbl)

        for ins in self.ins_list:
            ins.compilar(driver, ts_local, tmp)
        tmp.add_goto(continue_lbl)

        tmp.imprimir_label(condition.false_lbl)

    def traverse(self):
        padre = Node("WHILE", "")

        padre.AddHijo(Node("while", ""))
        padre.AddHijo(self.condition.traverse())

        if self.ins_list and len(self.ins_list) > 0:
            hijo_ins = Node("INSTRUCCIONES", "")

            for ins in self.ins_list:
                hijo_ins.AddHijo(ins.traverse())
            padre.AddHijo(hijo_ins)

        padre.AddHijo(Node("end", ""))
        return padre

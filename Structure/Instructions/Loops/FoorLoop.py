from Structure.AST.Node import Node
from Structure.Instructions.Transference_structures.ReturnStructure import ReturnStructure
from Structure.Instructions.Transference_structures.BreakStructure import BreakStructure
from Structure.Instructions.Transference_structures.ContinueStructure import ContinueStructure
from Structure.SymbolTable.Symbol import Symbol
from Structure.Interfaces.Instruction import Instruction
from Structure.Interfaces.Expression import Expression
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Types, Type
from Temporal import Temporal


class FoorLoop(Instruction):

    def __init__(self, id: str, iterable: Expression, list_inst: list, line: int, column: int) -> None:
        super().__init__()
        self.id = id
        self.iterable = iterable
        self.list_ins = list_inst
        self.line = line
        self.column = column

    def ejecutar(self, driver: Driver, ts: SymbolTable):
        iterable_type = self.iterable.getType(driver, ts)

        if iterable_type == Types.ARRAY or iterable_type == Types.STRING or iterable_type == Types.RANGE:
            iterable_value = self.iterable.getValue(driver, ts)

            for i in iterable_value:
                ts_local = SymbolTable(ts, "ITERACION FOR")
                # Se agrega la variable 
                var_value = None
                if type(i) == str or type(i) == int:
                    var_value = i
                else:
                    var_value = i.getValue(driver, ts)

                t = None
                if type(var_value) == float:
                    t = Type("FLOAT64")
                elif type(var_value) == int:
                    t = Type("INT64")
                elif type(var_value) == str:
                    t = Type("STRING")
                elif type(var_value) == bool:
                    t = Type("BOOL")
                elif type(var_value) == list:
                    t = Type("ARRAY")
                elif type(var_value) == range:
                    t = Type("RANGE")
                else:
                    t = Type("NOTHING")

                if ts_local.exist(self.id):
                    ts_local.getSymbol(self.id).setValue(var_value)
                else:
                    new_symbol = Symbol(1, t, self.id, var_value, None, False)
                    ts_local.add(self.id, new_symbol)

                driver.agregarTabla(ts_local)

                for ins in self.list_ins:
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

    def compilar(self, driver: Driver, symbol_table: SymbolTable, tmp: Temporal):
        pass

    def traverse(self):
        padre = Node("FOR", "")

        padre.AddHijo(Node("for", ""))
        padre.AddHijo(Node(self.id, ""))
        padre.AddHijo(Node("in", ""))
        padre.AddHijo(self.iterable.traverse())

        if self.list_ins and len(self.list_ins) > 0:
            hijo_ins = Node("INSTRUCCIONES", "")

            for ins in self.list_ins:
                hijo_ins.AddHijo(ins.traverse())
            padre.AddHijo(hijo_ins)

        padre.AddHijo(Node("end", ""))
        return padre

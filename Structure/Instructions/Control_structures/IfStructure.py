from Structure.AST.Node import Node
from Structure.Instructions.Transference_structures.ReturnStructure import ReturnStructure
from Structure.Instructions.Transference_structures.ContinueStructure import ContinueStructure
from Structure.Instructions.Transference_structures.BreakStructure import BreakStructure
from Structure.Interfaces.Instruction import Instruction
from Structure.Interfaces.Expression import Expression
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Types

class IfStructure (Instruction):

    def __init__(self, condition: Expression, if_ins, else_ins, line, column) -> None:
        super().__init__()
        self.condition = condition
        self.if_ins = if_ins
        self.else_ins = else_ins
        self.line = line
        self.column = column

    def ejecutar(self, driver: Driver, ts : SymbolTable):
        local_ts = SymbolTable(ts, "IF")

        condition_value = self.condition.getValue(driver, ts)
        if self.condition.getType(driver, ts) == Types.BOOL:
            if condition_value:
                for ins in self.if_ins:
                    res = ins.ejecutar(driver, local_ts)

                    if isinstance(ins, BreakStructure) or isinstance(res, BreakStructure):
                        return res
                    elif isinstance(ins, ContinueStructure) or isinstance(res, ContinueStructure):
                        return res
                    elif isinstance(ins, ReturnStructure) or isinstance(res, ReturnStructure):
                        return res

            else:
                for ins in self.else_ins:
                    res = ins.ejecutar(driver, local_ts)

                    if isinstance(ins, BreakStructure) or isinstance(res, BreakStructure):
                        return res
                    elif isinstance(ins, ContinueStructure) or isinstance(res, ContinueStructure):
                        return res
                    elif isinstance(ins, ReturnStructure) or isinstance(res, ReturnStructure):
                        return res

            driver.agregarTabla(local_ts)

    def traverse(self):
        padre = Node("IF","")

        padre.AddHijo(Node("if",""))
        padre.AddHijo(self.condition.traverse())

        if self.if_ins and len(self.if_ins) > 0:
            hijo_if = Node("INSTRUCCIONES","")

            for ins in self.if_ins:
                hijo_if.AddHijo(ins.traverse())

            padre.AddHijo(hijo_if)

        if self.else_ins and len(self.else_ins) > 0:
            hijo_else = Node("INSTRUCCIONES","")

            for ins in self.if_ins:
                hijo_else.AddHijo(ins.traverse())

            padre.AddHijo(hijo_else)
        padre.AddHijo(Node("end",""))

        return padre
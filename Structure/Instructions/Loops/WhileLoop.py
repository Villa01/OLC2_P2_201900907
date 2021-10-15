
from Structure.AST.Node import Node
from Structure.Instructions.Transference_structures.ReturnStructure import ReturnStructure
from Structure.Instructions.Transference_structures.ContinueStructure import ContinueStructure
from Structure.Instructions.Transference_structures.BreakStructure import BreakStructure
from Structure.Interfaces.Instruction import Instruction
from Structure.Interfaces.Expression import Expression
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Types


class WhileLoop (Instruction):

    def __init__(self, condition : Expression, ins_list, line, column) -> None:
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


    def traverse(self):
        padre = Node("WHILE", "")

        padre.AddHijo(Node("while",""))
        padre.AddHijo(self.condition.traverse())

        if self.list_ins and len(self.list_ins)>0:
            hijo_ins = Node("INSTRUCCIONES","")

            for ins in self.list_ins:
                hijo_ins.AddHijo(ins.traverse())
            padre.AddHijo(hijo_ins)

        padre.AddHijo(Node("end",""))
        return padre

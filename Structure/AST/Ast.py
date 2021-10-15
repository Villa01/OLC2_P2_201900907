from Structure.AST.Node import Node
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Structure.Instructions.Functions import Function
from Structure.Interfaces.Instruction import Instruction
from Temporal import Temporal


class Ast:

    def __init__(self, instruction_list) -> None:
        self.instruction_list = instruction_list

    def ejecutar(self, driver: Driver, ts: SymbolTable):
        for ins in self.instruction_list:
            if isinstance(ins, Function):
                ins.addFunctionSymbol(driver, ts)

        for ins in self.instruction_list:
            if not isinstance(ins, Function):
                ins.ejecutar(driver, ts)

    def compilar(self, driver, st, tmp: Temporal):
        for ins in self.instruction_list:
            ins.compilar(driver, st, tmp)

        driver.console += tmp.get_code()

    def traverse(self):
        raiz = Node("INICIO", "")

        for ins in self.instruction_list:
            raiz.AddHijo(ins.traverse())

        return raiz

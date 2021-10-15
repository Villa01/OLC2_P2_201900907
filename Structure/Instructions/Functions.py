from Structure.AST.Node import Node
from Structure.Interfaces.Instruction import Instruction
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Type, Types
from Structure.SymbolTable.Symbol import Symbol

class Function (Symbol, Instruction):

    def __init__(self, symbol: int, symbol_type: Type, identifier: str, value, param_list, method, ins_list, line, column) -> None:
        super().__init__(symbol, symbol_type, identifier, value, param_list, method)
        self.ins_list = ins_list
        self.line = line
        self.column = column
    
    def addFunctionSymbol(self, driver:Driver, st: SymbolTable):
        if not st.exist(self.identifier):
            st.add(self.identifier, self)
        else:
            driver.agregarError(f'No se encontró {self.identifier}', self.line, self.column)

    def ejecutar(self, driver: Driver, ts: SymbolTable):
        ts_local = SymbolTable(ts, 'Funcion ' + self.identifier)
        for ins in self.ins_list:
            res = ins.ejecutar(driver, ts_local)

            if res != None:
                driver.agregarTabla(ts_local)
                return res

        
        driver.agregarTabla(ts_local)
        return None

    def traverse(self):
        padre = Node("FUNCION","")
        padre.AddHijo(Node("function",""))
        padre.AddHijo(Node(self.identifier,""))
        padre.AddHijo(Node("(",""))

        if len(self.param_list) >0:
            hijo_param = Node("PARAMETROS","")
            for param in self.param_list:
                hijo_param.AddHijo(Node(param.traverse()))
            padre.AddHijo(hijo_param)
        padre.AddHijo(Node(")",""))

        padre.AddHijo(Node("end",""))

        return padre

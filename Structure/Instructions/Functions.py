from Structure.AST.Node import Node
from Structure.Interfaces.Instruction import Instruction
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Type, Types
from Structure.SymbolTable.Symbol import Symbol
from Temporal import Temporal


class Function(Symbol, Instruction):

    def __init__(self, symbol: int, symbol_type: Type, identifier: str, value, param_list, method, ins_list, line,
                 column) -> None:
        super().__init__(symbol, symbol_type, identifier, value, param_list, method)
        self.ins_list = ins_list
        self.line = line
        self.column = column

    def addFunctionSymbol(self, driver: Driver, st: SymbolTable):
        if not st.exist(self.identifier):
            st.add(self.identifier, self)
        else:
            driver.agregarError(f'No se encontró {self.identifier}', self.line, self.column)

    def ejecutar(self, driver: Driver, ts: SymbolTable):
        ts_local = SymbolTable(ts, 'Funcion ' + self.identifier)
        for ins in self.ins_list:
            res = ins.ejecutar(driver, ts_local)

            if res is not None:
                driver.agregarTabla(ts_local)
                return res

        driver.agregarTabla(ts_local)
        return None

    def compilar(self, driver: Driver, symbol_table: SymbolTable, tmp: Temporal):
        self.addFunctionSymbol(driver, symbol_table)
        ts_local = SymbolTable(symbol_table, 'Funcion ' + self.identifier)
        return_lbl = tmp.new_temp()
        ts_local.size = 1
        ts_local.return_lbl = return_lbl

        for param in self.param_list:
            ts_local.add(param.identifier, param)

        tmp.addBeginFunc(self.identifier)

        try:
            for ins in self.ins_list:
                ins.compilar(driver, symbol_table, tmp)
        except:
            driver.agregarError(f'Error al compilar instrucciones de {self.identifier}', self.line, self.column)

        tmp.add_comment('Goto para que go no de error')
        tmp.add_goto(return_lbl)
        tmp.imprimir_label(return_lbl)
        tmp.addEndFunc()

    def traverse(self):
        padre = Node("FUNCION", "")
        padre.AddHijo(Node("function", ""))
        padre.AddHijo(Node(self.identifier, ""))
        padre.AddHijo(Node("(", ""))

        if len(self.param_list) > 0:
            hijo_param = Node("PARAMETROS", "")
            for param in self.param_list:
                hijo_param.AddHijo(Node(param.traverse()))
            padre.AddHijo(hijo_param)
        padre.AddHijo(Node(")", ""))

        padre.AddHijo(Node("end", ""))

        return padre

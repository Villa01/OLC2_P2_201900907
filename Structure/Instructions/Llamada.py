from Structure.AST.Node import Node
from Structure.Instructions.Functions import Function
from Structure.Instructions.Transference_structures.Return import Return
from Structure.Interfaces.Instruction import Instruction
from Structure.Interfaces.Expression import Expression
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Type, Types
from Structure.SymbolTable.Symbol import Symbol
from Temporal import Temporal


class Llamada(Instruction, Expression):

    def __init__(self, id: str, param_list, line, column) -> None:
        super().__init__()
        self.id = id
        self.param_list = param_list
        self.line = line
        self.column = column

    def getType(self, driver: Driver, symbolTable: SymbolTable):
        value: Function = symbolTable.getSymbol(self.id)
        return value.symbol_type.type

    def getValue(self, driver: Driver, symbolTable):
        value = self.ejecutar(driver, symbolTable)
        return value

    def ejecutar(self, driver: Driver, ts: SymbolTable):

        ts_local = SymbolTable(ts, 'Llamada a ' + self.id)

        func_simb = ts_local.getSymbol(self.id)

        func_param = func_simb.param_list
        # TODO: verificar los parametros
        names = []
        for symb in func_param:
            names.append(symb.identifier)

        cont = 0
        for param in self.param_list:
            t = param.getType(driver, ts)
            if t == Types.INT64:
                t = Type("INT64")
            elif t == Types.FLOAT64:
                t = Type("FLOAT64")
            elif t == Types.BOOL:
                t = Type("BOOL")
            elif t == Types.CHAR:
                t = Type("CHAR")
            elif t == Types.STRING:
                t = Type("STRING")
            elif t == Types.RANGE:
                t = Type("RANGE")
            elif t == Types.ARRAY:
                t = Type("ARRAY")
            else:
                t = Type("NOTHING")

            val = param.getValue(driver, ts)
            new_symbol = Symbol(6, t, names[cont], val, None, False)
            ts_local.add(names[cont], new_symbol)
            cont += 1

        res = func_simb.ejecutar(driver, ts_local)

        if res is not None:
            return res
        else:
            return None

    def compilar(self, driver: Driver, symbol_table: SymbolTable, tmp: Temporal):

        func = symbol_table.getSymbol(self.id)
        if func is not None:
            param_values = []

            size = symbol_table.size
            cont = 0
            for param in func.param_list:
                t = self.param_list[cont].getType(driver, symbol_table)
                if t == Types.INT64:
                    t = Type("INT64")
                elif t == Types.FLOAT64:
                    t = Type("FLOAT64")
                elif t == Types.BOOL:
                    t = Type("BOOL")
                elif t == Types.CHAR:
                    t = Type("CHAR")
                elif t == Types.STRING:
                    t = Type("STRING")
                elif t == Types.RANGE:
                    t = Type("RANGE")
                elif t == Types.ARRAY:
                    t = Type("ARRAY")
                else:
                    t = Type("NOTHING")
                param.symbol_type = t
                value = self.param_list[cont].getValue(driver, symbol_table)
                ret_valu = param.compilar(driver, symbol_table, tmp)
                ret_valu.value = value
                param_values.append(ret_valu)
                symbol_table.add(param.identifier, param)
                cont += 1
            temp = tmp.new_temp()

            tmp.add_exp(temp, tmp.P, size + 1, '+')
            aux = 0
            for param in param_values:
                aux += 1
                tmp.set_stack(temp, param.value)
                if aux != len(param_values):
                    tmp.add_exp(temp, temp, '1', '+')
            tmp.new_env(size)
            tmp.llamar_func(self.id)
            tmp.get_stack(temp, tmp.P)
            tmp.ret_env(size)

            return Return(temp, func.symbol_type, True)
        else:
            # STRUCT
            pass

    def traverse(self):
        padre = Node("Llamada", "")
        padre.AddHijo(Node(self.identificador, ""))
        padre.AddHijo(Node("(", ""))

        if self.param_list.length > 0:
            hijo_param = Node("PARAMETROS", "")

            for param in self.param_list:
                hijo_param.AddHijo(param.recorrer())
            padre.AddHijo(hijo_param)

        padre.AddHijo(Node(")", ""))

        return padre

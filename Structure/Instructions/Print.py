from Structure.AST.Node import Node
from Structure.Interfaces.Instruction import Instruction
from Structure.Interfaces.Expression import Expression
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Types
from Temporal import Temporal


class Print(Instruction):

    def __init__(self, exps: Expression, line: int, column: int, n: bool) -> None:
        super().__init__()
        self.exps = exps
        self.line = line
        self.column = column
        self.n = n

    def ejecutar(self, driver: Driver, ts: SymbolTable):

        value_list = []
        for exp in self.exps:
            value = exp.getValue(driver, ts)
            value_list.append(value)

        for value in value_list:
            if type(value) == int or type(value) == float or type(value) == str or type(value) == bool:
                driver.append(str(value))
            elif type(value) == list:
                driver.append(str("["))
                driver.append(self.printArray(value, driver, ts))
                driver.append(str("]"))
            elif value is None:
                driver.append("None")
        if self.n:
            driver.append("\n")

    def compilar(self, driver: Driver, symbol_table: SymbolTable, tmp: Temporal):
        for exp in self.exps:
            valor = exp.compilar(driver, symbol_table, tmp)
            val = exp.getValue(driver, symbol_table)
            t = exp.getType(driver, symbol_table)

            if t == Types.INT64:
                tmp.append_code(f'fmt.Printf("%d", int({valor}));\n')
            elif t == Types.FLOAT64:
                tmp.add_print("f", valor)
            elif t == Types.BOOL:
                if val:
                    tmp.print_true()
                else:
                    tmp.print_false()
            elif t == Types.STRING:
                tmp.new_temp()
                param_temp = tmp.get_temp()

                tmp.add_assing(param_temp, tmp.H)

                # tmp.add_exp(param_temp, 'p', 1, '+')
                # tmp.add_exp(param_temp, param_temp, 1, '+')
                for letra in valor:
                    tmp.set_heap(tmp.H, ord(letra))
                    tmp.add_exp(tmp.H, tmp.H, 1, '+')

                tmp.set_heap(tmp.H, -1)

                # cambio de entorno
                tmp.new_temp()
                temp_env = tmp.get_temp()
                tmp.add_exp(temp_env, tmp.P, symbol_table.size,'+')
                tmp.add_exp(temp_env, temp_env, 1, '+')
                tmp.set_stack(temp_env, param_temp)

                tmp.new_env(symbol_table.size)
                tmp.fPrintString()
                tmp.llamar_func('print_string')
                tmp.ret_env(symbol_table.size)

                tmp.new_temp()
                temporal = tmp.get_temp()
                tmp.get_stack(temporal, 'p')

        if self.n:
            tmp.add_print('c', 10)

    def traverse(self):
        padre = Node("Print", "");
        padre.AddHijo(Node("print", ""));
        padre.AddHijo(Node("(", ""));

        hijo = Node("EXPRESIONES", "");
        for exp in self.exps:
            hijo.AddHijo(exp.traverse())

        padre.AddHijo(hijo);
        padre.AddHijo(Node(")", ""));

        return padre

    def printArray(self, l: list, driver, st):
        text = ""
        for i in l:
            i = i.getValue(driver, st)
            if type(i) == list:
                text += "["
                text += self.printArray(i, driver, st) + " "
                text += "]"
            else:
                text += str(i) + " "

        return text

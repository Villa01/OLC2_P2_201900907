from Structure.AST.Node import Node
from Structure.Instructions.Transference_structures.Return import Return
from Structure.Interfaces.Instruction import Instruction
from Structure.Interfaces.Expression import Expression
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Types, Type
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
            ret: Return = exp.compilar(driver, symbol_table, tmp)
            valor = ret.value

            t = ret.type
            if isinstance(t, Type):
                t = ret.type.type

            if t == Types.INT64:
                tmp.append_code(f'fmt.Printf("%d", int({valor}));\n')
            elif t == Types.FLOAT64:
                tmp.add_print("f", valor)
            elif t == Types.BOOL:
                temp_label = tmp.new_label()
                tmp.imprimir_label(ret.true_lbl)
                tmp.print_true()

                tmp.add_goto(temp_label)

                tmp.imprimir_label(ret.false_lbl)
                tmp.print_false()

                tmp.imprimir_label(temp_label)

            elif t == Types.STRING:
                tmp.fPrintString()

                param_tmp = tmp.new_temp()

                tmp.add_exp(param_tmp, tmp.P, symbol_table.size, '+')
                tmp.add_exp(param_tmp, param_tmp, '1', '+')
                tmp.set_stack(param_tmp, valor)

                tmp.new_env(symbol_table.size)
                tmp.llamar_func('print_string')

                temp = tmp.new_temp()
                tmp.get_stack(temp, tmp.P)
                tmp.ret_env(symbol_table.size)

            elif t == Types.NOTHING:
                tmp.print_cadena('Nothing')

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

from Structure.AST.Node import Node
from Structure.Instructions.Transference_structures.Return import Return
from Structure.Interfaces.Expression import Expression
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Structure.SymbolTable.Type import Types


class Primitive(Expression):

    def __init__(self, primitive, line: int, column: int) -> None:
        self.primitive = primitive
        self.line = line
        self.column = column

    def getType(self, driver: Driver, ts: SymbolTable):
        value = self.getValue(driver, ts)

        if type(value) == float:
            return Types.FLOAT64
        elif type(value) == int:
            return Types.INT64
        elif type(value) == str:
            return Types.STRING
        elif type(value) == bool:
            return Types.BOOL
        elif type(value) == list:
            return Types.ARRAY
        elif type(value) == range:
            return Types.RANGE

    def getValue(self, driver: Driver, ts: SymbolTable):
        return self.primitive

    def compilar(self, driver, st, tmp):
        exp_type = self.getType(driver, st)
        exp_value = self.getValue(driver, st)
        if exp_type == Types.INT64 or exp_type == Types.FLOAT64:
            return Return(str(exp_value), exp_type, False)
        elif exp_type == Types.BOOL:
            if self.true_label == '':
                self.true_label = tmp.new_label()
            if self.false_label == '':
                self.false_label = tmp.new_label()

            if exp_value:
                tmp.add_goto(self.true_label)
                tmp.add_comment('Goto para evitar el error de go')
                tmp.add_goto(self.false_label)
            else:
                tmp.add_goto(self.false_label)
                tmp.add_comment('Goto para evitar el error de go')
                tmp.add_goto(self.true_label)

            ret = Return(exp_value, exp_type, False)
            ret.true_lbl = self.true_label
            ret.false_lbl = self.false_label

            return ret

        elif exp_type == Types.STRING:
            ret_temp = tmp.new_temp()
            tmp.add_exp(ret_temp, tmp.H, '', '')

            for letra in str(exp_value):
                tmp.set_heap(tmp.H, ord(letra))
                tmp.aumentar_heap()
            tmp.set_heap(tmp.H, '-1')
            tmp.aumentar_heap()
            return Return(ret_temp, Types.STRING, True)
        else:
            # TODO: agregar tipos necesarios
            pass

    def traverse(self):
        padre = Node("Primitivo", "")
        pr = self.primitive
        if not type(self.primitive) == str:
            pr = str(pr)
        padre.AddHijo(Node(pr, ""))

        return padre

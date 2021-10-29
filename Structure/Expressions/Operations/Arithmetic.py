import sys

from Structure.AST.Node import Node
from Structure.Expressions.Identifier import Identifier
from Structure.Instructions.Llamada import Llamada
from Structure.Instructions.Transference_structures.Return import Return
from Structure.SymbolTable.Symbol import Symbol
from Temporal import Temporal

sys.path.append('../')

from Structure.Expressions.Operations.Operations import Operation, Operator, getStringOperator
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Types
from Structure.Driver import Driver
from Structure.Interfaces.Expression import Expression


class Arithmetic(Operation, Expression):
    """Manages all the aritmethic operations
       Parameters
        ----------
        exp1: Expression 
            first operand
        operator: string
                the string of an operator
        exp2: Expression 
            second operand
        line: number
            line where it was obtained
        column : number
            position where it was obtained
        expU : Expression
            If there is an unary expression this is it.
    """

    def __init__(self, exp1: Expression, operator: Operator, exp2: Expression, line: int, column: int,
                 expU: Expression) -> None:
        Operation.__init__(self=self, exp1=exp1, operator=operator, exp2=exp2, line=line, column=column, expU=expU)

    def getType(self, driver: Driver, ts: SymbolTable):
        value = self.getValue(driver, ts)

        if type(value) == float:
            return Types.FLOAT64
        elif type(value) == int:
            return Types.INT64
        elif type(value) == str and len(value) > 1:
            return Types.STRING
        elif type(value) == str and len(value) < 1:
            return Types.CHAR
        elif type(value) == bool:
            return Types.BOOL
        elif type(value) == range:
            return Types.RANGE
        elif type(value) == list:
            return Types.ARRAY

    def getValue(self, driver: Driver, ts: SymbolTable):

        valor_exp1 = None
        valor_exp2 = None
        valor_expU = None

        if not self.expU:
            valor_exp1 = self.exp1.getValue(driver, ts)
            valor_exp2 = self.exp2.getValue(driver, ts)
        else:
            valor_expU = self.exp1.getValue(driver, ts)

        # Sum
        if self.Operator == Operator.SUM:
            # int64 or float64
            if type(valor_exp1) == int or type(valor_exp1) == float:
                # int64 + int64 or float64 + float64
                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 + valor_exp2
                else:
                    driver.agregarError(f'No se admite la suma con los tipos definidos', self.line, self.column)
            else:
                driver.agregarError(f'No se admite la suma con los tipos definidos', self.line, self.column)
        # Substraction   
        elif self.Operator == Operator.SUBS:
            # int64 or float64
            if type(valor_exp1) == int or type(valor_exp1) == float:
                # int64 - int64 or float64 - float64
                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 - valor_exp2
                else:
                    driver.agregarError(f'No se admite la resta con los tipos definidos', self.line, self.column)
            else:
                driver.agregarError(f'No se admite la resta con los tipos definidos', self.line, self.column)
        # Multiplication
        elif self.Operator == Operator.MULT:
            # int64 or float64
            if type(valor_exp1) == int or type(valor_exp1) == float:
                # int64 - int64 or float64 - float64
                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 * valor_exp2
                else:
                    driver.agregarError(f'No se admite la multiplicacion con los tipos definidos', self.line,
                                        self.column)
            # string 
            if type(valor_exp1) == str:
                # string * string 
                if type(valor_exp2) == str:
                    return valor_exp1 + valor_exp2
                else:
                    driver.agregarError(f'No se admite la multiplicacion con los tipos definidos', self.line,
                                        self.column)
            else:
                driver.agregarError(f'No se admite la multiplicacion con los tipos definidos', self.line, self.column)
        # Division
        elif self.Operator == Operator.DIV:
            # int64 or float64
            if type(valor_exp1) == int or type(valor_exp1) == float:
                # int64 - int64 or float64 / float64
                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 / valor_exp2
                else:
                    driver.agregarError(f'No se admite la division con los tipos definidos', self.line, self.column)
            else:
                driver.agregarError(f'No se admite la division con los tipos definidos', self.line, self.column)
        elif self.Operator == Operator.POT:
            # int64 or float64
            if type(valor_exp1) == int or type(valor_exp1) == float:
                # int64 - int64 or float64 / float64
                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 ** valor_exp2
                else:
                    driver.agregarError(f'No se admite la potencia con los tipos definidos', self.line, self.column)
            # string 
            if type(valor_exp1) == str:
                # string ^ int
                if type(valor_exp2) == int:
                    return valor_exp1 * valor_exp2
                else:
                    driver.agregarError(f'No se admite la potencia con los tipos definidos', self.line, self.column)
            else:
                # TODO: agregar error semantico
                pass
        elif self.Operator == Operator.MOD:
            # int64 or float64
            if type(valor_exp1) == int or type(valor_exp1) == float:
                # int64 - int64 or float64 / float64
                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 % valor_exp2
                else:
                    driver.agregarError(f'No se admite el modulo con los tipos definidos', self.line, self.column)
            else:
                driver.agregarError(f'No se admite el modulo con los tipos definidos', self.line, self.column)

        elif self.Operator == Operator.UNARY:
            if type(valor_expU) == int or type(valor_expU) == float:
                return -valor_expU
            else:
                driver.agregarError(f'No se admite el complemento aritmetico con los tipos definidos', self.line,
                                    self.column)
        else:
            driver.agregarError(f'No se admite la operacion', self.line, self.column)

    def compilar(self, driver, ts: SymbolTable, tmp: Temporal):

        left_value = self.exp1.compilar(driver, ts, tmp)
        # Guardar temporales
        pos = 0
        if not self.expU:
            if isinstance(self.exp2, Llamada) and isinstance(self.exp1, Identifier):
                tmp.add_comment('Guardado de temporales')
                tmp_g = tmp.new_temp()
                symbol: Symbol = ts.getSymbol(self.exp1.id)
                pos = symbol.position
                tmp.add_exp(tmp_g, tmp.P, symbol.position, '+')
                tmp.set_stack(tmp_g, left_value.value)
                tmp.add_comment('Fin guardado de temporales')

        if not self.expU:
            right_value = self.exp2.compilar(driver, ts, tmp)

        # Recuperar temporales
        if not self.expU:
            if isinstance(self.exp2, Llamada) and isinstance(self.exp1, Identifier):
                tmp.add_comment('Recuperando de temporales')
                tmp_g = tmp.new_temp()
                tmp.add_exp(tmp_g, tmp.P, pos, '+')
                tmp.get_stack(left_value.value, tmp_g)
                tmp.add_comment('Fin guardado de temporales')

        temp = tmp.new_temp()
        op = getStringOperator(self.Operator)

        if self.Operator == Operator.POT:

            if left_value.type == Types.STRING and right_value.type == Types.INT64:

                tmp.add_comment("Inicio repeticion")
                tmp_palabra = left_value.value
                # Obtener tamaño del string

                tmp.fSizeString()
                tmp_param = tmp.new_temp()
                tmp.add_exp(tmp_param, tmp.P, ts.size + 1, '+')
                tmp.set_stack(tmp_param, tmp_palabra)

                tmp.new_env(ts.size)
                tmp.llamar_func('sizeString')
                tmp_size = tmp.new_temp()
                tmp.get_stack(tmp_size, tmp.P)
                tmp.ret_env(ts.size)

                tmp_cont = tmp.new_temp()

                tmp_apunt = tmp.new_temp()
                tmp.add_exp(tmp_apunt, tmp_palabra, '', '')

                tmp_iter = tmp.new_temp()
                tmp.add_exp(tmp_iter, 0, '', '')

                true_iter_lbl = tmp.new_label()
                false_iter_lbl = tmp.new_label()

                lbl_iter = tmp.new_label()
                tmp.imprimir_label(lbl_iter)

                tmp.add_exp(tmp_cont, 0, '', '')    # t1 = 0

                tmp_comp = tmp.new_temp()
                tmp.add_exp(tmp_comp, right_value.value, 1, '-')
                tmp.add_if(tmp_iter, '<', tmp_comp, true_iter_lbl)
                tmp.add_goto(false_iter_lbl)

                tmp.imprimir_label(true_iter_lbl)

                tmp_cont_pal = tmp.new_temp()
                tmp.add_exp(tmp_cont_pal, tmp_palabra, '', '')   # t_cont_pal = t_pal
                tmp.add_exp(tmp_apunt, tmp_apunt, tmp_size, '+')

                lbl_loop = tmp.new_label()
                tmp.imprimir_label(lbl_loop)  # L1:

                true_lbl = tmp.new_label()
                false_lbl = tmp.new_label()

                tmp.add_if(tmp_cont, '<', tmp_size, true_lbl)  # if t1 < t0 {goto L2;}
                tmp.add_goto(false_lbl)     # goto L3;

                tmp.imprimir_label(true_lbl)    # L2:

                tmp_val = tmp.new_temp()
                tmp.get_heap(tmp_val, tmp_cont_pal)     # t_val = heap[t_cont_pal]

                tmp.set_heap(tmp_apunt, tmp_val)    # heap[t_apunt] = t_val

                tmp.add_exp(tmp_apunt, tmp_apunt, 1, '+')   # t_apunt = t_apunt + 1
                tmp.add_exp(tmp_cont, tmp_cont, 1, '+')     # t_cont = t_cont + 1
                tmp.add_exp(tmp_cont_pal, tmp_cont_pal, 1, '+')     # t_cont = t_cont + 1

                tmp.add_goto(lbl_loop)

                tmp.imprimir_label(false_lbl)
                tmp.add_exp(tmp_iter, tmp_iter, 1, '+')
                tmp.add_goto(lbl_iter)
                tmp.imprimir_label(false_iter_lbl)

                tmp.set_heap(tmp_apunt, -1)

                tmp.add_comment("Fin repeticion")
                return Return(tmp_palabra, Types.STRING, True)

            tmp.fPotencia()
            param_temp = tmp.new_temp()

            tmp.add_exp(param_temp, tmp.P, ts.get_size(), '+')
            tmp.add_exp(param_temp, param_temp, '1', '+')
            tmp.set_stack(param_temp, left_value.value)

            tmp.add_exp(param_temp, param_temp, '1', '+')
            tmp.set_stack(param_temp, right_value.value)

            tmp.new_env(ts.get_size())
            tmp.llamar_func('potencia')

            temp = tmp.new_temp()
            tmp.get_stack(temp, tmp.P)
            tmp.ret_env(ts.get_size())

            return Return(temp, Types.INT64, True)
        else:
            if not self.expU:
                if op == '/' or op == '%':
                    fine_lbl = tmp.new_label()
                    error_lbl = tmp.new_label()
                    salida = tmp.new_label()

                    tmp.add_if(right_value.value, '!=', 0, fine_lbl)
                    tmp.add_goto(error_lbl)

                    tmp.imprimir_label(error_lbl)
                    tmp.print_cadena("Math Error")
                    tmp.add_exp(temp, 0, '', '')
                    tmp.add_goto(salida)

                    tmp.imprimir_label(fine_lbl)

                    if op == '%':
                        tmp.add_exp(temp, f'math.Mod({left_value.value},{right_value.value})', '', '')
                        tmp.add_import("math")
                    else:
                        tmp.add_exp(temp, left_value.value, right_value.value, op)

                    tmp.imprimir_label(salida)
                else:
                    if op == '*' and left_value.type == Types.STRING and right_value.type == Types.STRING:
                        # Concatenacion de cadenas
                        tmp.add_comment('Inicio concatencacion')

                        tmp_par1 = tmp.new_temp()
                        tmp.add_exp(tmp_par1, tmp.P, 1, '+')
                        tmp.add_exp(tmp_par1, tmp_par1, ts.size, '+')
                        tmp.set_stack(tmp_par1, left_value.value)

                        tmp_par2 = tmp.new_temp()
                        tmp.add_exp(tmp_par2, tmp.P, 2, '+')
                        tmp.add_exp(tmp_par2, tmp_par2, ts.size, '+')
                        tmp.set_stack(tmp_par2, right_value.value)

                        tmp.fConcatenar()

                        tmp.new_env(ts.size)
                        tmp.llamar_func('concatenar')
                        dir_ret = tmp.new_temp()
                        tmp.add_exp(dir_ret, tmp.P, 0, '+')
                        ret = tmp.new_temp()
                        tmp.get_stack(ret, dir_ret)
                        tmp.ret_env(ts.size)
                        tmp.add_comment('Fin concatencacion')
                        return Return(ret, Types.STRING, True)
                    else:
                        tmp.add_exp(temp, left_value.value, right_value.value, op)
            else:
                tmp.add_exp(temp, 0, left_value.value, '-')
            return Return(temp, Types.INT64, True)

    def traverse(self):
        padre = Node("Exp", "")
        temp = Operation(None, None, None, None, None, None)
        sOp = getStringOperator(self.Operator)
        if self.expU:
            padre.AddHijo(Node(sOp, ""))
            padre.AddHijo(self.exp1.traverse())
        else:
            padre.AddHijo(self.exp1.traverse())
            padre.AddHijo(Node(sOp, ""))
            padre.AddHijo(self.exp2.traverse())

        return padre

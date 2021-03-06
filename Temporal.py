class Temporal:
    tmp = 0
    lbl = 0
    P = 'p'
    H = 'h'

    def __init__(self) -> None:
        self.code = ''
        self.temporales = []
        self.imports = ['fmt']
        self.funcs = ''
        self.natives = ''
        self.inFunc = False
        self.inNatives = False

        # Lista de Nativas
        self.printString = False
        self.potencia = False
        self.parse = False
        self.concatenar = False
        self.sizeString = False
        self.lowercase = False
        self.uppercase = False

    def add_comment(self, comment):
        self.append_code(f'/* {comment} */\n')

    def add_import(self, imp):
        if imp not in self.imports:
            self.imports.append(imp)

    # funciones para temporales

    def new_temp(self):
        self.tmp += 1
        self.temporales.append(self.get_temp())
        return self.get_temp()

    def get_temp(self):
        return f't{self.tmp}'

    # Funciones para labels

    def new_label(self):
        self.lbl += 1
        return self.get_label()

    def get_label(self):
        return f'L{self.lbl}'

    def imprimir_label(self, label):
        self.append_code(f'{label}:\n')

    def get_header(self):
        header = '/*----HEADER----*/\npackage main;\n\nimport ('
        for imp in self.imports:
            header += f'\n\t"{imp}"'
        header += '\n);\n\n'
        if self.tmp > 0:
            header += 'var '
            cont = 0
            for temp in self.temporales:
                header += temp
                if cont != self.tmp - 1:
                    header += " ,"
                cont += 1
            header += " float64 ;\n"

        header += f"var {self.P}, {self.H} float64;\nvar stack [30101999]float64;\nvar heap [30101999]float64;\n\n"

        return header

    def get_code(self):
        return f'{self.get_header()}{self.natives}\n{self.funcs}\nfunc main(){{\n{self.code}\n}}'

    def append_code(self, code, tab='\t'):
        if self.inNatives:
            if self.natives == '':
                self.natives = self.natives + '/*-----NATIVES-----*/\n'
            self.natives = self.natives + tab + code
        elif self.inFunc:
            if self.funcs == '':
                self.funcs = self.funcs + '/*-----FUNCS-----*/\n'
            self.funcs = self.funcs + tab + code
        else:
            self.code = self.code + '\t' + code

    def add_exp(self, result, left, right, op):
        self.append_code(f'{result}={left}{op}{right};\n')

    def add_assing(self, result, exp):
        self.append_code(f'{result}={exp}\n;')

    def add_print(self, t, value):
        self.append_code(f'fmt.Printf("%{t}", {value});\n')

    def print_true(self):
        self.add_print("c", 116)
        self.add_print("c", 114)
        self.add_print("c", 117)
        self.add_print("c", 101)

    def print_false(self):
        self.add_print("c", 102)
        self.add_print("c", 97)
        self.add_print("c", 108)
        self.add_print("c", 115)
        self.add_print("c", 101)

    def print_cadena(self, palabra):
        for letra in palabra:
            self.add_print("c", ord(letra))

    def addBeginFunc(self, nombre):
        if not self.inNatives:
            self.inFunc = True
        self.append_code(f'func {nombre}(){{\n', '')

    def addEndFunc(self):
        self.append_code('return;\n}\n')

    # Funciones para manejar el stack
    def set_stack(self, pos, value):
        self.append_code(f'stack[int({pos})]={value};\n')

    def get_stack(self, place, pos):
        self.append_code(f'{place}=stack[int({pos})];\n')

    # Entoros
    def new_env(self, size):
        self.append_code(f'{self.P}={self.P}+{size};\n')

    def llamar_func(self, name):
        self.append_code(f'{name}();\n')

    def ret_env(self, size):
        self.append_code(f'{self.P}={self.P}-{size};\n')

    # Funciones para manejar el heap

    def set_heap(self, pos, value):
        self.append_code(f'heap[int({pos})]={value};\n')

    def get_heap(self, place, pos):
        self.append_code(f'{place}=heap[int({pos})];\n')

    def aumentar_heap(self):
        self.append_code(f'{self.H}={self.H}+1;\n')

    # Sentencias de control
    def add_if(self, op1, operator, op2, label):
        self.append_code(f'if {op1} {operator} {op2} {{goto {label};}}\n')

    def add_goto(self, label):
        self.append_code(f'goto {label};\n')

    def save_string_heap(self, palabra, size):
        tmp_h = self.new_temp()
        self.add_exp(tmp_h, self.H, '', '')

        for letra in palabra:
            self.set_heap(self.H, 'rune(letra)')
            self.add_exp(self.H, self.H, 1, '+')

        self.set_stack(size, tmp_h)

    def fparse(self):
        if self.parse:
            return
        self.parse = True
        self.inNatives = True

        self.addBeginFunc('parse')

        return_lbl = self.new_label()

    # Funciones Nativas
    def fPrintString(self):

        if self.printString:
            return
        self.printString = True
        self.inNatives = True

        self.addBeginFunc('print_string')

        self.new_label()
        return_lbl = self.get_label()
        self.new_label()
        fin_cadena = self.get_label()

        # Temporal para puntero de la pila
        self.new_temp()
        tmp_p = self.get_temp()

        # Temporal para puntero de la heap
        self.new_temp()
        tmp_h = self.get_temp()

        # Agregando el parametro para el procedimiento
        self.add_exp(tmp_p, self.P, '1', '+')

        self.get_stack(tmp_h, tmp_p)

        # temporal para comparar
        self.new_temp()
        tmp_c = self.get_temp()

        self.imprimir_label(fin_cadena)

        self.get_heap(tmp_c, tmp_h)

        self.add_if(tmp_c, '==', '-1', return_lbl)

        self.add_print('c', f'int({tmp_c})')
        self.add_exp(tmp_h, tmp_h, '1', '+')

        self.add_goto(fin_cadena)
        self.imprimir_label(return_lbl)
        self.addEndFunc()

        self.inNatives = False

    def flowercase(self):
        if self.lowercase:
            return
        self.inNatives = True
        self.lowercase = True

        self.addBeginFunc('lowercase')

        ret = self.get_temp()
        self.add_exp(ret, self.H, '', '')

        dir_param = self.new_temp()
        self.add_exp(dir_param, self.P, '1', '+')
        tmp_param = self.new_temp()
        self.get_stack(tmp_param, dir_param)

        loop_lbl = self.new_label()
        true_lbl = self.new_label()
        false_lbl = self.new_label()

        self.imprimir_label(loop_lbl)

        tmp_letra = self.new_temp()

        self.get_heap(tmp_letra, tmp_param)

        self.add_if(tmp_letra, '!=', -1, true_lbl)
        self.add_goto(false_lbl)

        self.imprimir_label(true_lbl)

        minus_lbl = self.new_label()
        mayus_lbl = self.new_label()
        salir = self.new_label()

        self.add_if(tmp_letra, '<', 97, mayus_lbl)
        self.add_goto(minus_lbl)

        self.imprimir_label(mayus_lbl)
        self.add_exp(tmp_letra, tmp_letra, 32, '+')
        self.add_goto(salir)

        self.imprimir_label(minus_lbl)
        self.add_goto(salir)

        self.imprimir_label(salir)
        self.set_heap(self.H, tmp_letra)
        self.add_exp(self.H, self.H, 1, '+')
        self.add_exp(tmp_param, tmp_param, 1, '+')
        self.add_goto(loop_lbl)

        self.imprimir_label(false_lbl)

        self.set_stack(self.P, ret)
        self.set_heap(self.H, -1)
        self.addEndFunc()
        self.inNatives = False

    def fupperacse(self):
        if self.uppercase:
            return
        self.inNatives = True
        self.uppercase = True

        self.addBeginFunc('uppercase')

        ret = self.get_temp()
        self.add_exp(ret, self.H, '', '')

        dir_param = self.new_temp()
        self.add_exp(dir_param, self.P, '1', '+')
        tmp_param = self.new_temp()
        self.get_stack(tmp_param, dir_param)

        loop_lbl = self.new_label()
        true_lbl = self.new_label()
        false_lbl = self.new_label()

        self.imprimir_label(loop_lbl)

        tmp_letra = self.new_temp()

        self.get_heap(tmp_letra, tmp_param)

        self.add_if(tmp_letra, '!=', -1, true_lbl)
        self.add_goto(false_lbl)

        self.imprimir_label(true_lbl)

        minus_lbl = self.new_label()
        mayus_lbl = self.new_label()
        salir = self.new_label()

        self.add_if(tmp_letra, '>', 96, mayus_lbl)
        self.add_goto(minus_lbl)

        self.imprimir_label(mayus_lbl)
        self.add_exp(tmp_letra, tmp_letra, 32, '-')
        self.add_goto(salir)

        self.imprimir_label(minus_lbl)
        self.add_goto(salir)

        self.imprimir_label(salir)
        self.set_heap(self.H, tmp_letra)
        self.add_exp(self.H, self.H, 1, '+')
        self.add_exp(tmp_param, tmp_param, 1, '+')
        self.add_goto(loop_lbl)

        self.imprimir_label(false_lbl)

        self.set_stack(self.P, ret)
        self.set_heap(self.H, -1)
        self.addEndFunc()
        self.inNatives = False

    def fSizeString(self):
        if self.sizeString:
            return
        self.inNatives = True
        self.sizeString = True

        self.addBeginFunc('sizeString')

        t = self.new_temp()
        self.add_exp(t, self.P, 1, '+')  # t1 = P + 1
        t_param = self.new_temp()
        self.get_stack(t_param, t)  # t2 = stack[t1]
        t_cont = self.new_temp()
        self.add_exp(t_cont, 0, '', '')  # t4 = 0

        lbl_loop = self.new_label()
        self.imprimir_label(lbl_loop)  # L1:

        t_letra = self.new_temp()
        self.get_heap(t_letra, t_param)  # t3 = heap[t2]

        true_lbl = self.new_label()
        false_lbl = self.new_label()

        self.add_if(t_letra, '==', -1, true_lbl)  # if t3 == -1 {goto L2;}
        self.add_goto(false_lbl)  # goto L3;

        self.imprimir_label(false_lbl)  # L3:

        self.add_exp(t_cont, t_cont, 1, '+')  # t4 = t4 + 1
        self.add_exp(t_param, t_param, 1, '+')  # t2 = t2 + 1
        self.add_goto(lbl_loop)  # goto L1;

        self.imprimir_label(true_lbl)  # L3:

        ret = self.new_temp()
        self.add_exp(ret, self.P, 0, '+')  # t5 = P + 0
        self.set_stack(self.P, t_cont)

        self.addEndFunc()
        self.inNatives = False

    def fConcatenar(self):
        if self.concatenar:
            return
        self.concatenar = True
        self.inNatives = True

        self.addBeginFunc('concatenar')

        dir_param1 = self.new_temp()
        self.add_exp(dir_param1, self.P, 1, '+')

        tmp_param1 = self.new_temp()
        self.get_stack(tmp_param1, dir_param1)

        res_pos = self.new_temp()
        self.add_exp(res_pos, self.H, '', '')

        lbl_loop1 = self.new_label()
        self.imprimir_label(lbl_loop1)

        tmp_letra = self.new_temp()
        self.get_heap(tmp_letra, tmp_param1)

        lbl_true = self.new_label()
        lbl_false = self.new_label()

        self.add_if(tmp_letra, '!=', '-1', lbl_true)
        self.add_goto(lbl_false)

        self.imprimir_label(lbl_true)

        self.set_heap(self.H, tmp_letra)
        self.add_exp(self.H, self.H, 1, '+')
        self.add_exp(tmp_param1, tmp_param1, 1, '+')
        self.add_goto(lbl_loop1)

        self.imprimir_label(lbl_false)

        # Segunda palabra
        dir_param2 = self.new_temp()
        self.add_exp(dir_param2, self.P, 2, '+')

        tmp_param2 = self.new_temp()
        self.get_stack(tmp_param2, dir_param2)

        lbl_loop2 = self.new_label()
        self.imprimir_label(lbl_loop2)

        tmp_letra = self.new_temp()
        self.get_heap(tmp_letra, tmp_param2)

        lbl_true = self.new_label()
        lbl_false = self.new_label()

        self.add_if(tmp_letra, '!=', '-1', lbl_true)
        self.add_goto(lbl_false)

        self.imprimir_label(lbl_true)

        self.set_heap(self.H, tmp_letra)
        self.add_exp(self.H, self.H, 1, '+')
        self.add_exp(tmp_param2, tmp_param2, 1, '+')
        self.add_goto(lbl_loop2)

        self.imprimir_label(lbl_false)

        self.set_heap(self.H, -1)

        self.set_stack(self.P, res_pos)

        self.addEndFunc()
        self.inNatives = False

    def fPotencia(self):
        if self.potencia:
            return
        self.potencia = True
        self.inNatives = True

        self.addBeginFunc('potencia')

        t0 = self.new_temp()
        self.add_exp(t0, self.P, '1', '+')

        t1 = self.new_temp()
        self.get_stack(t1, t0)

        self.add_exp(t0, t0, '1', '+')

        t2 = self.new_temp()
        self.get_stack(t2, t0)
        self.add_exp(t0, t1, '', '')

        l0 = self.new_label()
        l1 = self.new_label()

        self.imprimir_label(l0)
        self.add_if(t2, '<=', '1', l1)
        self.add_exp(t1, t1, t0, '*')
        self.add_exp(t2, t2, '1', '-')
        self.add_goto(l0)
        self.imprimir_label(l1)
        self.set_stack(self.P, t1)

        self.addEndFunc()
        self.inNatives = False

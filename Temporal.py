class Temporal:
    tmp = 0
    lbl = 0

    def __init__(self) -> None:
        self.code = ''
        self.temporales = []

    # funciones para temporales

    def new_temp(self):
        self.tmp += 1
        self.temporales.append(self.get_temp())

    def get_temp(self):
        return f't{self.tmp}'

    # Funciones para labels

    def new_label(self):
        self.lbl += 1

    def get_label(self):
        return f'L{self.lbl}'

    def imprimir_label(self, label):
        self.append_code(f'{label}:\n')

    def get_header(self):
        header = '/*----HEADER----*/\npackage main;\n\nimport (\n\t"fmt"\n)\n\n'
        if self.tmp > 0:
            header += 'var '
            cont = 0
            for temp in self.temporales:
                header += temp
                if cont != self.tmp - 1:
                    header += " ,"
                cont += 1
            header += " float64; \n"

        header += "var P, H float64;\nvar stack [30101999]float64;\nvar heap [30101999]float64;\n\n"

        return header

    def get_code(self):
        return f'{self.get_header()}\nfunc main(){{\n{self.code}\n}}'

    def append_code(self, code):
        self.code += f'{code}\n'

    def add_exp(self, result, left, right, op):
        self.append_code(f'{result}={left}{op}{right};\n')

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

    def addComment(self, comment):
        self.append_code(f'/* {comment} */\n')

    def addBeginFunc(self, nombre):
        #if not self.inNatives:
        #    self.inFunc = True
        self.append_code(f'func {nombre}(){{\n')

    def addEndFunc(self):
        self.append_code('return;\n}\n')

    # Funciones para manejar el stack
    def set_stack(self, pos, value):
        self.append_code(f'stack[int({pos})]={value};\n')

    def get_stack(self, place, pos):
        self.append_code(f'{place}=stack[int({pos})];\n')

    # Funciones para manejar el heap

    def set_heap(self, pos, value):
        self.append_code(f'heap[int({pos})]={value};\n')

    def get_heap(self, place, pos):
        self.append_code(f'{place}=heap[int({pos})];\n')

    def aumentar_heap(self):
        self.append_code('H=H+1;\n')

    # Sentencias de control
    def add_if(self, op1, operator, op2, label):
        self.append_code(f'if {op1} {operator} {op2} {{goto {label};}}\n')

    def add_goto(self, label):
        self.append_code(f'goto {label};\n')

    # Funciones Nativas
    def fPrintString(self):
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
        self.add_exp(tmp_p, 'p', '1', '+')

        self.get_stack(tmp_h, tmp_p)

        # temporal para comparar
        self.new_temp()
        tmp_c = self.get_temp()

        self.imprimir_label(fin_cadena)

        self.get_heap(tmp_c, tmp_h)

        self.add_if(tmp_c, '==', '-1', return_lbl)

        self.add_print('c', tmp_c)
        self.add_exp(tmp_h, tmp_h, '1', '+')

        self.add_goto(fin_cadena)
        self.imprimir_label(return_lbl)

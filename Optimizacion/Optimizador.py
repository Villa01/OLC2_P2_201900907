from Optimizacion.Blocks import Blocks
from Optimizacion.Expresiones.Expresion import Expression
from Optimizacion.Gotos.Goto import Goto
from Optimizacion.Gotos.If import If
from Optimizacion.Instructions.Asignacion import Assignment
from Optimizacion.Instructions.Label import Label
from Optimizacion.repOptimizacion import repOptimizacion


class Optimizador:

    def __init__(self, packages, temps, code):
        self.packages = packages
        self.temps = temps
        self.code = code
        self.blocks = []
        self.optimizaciones = []

    def getCode(self):
        ret = f'package main;\n\nimport (\n\t"{self.packages}"\n);\n'
        for temp in self.temps:
            ret = ret + f'var {temp}\n'
        ret = ret + '\n'

        for func in self.code:
            ret = ret + func.getCode() + '\n\n'
        return ret

    def Bloques(self):
        self.blocks = []
        self.GenerarBloques()

        # APLICAR REGLAS A NIVEL LOCAL Y GLOBAL

    def GenerarBloques(self):
        self.GenerarLideres()
        self.CrearBloques()
        self.ConnectBloques()
        print('Prueba')

    def GenerarLideres(self):
        # Por cada funcion
        for func in self.code:
            # La primera instrucción de tres direcciones en el código intermedio es líder
            func.instr[0].isLeader = True

            # Cualquier instrucción que siga justo después de un salto
            # condicional o incondicional es líder
            flag = False
            for instr in func.instr:
                if flag:
                    instr.isLeader = True
                    flag = False
                if type(instr) is Goto or type(instr) is If:
                    flag = True

    def CrearBloques(self):
        # Por cada funcion
        for func in self.code:
            # Bloques de la funcion actual
            blocks = []
            block = None
            for instr in func.instr:
                if instr.isLeader:
                    # Si ya hay un bloque creado. Agregarlo al arreglo de bloques
                    if block is not None:
                        blocks.append(block)
                    block = Blocks(instr)
                block.code.append(instr)
            # EOF
            blocks.append(block)
            # Guardo mis bloques de la funcion
            self.blocks.append(blocks)

    def ConnectBloques(self):
        # Por cada arreglo de bloques en una función
        for func in self.blocks:
            prevBlock = None
            # Por cada bloque en la funcion. Los uniremos en cascada
            for block in func:
                if prevBlock is None:
                    prevBlock = block
                    continue
                prevBlock.nexts.append(block)
                prevBlock = block

            # Revisar saltos entre bloques
            for block in func:
                # Obtener ultima instruccion
                lastIns = block.code[len(block.code) - 1]
                if type(lastIns) is Goto or type(lastIns) is If:
                    label = lastIns.label
                    # Revisando todos los bloques
                    for check in func:
                        if type(check.first) is Label and check.first.id == label:
                            block.nexts.append(check)
                            break

    def Mirilla(self):
        # Por cada funcion
        for func in self.code:
            tamanio = 10

            # Mientras no nos hemos pasado del tamaño (Fin del código)
            while tamanio <= len(func.instr):
                flagOpt = False

                # Darle 5 pasadas al codigo con el tamaño actual
                for i in range(5):
                    aux = 0
                    # Dar una pasada completa
                    while (tamanio + aux) <= len(func.instr):
                        #flagOpt = flagOpt or self.Regla1(func.instr[0 + aux: tamanio + aux])
                        flagOpt = flagOpt or self.Regla3(func.instr[0 + aux: tamanio + aux])
                        flagOpt = flagOpt or self.Regla6(func.instr[0 + aux: tamanio + aux])
                        flagOpt = flagOpt or self.Regla7(func.instr[0 + aux: tamanio + aux])
                        aux = aux + 1

                # Si no hubo optimizacion en la pasada, subir el tamaño
                if not flagOpt:
                    tamanio = tamanio + 20

    def Regla1(self, array):
        ret = False

        for i in range(len(array)):
            print(f'i: {i}')
            actual = array[i]
            cambia = False
            exp_actual = actual.getCode()
            if type(actual) is Assignment:

                for j in range(len(array)):
                    if j <= i:
                        continue
                    comp = array[j]
                    prueba = comp.getCode()
                    if not actual.deleted and not comp.deleted and type(actual) is Assignment and \
                            type(comp) is Assignment and actual is not comp:
                        if comp.place.getCode() == actual.place.getCode():
                            cambia = True
                        if comp.exp.getCode() == actual.place.getCode():
                            optimizado = exp_actual
                            exp_actual += comp.getCode()
                            print(exp_actual)
                            comp.deleted = True
                            self.agregar_optimizacion('Mirilla', 'Regla 2', exp_actual, optimizado, actual.line)
                            exp_actual = ''
                            ret = True
                            cambia = False
        return ret

    def Regla3(self, array):
        ret = False
        for i in range(len(array) - 2):
            actual = array[i]
            if type(actual) is If and not actual.deleted:
                nextIns = array[i + 1]
                if type(nextIns) is Goto and not nextIns.deleted:
                    sigIns = array[i + 2]
                    exp_actual = actual.getCode() + '\n'
                    exp_actual += nextIns.getCode() + '\n'
                    exp_actual += sigIns.getCode()
                    if type(sigIns) is Label and not sigIns.deleted:
                        if sigIns.id == actual.label:
                            actual.condition.getContrary()
                            actual.label = nextIns.label
                            nextIns.deleted = True
                            array[i + 2].deleted = True
                            ret = True
                            optimizada = actual.getCode()
                            self.agregar_optimizacion('Mirilla', 'Regla 3', exp_actual, optimizada, actual.line)
        return ret

    def Regla6(self, array):
        ret = False
        for i in range(len(array)):
            actual = array[i]
            if type(actual) is Assignment and not actual.deleted and isinstance(actual.exp, Expression):
                exp_actual = actual.getCode()
                if actual.selfAssignment():
                    actualOpt = actual.exp.neutralOps()
                    if actualOpt:
                        ret = True
                        actual.deleted = True
                        optimizada = actual.getCode()
                        self.agregar_optimizacion('Mirilla', 'Regla 6', exp_actual, optimizada, actual.exp.line)
        return ret

    def Regla7(self, array):
        ret = False

        for i in range(len(array)):
            actual = array[i]
            if type(actual) is Assignment and not actual.deleted and isinstance(actual.exp, Expression):
                exp_actual = actual.getCode()
                if actual.exp.eliminar_neutros():
                    optimizada = actual.getCode()
                    self.agregar_optimizacion('Mirilla', 'Regla 7', exp_actual, optimizada, actual.exp.line)
                    ret = True
        return ret

    def agregar_optimizacion(self, tipo, regla, original, optimizada, fila):
        opt = repOptimizacion(tipo, regla, original, optimizada, fila)
        self.optimizaciones.append(opt)

    def generar_reporte(self):
        cuerpohtml = " <html><header><title>ReporteTablaSimbolos</title><style>#tabla {font-family:Arial,Helvetica," \
                     "sans-serif;border-collapse:collapse;width:100%;}#tabla  td,#tabla  th{" \
                     "border:1pxsolid#ddd;padding:8px;}#tabla  tr:nth-child(even){background-color:#f2f2f2;}#tabla  " \
                     "tr:hover{background-color:#ddd;}#tabla  th{" \
                     "padding-top:12px;padding-bottom:12px;text-align:left;background-color:#04AA6D;color:white" \
                     ";}</style></header><body> "
        cuerpohtml += " <table id=\"tabla\">"
        cuerpohtml += " <thead>"
        cuerpohtml += "<tr>" + "<td colspan=\"6\">Reporte de optimizacion</td>" + "</tr>" + "<tr>" \
                                                                                            "<th>Tipo de optimizacion</th><th>Regla aplicada</th><th>Expresion original</th>" \
                                                                                            "<th>Expresion optimizada</th><th>Fin</th>"

        for opt in self.optimizaciones:
            cuerpohtml += f'<tr><td>{opt.tipo}</td><td>{opt.regla}</td><td>{opt.expresion_original}</td>' \
                          f'<td>{opt.expresion_optimizada}</td><td>{opt.fila}</td></tr>'

        cuerpohtml += '</body></html>'
        return cuerpohtml

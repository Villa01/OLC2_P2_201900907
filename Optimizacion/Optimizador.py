from Optimizacion.Expresiones.Expresion import Expression
from Optimizacion.Gotos.Goto import Goto
from Optimizacion.Gotos.If import If
from Optimizacion.Instructions.Asignacion import Assignment
from Optimizacion.Instructions.Label import Label


class Optimizador:

    def __init__(self, packages, temps, code):
        self.packages = packages
        self.temps = temps
        self.code = code

    def getCode(self):
        ret = f'package main;\n\nimport (\n\t"{self.packages}"\n);\n'
        for temp in self.temps:
            ret = ret + f'var {temp}\n'
        ret = ret + '\n'

        for func in self.code:
            ret = ret + func.getCode() + '\n\n'
        return ret

    def Mirilla(self):
        # Por cada funcion
        for func in self.code:
            tamanio = 20

            # Mientras no nos hemos pasado del tamaño (Fin del código)
            while tamanio <= len(func.instr):
                flagOpt = False

                # Darle 5 pasadas al codigo con el tamaño actual
                for i in range(5):
                    aux = 0
                    # Dar una pasada completa
                    while (tamanio + aux) <= len(func.instr):
                        flagOpt = flagOpt or self.Regla3(func.instr[0 + aux: tamanio + aux])
                        flagOpt = flagOpt or self.Regla6(func.instr[0 + aux: tamanio + aux])
                        flagOpt = flagOpt or self.Regla7(func.instr[0 + aux: tamanio + aux])
                        aux = aux + 1

                # Si no hubo optimizacion en la pasada, subir el tamaño
                if not flagOpt:
                    tamanio = tamanio + 20

    def Regla3(self, array):
        # Auxiliar para verificar que la regla se implemento
        ret = False
        # Recorrer el arreglo de instrucciones C3D
        for i in range(len(array)-2):
            actual = array[i]
            # Si la instruccion es un If
            if type(actual) is If and not actual.deleted:
                nextIns = array[i+1]
                # Si el siguiente es un Goto
                if type(nextIns) is Goto and not nextIns.deleted:
                    # SE DEBE ELIMINAR i+1 e i+2. Goto LBL y LBL:
                    sigIns = array[i+2]
                    if type(sigIns) is Label and not sigIns.deleted:
                        if sigIns.id == actual.label:
                            actual.condition.getContrary()
                            actual.label = nextIns.label
                            nextIns.deleted = True
                            array[i+2].deleted = True
                            ret = True
        return ret

    def Regla6(self, array):
        ret = False

        # Recorrer el arreglo de instrucciones C3D
        for i in range(len(array)):
            actual = array[i]
            # Si la instruccion es una Asignacion
            if type(actual) is Assignment and not actual.deleted and isinstance(actual.exp, Expression):
                # Si se esta asignando a si mismo
                if actual.selfAssignment():
                    actualOpt = actual.exp.neutralOps()
                    if actualOpt:
                        ret = True
                        actual.deleted = True
        return ret

    def Regla7(self, array):
        ret = False

        for i in range(len(array)):
            actual = array[i]
            if type(actual) is Assignment and not actual.deleted and isinstance(actual.exp, Expression):
                if actual.exp.eliminar_neutros():
                    ret = True
        return ret
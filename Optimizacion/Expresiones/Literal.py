from Optimizacion.C3DInstruccion import C3DInstruction


class Literal(C3DInstruction):

    def __init__(self, value, line, column, constant=False):
        C3DInstruction.__init__(self, line, column)
        self.value = value
        self.constant = constant
        self.deleted = False

    def getCode(self):
        if self.deleted:
            return ''
        return str(self.value)

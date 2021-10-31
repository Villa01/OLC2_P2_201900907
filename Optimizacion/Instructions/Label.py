from Optimizacion.C3DInstruccion import C3DInstruction


class Label(C3DInstruction):

    def __init__(self, id, line, column):
        C3DInstruction.__init__(self, line, column)
        self.id = id

    def getCode(self):
        if self.deleted:
            return ''
        return f'{self.id}:'

from Optimizacion.C3DInstruccion import C3DInstruction


class Goto(C3DInstruction):

    def __init__(self, label, line, column):
        C3DInstruction.__init__(self, line, column)
        self.label = label

    def getCode(self):
        if self.deleted:
            return ''
        return f'goto {self.label};'

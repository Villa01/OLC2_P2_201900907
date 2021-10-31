from Optimizacion.C3DInstruccion import C3DInstruction


class CallFun(C3DInstruction):

    def __init__(self, id, line, column):
        C3DInstruction.__init__(self, line, column)
        self.id = id

    def getCode(self):
        return f'{self.id}();'

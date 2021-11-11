from Optimizacion.C3DInstruccion import C3DInstruction
from Optimizacion.Expresiones import Literal


class Assignment(C3DInstruction):

    def __init__(self, place, exp, line, column):
        C3DInstruction.__init__(self, line, column)
        self.place = place
        self.exp = exp

    def selfAssignment(self):
        if type(self.exp) is Literal:
            aux = self.place.getCode() == self.exp.getCode()
        else:
            aux = self.place.getCode() == self.exp.right.getCode() or self.place.getCode() == self.exp.left.getCode()
        return aux

    def contiene(self, text):
        if text == self.place.getCode() or text == self.exp.getCode():
            return True
        return False

    def getCode(self):
        if self.deleted:
            return ''
        return f'{self.place.getCode()} = {self.exp.getCode()};'

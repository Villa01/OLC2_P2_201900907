
from Structure.AST.Node import Node
import re
import sys
sys.path.append('../')

from Structure.Expressions.Operations.Operations import Operation, Operator
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Structure.Interfaces.Expression import Expression
from Structure.SymbolTable.Type import Types

class Relational (Operation, Expression):
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
    
    def __init__(self, exp1 : Expression, operator : Operator, exp2 : Expression, line : int, column : int, expU : Expression) -> None:
        Operation.__init__(self=self, exp1=exp1, operator=operator,exp2= exp2,line= line, column=column, expU=expU)

    def getType(self, driver:Driver, ts: SymbolTable):
        value = self.getValue(driver, ts)

        if type(value) == float:
            return Types.FLOAT64
        elif type(value) == int:
            return Types.INT64
        elif type(value) == str and len(value)> 1:
            return Types.STRING
        elif type(value) == str and len(value) < 1: 
            return Types.CHAR  
        elif type(value) == bool: 
            return Types.BOOL  

    def getValue(self, driver:Driver, ts: SymbolTable):
        
        valor_exp1 = None
        valor_exp2 = None
        valor_expU = None

        if(self.expU == False):
            valor_exp1 = self.exp1.getValue(driver, ts)
            valor_exp2 = self.exp2.getValue(driver, ts)
        else:
            valor_expU = self.exp1.getValue(driver, ts)

        
        if(self.Operator == Operator.LESSTH):
            if type(valor_exp1) == int or type(valor_exp1) == float:
                
                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 < valor_exp2
                else: 
                    driver.agregarError(f'No se admite el < and con los tipos definidos', self.line, self.column)
            elif  type(valor_exp1) == str:
                if type(valor_exp2) == str:
                    return valor_exp1 < valor_exp2
                else: 
                    driver.agregarError(f'No se admite el operador < con los tipos definidos', self.line, self.column)
            else: 
                driver.agregarError(f'No se admite el operador < con los tipos definidos', self.line, self.column)
        elif(self.Operator == Operator.GREATERTH):
            if type(valor_exp1) == int or type(valor_exp1) == float:
                
                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 > valor_exp2
                else: 
                    driver.agregarError(f'No se admite el operador > con los tipos definidos', self.line, self.column)

            elif  type(valor_exp1) == str:
                if type(valor_exp2) == str:
                    return valor_exp1 > valor_exp2
                else: 
                    driver.agregarError(f'No se admite el operador > con los tipos definidos', self.line, self.column)
            else: 
                driver.agregarError(f'No se admite el operador > con los tipos definidos', self.line, self.column)

        elif(self.Operator == Operator.LESSOREQ):
            if type(valor_exp1) == int or type(valor_exp1) == float:
                
                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 <= valor_exp2
                elif type(valor_exp2) == bool:
                    return valor_exp1 <= valor_exp2
                else: 
                    driver.agregarError(f'No se admite el operador <= con los tipos definidos', self.line, self.column)

            elif  type(valor_exp1) == bool:
                if type(valor_exp2) == bool:
                    return valor_exp1 <= valor_exp2
                elif type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 <= valor_exp2
                else: 
                    driver.agregarError(f'No se admite el operador <= con los tipos definidos', self.line, self.column)

            elif  type(valor_exp1) == str:
                if type(valor_exp2) == str:
                    return valor_exp1 <= valor_exp2
                else: 
                    driver.agregarError(f'No se admite el operador <= con los tipos definidos', self.line, self.column)
            
            else: 
                driver.agregarError(f'No se admite el operador <= con los tipos definidos', self.line, self.column)
        
        elif(self.Operator == Operator.GREATOREQ):
            if type(valor_exp1) == int or type(valor_exp1) == float:
                
                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 >= valor_exp2
                elif type(valor_exp2) == bool:
                    return valor_exp1 >= valor_exp2
                else: 
                    driver.agregarError(f'No se admite el operador >= con los tipos definidos', self.line, self.column)

            elif  type(valor_exp1) == bool:
                if type(valor_exp2) == bool:
                    return valor_exp1 >= valor_exp2
                elif type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 >= valor_exp2
                else: 
                    driver.agregarError(f'No se admite el operador >= con los tipos definidos', self.line, self.column)
            
            elif  type(valor_exp1) == str:
                if type(valor_exp2) == str:
                    return valor_exp1 >= valor_exp2
                else: 
                    driver.agregarError(f'No se admite el operador >= con los tipos definidos', self.line, self.column)
            else: 
                driver.agregarError(f'No se admite el operador >= con los tipos definidos', self.line, self.column)

        elif(self.Operator == Operator.EQUALEQUAL):
            if type(valor_exp1) == int or type(valor_exp1) == float:
                
                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 == valor_exp2
                elif type(valor_exp2) == bool:
                    return valor_exp1 == valor_exp2
                else: 
                    driver.agregarError(f'No se admite el operador == con los tipos definidos', self.line, self.column)

            elif  type(valor_exp1) == bool:
                if type(valor_exp2) == bool:
                    return valor_exp1 == valor_exp2
                elif type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 == valor_exp2
                else: 
                    driver.agregarError(f'No se admite el operador == con los tipos definidos', self.line, self.column)

            elif  type(valor_exp1) == str:
                if type(valor_exp2) == str:
                    return valor_exp1 == valor_exp2
                else: 
                    driver.agregarError(f'No se admite el operador == con los tipos definidos', self.line, self.column)

            else: 
                driver.agregarError(f'No se admite el operador == con los tipos definidos', self.line, self.column)

        elif(self.Operator == Operator.DIFF):
            if type(valor_exp1) == int or type(valor_exp1) == float:
                
                if type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 != valor_exp2
                elif type(valor_exp2) == bool:
                    return valor_exp1 != valor_exp2
                else: 
                    driver.agregarError(f'No se admite el operador != con los tipos definidos', self.line, self.column)

            elif  type(valor_exp1) == bool:
                if type(valor_exp2) == bool:
                    return valor_exp1 != valor_exp2
                elif type(valor_exp2) == int or type(valor_exp2) == float:
                    return valor_exp1 != valor_exp2
                else: 
                    driver.agregarError(f'No se admite el operador != con los tipos definidos', self.line, self.column)
            
            elif  type(valor_exp1) == str:
                if type(valor_exp2) == str:
                    return valor_exp1 != valor_exp2
                else: 
                    driver.agregarError(f'No se admite el operador != con los tipos definidos', self.line, self.column)
            
        
        else: 
            driver.agregarError(f'No se admite la operacion', self.line, self.column)

    def traverse(self):
        padre = Node("RELACIONAL", "");
        temp = Operation(None, None, None, None, None, None)
        sOp = temp.getStringOperator(self.Operator)
        if (self.expU):
            padre.AddHijo(Node(sOp, ""))
            padre.AddHijo(self.exp1.traverse());
        else:
            padre.AddHijo(self.exp1.traverse());
            padre.AddHijo(Node(sOp, ""))
            padre.AddHijo(self.exp2.traverse());

        

        return padre
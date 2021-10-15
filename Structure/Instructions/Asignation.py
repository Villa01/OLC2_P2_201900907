

from Structure.Expressions.Identifier import Identifier
from Structure.AST.Node import Node
from Structure.Interfaces.Instruction import Instruction
from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.SymbolTable.Type import Type, Types
from Structure.SymbolTable.Symbol import Symbol

class Asignation (Instruction):
    

    def __init__(self, id : str, variable: Symbol, t: Type, env : str, line : int, column : int) -> None:
        super().__init__()
        self.id = id
        self.variable = variable
        self.line = line
        self.column = column
        self.type = t
        self.env = env

    def ejecutar(self, driver: Driver, ts : SymbolTable):
        var_value = None
        var_type = None
        
        if self.variable != None:
            var_value = self.variable.value.getValue(driver, ts)
            var_type = self.variable.value.getType(driver, ts)
        
        if self.type != None:
            # Si trae un tipo definido verificar que sea el mismo tipo que la variable
            if self.type.type == var_type:
                # Si trae un tipo definido y es el mismo que la variable agregar a la tabla de simbolos

                if self.env == 'global':
                    if ts.exist(self.id):
                        ts.getSymbol(self.id).setValue(var_value)
                    else:   
                        new_symbol = Symbol(1, self.type, self.id, var_value, None, False)
                        ts.add(self.id, new_symbol)
                else: 
                    if ts.existsInActual(self.id):
                        ts.getSymbol(self.id).setValue(var_value)
                    else:   
                        new_symbol = Symbol(1, self.type, self.id, var_value, None, False)
                        ts.add(self.id, new_symbol)
            else: 
                t = var_value
                if type(var_value) == float:
                    t = Type("FLOAT64")
                elif type(var_value) == int:
                    t = Type("INT64")
                elif type(var_value) == str:
                    t = Type("STRING")
                elif type(var_value) == bool: 
                    t = Type("BOOL")
                elif type(var_value) == list: 
                    t = Type("ARRAY")
                elif type(var_value) == range:
                    t = Type("RANGE")
                else:
                    t = Type("NOTHING")
                driver.agregarError(f'No hay conversion entre {self.type.stype} y {t.stype}.', self.line, self.column)
        # Sino agregar a la tabla de simbolos
        else:
            t = None
            if type(var_value) == float:
                t = Type("FLOAT64")
            elif type(var_value) == int:
                t = Type("INT64")
            elif type(var_value) == str:
                t = Type("STRING")
            elif type(var_value) == bool: 
                t = Type("BOOL")
            elif type(var_value) == list: 
                t = Type("ARRAY")
            elif type(var_value) == range:
                t = Type("RANGE")
            else:
                t = Type("NOTHING")
            
            if self.env == 'global':
                if ts.exist(self.id):
                    ts.getSymbol(self.id).setValue(var_value)
                else: 
                    new_symbol = Symbol(1, t, self.id, var_value,  None, False)
                    ts.add(self.id, new_symbol)
            elif self.env == 'local': 
                if ts.existsInActual(self.id):
                    ts.getSymbol(self.id).setValue(var_value)
                else: 
                    new_symbol = Symbol(1, t, self.id, var_value,  None, False)
                    ts.add(self.id, new_symbol)

            else: 
                if ts.exist(self.id):
                    ts.getSymbol(self.id).setValue(var_value)
                else: 
                    new_symbol = Symbol(1, t, self.id, var_value,  None, False)
                    ts.add(self.id, new_symbol)


    def traverse(self):
        padre = Node("ASIGNACION", "")

        padre.AddHijo(Node(self.id,""))
        padre.AddHijo(Node(" = ",""))
        padre.AddHijo(self.variable.value.traverse())

        return padre

import sys

sys.path.append('../')


from Structure.Driver import Driver
from Structure.SymbolTable.SymbolTable import SymbolTable
from Temporal import Temporal


class Expression:

    def getType(self, driver: Driver, symbolTable):
        """
        Returns the type of the expression. 
        Parameters
        ----------
        driver: Driver
                Helps to manage all errors, reports and enviroments in the interpreter.
        symbolTable: SymbolTable
                Table where all the info of variables and functions is saved. 
        """
        pass

    def getValue(self, driver: Driver, symbolTable):
        """
        Returns the value of the expression.
        Parameters
        ----------
        driver: Driver
                Helps to manage all errors, reports and enviroments in the interpreter.
        symbolTable: SymbolTable
                Table where all the info of variables and functions is saved. 
        """
        pass

    def compilar(self, driver: Driver, symbol_table: SymbolTable, tmp: Temporal):
        pass

    def traverse(self):
        """
        Traverse the ast taking this node as the root. 
        Returns
        -------
        node : Node
            An ast node
        """
        pass

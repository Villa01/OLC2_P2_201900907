from Structure.SymbolTable.Type import Type
from Structure.SymbolTable.Symbol import Symbol
from Structure.SymbolTable.SymbolTable import SymbolTable
import sys

sys.path.append('../')

from Structure.AST.Error import Err, errors


class Driver:

    def __init__(self) -> None:
        self.error = []
        self.symbolTable = []
        self.console = ""
        self.size = 0

    def append(self, text):
        self.console += text

    def addError(self, t, description, line, column):
        error = Err(t, description, line, column)
        self.error.append(error)
        self.appendToConsole(f'{description} Linea: {line}, Columna: {column}')

    def appendToConsole(self, text):
        self.console += text + "\n"

    def agregarError(self, msg: str, line: int, column: int, t="SEMANTIC"):
        err = Err(t, msg, line, column)
        self.error.append(err)
        self.append(msg + ' Linea: ' + str(line) + ' Columna ' + str(column) + '\n')

    def graficar_er(self, controlador, ts):
        cuerpohtml = "<html><header><title>ReportedeErrores</title><style>#tabla {font-family:Arial,Helvetica," \
                     "sans-serif;border-collapse:collapse;width:100%;}#tabla  td,#tabla  th{" \
                     "border:1pxsolid#ddd;padding:8px;}#tabla  tr:nth-child(even){background-color:#f2f2f2;}#tabla  " \
                     "tr:hover{background-color:#ddd;}#tabla  th{" \
                     "padding-top:12px;padding-bottom:12px;text-align:left;background-color:#04AA6D;color:white" \
                     ";}</style></header><body> "
        cuerpohtml += "<table id=\"tabla\">"
        cuerpohtml += "<thead>"
        cuerpohtml += "<tr>" + "<td colspan=\"6\">Tabla de Errores</td>" + "</tr>" + "<tr>" + "<th>No.</th>" \
                                                                                              "<th>Tipo</th>" + "<th>Descripción</th>" + "<th>Linea</th>" + "<th>Columna</th>" + "</tr>" \
                                                                                                                                                                                 "</thead> "

        numero = 1
        for sim in self.error:
            cuerpohtml += "<tr>" + "<td>" + str(numero) + "</td><td>"
            cuerpohtml += sim.type + "</td><td>" + sim.description + "</td><td>" + str(sim.line) + "</td><td>"
            cuerpohtml += str(sim.column) + "</td>" + "</tr>"
            numero += 1

        cuerpohtml += '</body></html>'
        return cuerpohtml

    def graficar_st(self, controlador, ts):
        cuerpohtml = "<html><header><title>ReporteTablaSimbolos</title><style>#tabla {font-family:Arial,Helvetica," \
                     "sans-serif;border-collapse:collapse;width:100%;}#tabla  td,#tabla  th{" \
                     "border:1pxsolid#ddd;padding:8px;}#tabla  tr:nth-child(even){background-color:#f2f2f2;}#tabla  " \
                     "tr:hover{background-color:#ddd;}#tabla  th{" \
                     "padding-top:12px;padding-bottom:12px;text-align:left;background-color:#04AA6D;color:white" \
                     ";}</style></header><body> "
        cuerpohtml += "<table id=\"tabla\">"
        cuerpohtml += "<thead>"
        cuerpohtml += "<tr>" + "<td colspan=\"6\">Tabla de Simbolo</td>" + "</tr>" + "<tr>" + "<th>Rol</th>" + "<th>Nombre</th>" + "<th>Tipo</th>" + "<th>Ambito</th>" + "<th>Valor</th>" + "<th>Paramtros</th>" + "</tr>" + "</thead>"

        numero = 1
        for tabla in self.symbolTable:
            for sim in tabla.table.values():
                cuerpohtml += "<tr>" + "<td>" + self.getRol(sim) + "</td><td>"
                cuerpohtml += sim.identifier + "</td><td>" + self.getType(sim) + "</td><td>" + self.getEnv(
                    tabla) + "</td><td>"
                cuerpohtml += self.getValor(sim) + "</td><td>" + self.parametros(sim) + "</td>" + "</tr>"
                numero += 1

        cuerpohtml += '</body></html>'
        return cuerpohtml

    def agregarTabla(self, table):
        self.symbolTable.append(table)

    def getValor(self, sim: Symbol):
        if sim.value is not None:
            if type(sim.value) == str:
                return sim.value
            elif not type(sim.value) == str:
                return str(sim.value)
            else:
                return '...'

        else:
            return '...'

    def getType(self, sim: Symbol):
        return sim.symbol_type.stype.lower()

    def getRol(self, sim: Symbol):
        return sim.symbol_type.stype

    def getEnv(self, table: SymbolTable):
        if table.env:
            return table.env
        else:
            return '...'

    def parametros(self, sim: Symbol):
        if sim.param_list:
            return len(sim.param_list)
        else:
            return '...'

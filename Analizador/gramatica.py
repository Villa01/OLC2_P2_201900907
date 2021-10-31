#
# analizador léxico
#

import Analizador.ply.lex as lex
from Structure.Expressions.Operations.Native.Pop import Pop
from Structure.Expressions.Operations.Native.Push import Push
from Structure.Instructions.Functions import Function
from Structure.Instructions.Llamada import Llamada
from Structure.Instructions.Transference_structures.ReturnStructure import ReturnStructure

reserved = {
    'print': 'PRINT',
    'println': 'PRINTLN',
    'log10': 'LOG10',
    'log': 'LOG',
    'sin': 'SENO',
    'cos': 'COS',
    'tan': 'TAN',
    'sqrt': 'SQRT',
    'true': 'TRUE',
    'false': 'FALSE',
    'lowercase': 'LOWERCASE',
    'uppercase': 'UPPERCASE',
    'Int64': 'INT64',
    'String': 'STRING',
    'Float64': 'FLOAT64',
    'Bool': 'BOOL',
    'Char': 'CHAR',
    'Nothing': 'NOTHING',
    'parse': 'PARSE',
    'trunc': 'TRUNC',
    'float': 'FLOAT',
    'string': 'FSTRING',
    'typeof': 'TYPEOF',
    'if': 'IF',
    'elseif': 'ELSEIF',
    'else': 'ELSE',
    'end': 'END',
    'while': 'WHILE',
    'for': 'FOR',
    'in': 'IN',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'global': 'GLOBAL',
    'local': 'LOCAL',
    'length': 'LENGTH',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'pop': 'POP',
    'push': 'PUSH',
    'Array': 'ARRAY'
}

# lista del los nombres de los tokens
tokens = [
             'PARA',
             'PARC',
             'CORA',
             'CORC',
             'MAS',
             'MENOS',
             'POR',
             'DIVIDIDO',
             'DECIMAL',
             'ENTERO',
             'PYC',
             'POT',
             'MOD',
             'CADENA',
             'COMA',
             'MENORIGUAL',
             'MAYORIGUAL',
             'IGUALIGUAL',
             'DIFF',
             'MENORQUE',
             'MAYORQUE',
             'AND',
             'OR',
             'NOT',
             'ID',
             'DOSPTS',
             'IGUAL'
         ] + list(reserved.values())


# Tokens que necesitan acciones
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t


def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1]  # remuevo las comillas
    return t


def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_multi_comment(t):
    r'\#\=[^=]*\=\#'
    pass


def t_COMMENT(t):
    r'\#.*'
    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


# tokens que no necesitan acciones
t_PARA = r'\('
t_PARC = r'\)'
t_CORA = r'\['
t_CORC = r'\]'
t_MAS = r'\+'
t_MENOS = r'\-'
t_POR = r'\*'
t_DIVIDIDO = r'\/'
t_PYC = r'\;'
t_POT = r'\^'
t_MOD = r'\%'
t_COMA = r'\,'
t_DOSPTS = r'\:'

t_MENORIGUAL = r'\<\='
t_MAYORIGUAL = r'\>\='
t_IGUALIGUAL = r'\=\='
t_DIFF = r'\!\='
t_MENORQUE = r'\<'
t_MAYORQUE = r'\>'

t_AND = r'\&\&'
t_OR = r'\|\|'
t_NOT = r'\!'
t_IGUAL = r'\='

# Caracteres ignorados
t_ignore = " \t"


# manejo de errores lexicos
def t_error(t):
    print("Caracter no reconocido '%s'" % t.value[0])
    t.lexer.skip(1)


# Construyendo el analizador léxico
lexer = lex.lex()

#
# Analisis sintactico
#

# imports
import Analizador.ply.yacc as yacc
import sys

sys.path.append('../')

from Structure.Expressions.Operations.Arithmetic import Arithmetic
from Structure.Expressions.Operations.Relational import Relational
from Structure.Expressions.Operations.Logic import Logic
from Structure.Expressions.Primitive import Primitive

from Structure.AST.Ast import Ast
from Structure.Instructions.Print import Print
from Structure.Instructions.Asignation import Asignation
from Structure.Instructions.Control_structures.IfStructure import IfStructure
from Structure.Instructions.Loops.FoorLoop import FoorLoop
from Structure.Instructions.Loops.WhileLoop import WhileLoop
from Structure.Instructions.Transference_structures.BreakStructure import BreakStructure
from Structure.Instructions.Transference_structures.ContinueStructure import ContinueStructure
from Structure.Expressions.VectorAccess import VectorAccess
from Structure.Expressions.TypeRange import TypeRange

from Structure.SymbolTable.Symbol import Symbol
from Structure.SymbolTable.Type import Type

from Structure.Expressions.Operations.Native.Length import Length
from Structure.Instructions.VectorAsignation import VectorAsignation

from Structure.Expressions.Operations.Native.Logarithm import Logarithm
from Structure.Expressions.Operations.Native.Sin import Sin
from Structure.Expressions.Operations.Native.Cos import Cos
from Structure.Expressions.Operations.Native.Tan import Tan
from Structure.Expressions.Operations.Native.Sqrt import Sqrt
from Structure.Expressions.Operations.Native.Trunc import Trunc
from Structure.Expressions.Operations.Native.Float import Float
from Structure.Expressions.Operations.Native.String import String
from Structure.Expressions.Operations.Native.Typeof import Typeof
from Structure.Expressions.Operations.Native.Lowercase import Lowercase
from Structure.Expressions.Operations.Native.Uppercase import Uppercase
from Structure.Expressions.Operations.Native.Parse import Parse
from Structure.Expressions.Identifier import Identifier

# Asociación de operadores y precedencia
precedence = (
    ('left', 'OR', 'AND'),
    ('right', 'NOT'),
    ('left', 'MENORQUE', 'MAYORQUE', 'IGUALIGUAL', 'DIFF', 'MENORIGUAL', 'MAYORIGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO'),
    ('left', 'POT', 'MOD'),
    ('right', 'UNARIA'),
)


def p_start(t):
    """init : instrucciones"""
    t[0] = Ast(t[1])


# Definición de la gramática
def p_instrucciones_lista(t):
    """
    instrucciones    : instrucciones instruccion PYC
                     | instrucciones instruccion
    """
    t[0] = t[1]
    t[0].append(t[2])


def p_instruccion(t):
    """
    instrucciones : instruccion PYC
                    | instruccion
    """
    t[0] = []
    t[0].append(t[1])


def p_instrucciones_evaluar(t):
    """
    instruccion : print
                | println
                | asignacion
                | declaracion
                | sent_if
                | sent_while
                | sent_for
                | sent_break
                | sent_continue
                | asignacion_vect
                | sent_function
                | sent_llamada
                | sent_return
                | sent_push
                | sent_pop
                | expresion
    """
    t[0] = t[1]


def p_sent_pop(t):
    """
    sent_pop : POP NOT PARA expresion PARC
    """
    t[0] = Pop(t[4], t.lineno(1), 0)


def p_push(t):
    """
    sent_push : PUSH NOT PARA expresion COMA expresion PARC
    """
    t[0] = Push(t[4], t[6], t.lineno(1), 0)


def p_sent_return(t):
    """
    sent_return : RETURN
    """
    t[0] = ReturnStructure(None, t.lineno(1), 0)


def p_sent_return_v(t):
    """
    sent_return : RETURN expresion
    """
    t[0] = ReturnStructure(t[2], t.lineno(1), 0)


def p_sent_llamada(t):
    """
    sent_llamada : ID PARA PARC
    """
    t[0] = Llamada(t[1], [], t.lineno(1), 0)


def p_sent_llamada_p(t):
    """
    sent_llamada : ID PARA lista_expr PARC
    """
    t[0] = Llamada(t[1], t[3], t.lineno(1), 0)


def p_sent_function(t):
    """
    sent_function : FUNCTION ID PARA parametros PARC DOSPTS DOSPTS tipo instrucciones END
    """
    t[0] = Function(3, t[8], t[2], None, t[4], True, t[9], t.lineno(1), 0)


def p_sent_function2(t):
    """
    sent_function : FUNCTION ID PARA PARC DOSPTS DOSPTS tipo instrucciones END
    """
    t[0] = Function(3, t[7], t[2], None, [], True, t[8], t.lineno(1), 0)


def p_lista_parametros(t):
    """
    parametros : parametros COMA ID
    """
    t[0] = t[1]
    t[0].append(Symbol(1, Type('NOTHING'), t[3], None, None, False))


def p_lista_parametros_tipo(t):
    """
    parametros : parametros COMA ID DOSPTS DOSPTS tipo
    """
    t[0] = t[1]
    t[0].append(Symbol(1, t[5], t[3], None, None, False))


"""
def p_parametro(t):
    parametros : ID
    t[0] = [Symbol(1, Type('NOTHING'), t[1], None, None, False)]
"""


def p_parametro_t(t):
    """
    parametros : ID DOSPTS DOSPTS tipo
    """
    t[0] = [Symbol(1, t[4], t[1], None, None, False)]


def p_declaracion(t):
    """
    declaracion : GLOBAL ID
                | LOCAL ID
    """
    if t[1] == 'global':
        t[0] = Asignation(t[2], None, None, 'global', t.lineno(1), 0)
    elif t[1] == 'local':
        t[0] = Asignation(t[2], None, None, 'local', t.lineno(1), 0)


def p_asignacion_vect(t):
    """
    asignacion_vect : ID list_vector IGUAL expresion
    """
    t[0] = VectorAsignation(t[1], t[2], t[4], t.lineno(1), 0)


def p_sent_break(t):
    """
    sent_break : BREAK
    """
    t[0] = BreakStructure()


def p_sent_continue(t):
    """
    sent_continue : CONTINUE
    """
    t[0] = ContinueStructure()


def p_sent_for_(t):
    """
    sent_for : FOR ID IN expresion instrucciones END
    """
    t[0] = FoorLoop(t[2], t[4], t[5], t.lineno(1), 0)


def p_sent_while(t):
    """
    sent_while : WHILE expresion instrucciones END
    """
    t[0] = WhileLoop(t[2], t[3], t.lineno(1), 0)


def p_sent_while_par(t):
    """
    sent_while : WHILE PARA expresion PARC instrucciones END
    """
    t[0] = WhileLoop(t[3], t[5], t.lineno(1), 0)


def p_sent_if(t):
    """
    sent_if : IF expresion instrucciones END
    """
    t[0] = IfStructure(t[2], t[3], [], t.lineno(1), 0)


def p_sent_if_par(t):
    """
    sent_if : IF PARA expresion PARC instrucciones END
    """
    t[0] = IfStructure(t[3], t[5], [], t.lineno(1), 0)


def p_sent_if_else(t):
    """
    sent_if : IF expresion instrucciones ELSE instrucciones END
    """
    t[0] = IfStructure(t[2], t[3], t[5], t.lineno(1), 0)


def p_sent_if_else_par(t):
    """
    sent_if : IF PARA expresion PARC instrucciones ELSE instrucciones END
    """
    t[0] = IfStructure(t[3], t[5], t[7], t.lineno(1), 0)


def p_sent_if_elseif(t):
    """
    sent_if : IF expresion instrucciones else_if
    """
    t[0] = IfStructure(t[2], t[3], [t[4]], t.lineno(1), 0)


def p_sent_if_elseif_par(t):
    """
    sent_if : IF PARA expresion PARC instrucciones else_if
    """
    t[0] = IfStructure(t[3], t[5], [t[6]], t.lineno(1), 0)


def p_elseif_end(t):
    """
    else_if : ELSEIF expresion instrucciones END
    """
    t[0] = IfStructure(t[2], t[3], [], t.lineno(1), 0)


def p_elseif_end_par(t):
    """
    else_if : ELSEIF PARA expresion PARC instrucciones END
    """
    t[0] = IfStructure(t[3], t[5], [], t.lineno(1), 0)


def p_elseif(t):
    """
    else_if : ELSEIF expresion instrucciones else_if
    """
    t[0] = IfStructure(t[2], t[3], [t[4]], t.lineno(1), 0)


def p_elseif_par(t):
    """
    else_if : ELSEIF PARA expresion PARC instrucciones else_if
    """
    t[0] = IfStructure(t[3], t[5], [t[6]], t.lineno(1), 0)


def p_elseif_else(t):
    """
    else_if : ELSEIF expresion instrucciones ELSE instrucciones END
    """
    t[0] = IfStructure(t[2], t[3], t[5], t.lineno(1), 0)


def p_elseif_else_par(t):
    """
    else_if : ELSEIF PARA expresion PARC instrucciones ELSE instrucciones END
    """
    t[0] = IfStructure(t[3], t[5], t[7], t.lineno(1), 0)


def p_asignacion_tipo(t):
    """
    asignacion : ID IGUAL expresion DOSPTS DOSPTS tipo
    """
    t[0] = Asignation(t[1],
                      Symbol(1, t[6], t[1], t[3], None, False),
                      t[6],
                      'local', t.lineno(1), 0
                      )


def p_asignacion_tipo_g(t):
    """
    asignacion  : GLOBAL ID IGUAL expresion DOSPTS DOSPTS tipo
                | LOCAL ID IGUAL expresion DOSPTS DOSPTS tipo
    """
    t[0] = Asignation(t[2],
                      Symbol(1, t[7], t[2], t[4], None, False),
                      t[7],
                      t[1], t.lineno(1), 0
                      )


def p_asignacion(t):
    """
    asignacion : ID IGUAL expresion
    """
    t[0] = Asignation(t[1],
                      Symbol(1, None, t[1], t[3], None, False),
                      None,
                      None, t.lineno(1), 0
                      )


def p_asignacion_2(t):
    """
    asignacion : GLOBAL ID IGUAL expresion
                | LOCAL ID IGUAL expresion
    """

    t[0] = Asignation(t[2],
                      Symbol(1, None, t[2], t[4], None, False),
                      None,
                      t[1], t.lineno(1), 0
                      )


def p_tipo(t):
    """
    tipo : INT64
        | FLOAT64
        | STRING
        | NOTHING
        | BOOL
        | CHAR
        | ARRAY
    """
    t[0] = Type(t[1].upper())


def p_print(t):
    """
    print : PRINT PARA lista_expr PARC
    """
    t[0] = Print(t[3], t.lineno(1), 0, False)


def p_print_vacio(t):
    """
    println : PRINT PARA PARC
    """
    t[0] = Print([], t.lineno(1), 0, False)


def p_println_vacio(t):
    """
    println : PRINTLN PARA PARC
    """
    t[0] = Print([], t.lineno(1), 0, True)


def p_println(t):
    """
    println : PRINTLN PARA lista_expr PARC
    """
    t[0] = Print(t[3], t.lineno(1), 0, True)


def p_lista_expr_r(t):
    """
    lista_expr : lista_expr COMA expresion
    """
    t[0] = t[1]
    t[0].append(t[3])


def p_lista_expr(t):
    """
    lista_expr : expresion
    """
    t[0] = []
    t[0].append(t[1])


def p_expresion_binaria(t):
    """expresion : expresion MAS expresion
                  | expresion MENOS expresion
                  | expresion POR expresion
                  | expresion DIVIDIDO expresion
                  | expresion MOD expresion
                  | expresion POT expresion
    """
    t[0] = Arithmetic(t[1], t[2], t[3], t.lineno(1), 0, False)


def p_expresion_vector(t):
    """
    expresion : ID list_vector
    """
    t[0] = VectorAccess(t[1], t[2], t.lineno(1), 0)


def p_expresion_vector_list(t):
    """
    list_vector : list_vector CORA expresion CORC
    """
    t[0] = t[1]
    t[0].append(t[3])


def p_expresion_pos_vector(t):
    """
    list_vector : CORA expresion CORC
    """
    t[0] = []
    t[0].append(t[2])


def p_expresion_unaria(t):
    """expresion : MENOS expresion %prec UNARIA"""
    t[0] = Arithmetic(t[2], 'UNARIO', None, t.lineno(1), 0, True)


def p_expresion_relacional(t):
    """
    expresion : expresion MENORIGUAL expresion
                  | expresion MAYORIGUAL expresion
                  | expresion MENORQUE expresion
                  | expresion MAYORQUE expresion
                  | expresion DIFF expresion
                  | expresion IGUALIGUAL expresion
    """
    t[0] = Relational(t[1], t[2], t[3], t.lineno(1), 0, False)


def p_expresion_logica(t):
    """
    expresion : expresion AND expresion
                | expresion OR expresion
    """
    t[0] = Logic(t[1], t[2], t[3], t.lineno(1), 0, False)


def p_expresion_logica_unario(t):
    """
    expresion : NOT expresion
    """

    t[0] = Logic(t[2], t[1], None, t.lineno(1), 0, True)


def p_expresion_agrupacion(t):
    """expresion : PARA expresion PARC"""
    t[0] = t[2]


def p_expresion_primitivas(t):
    """
    expresion    : ENTERO
                    | DECIMAL
                    | CADENA
                    | TRUE
                    | FALSE
    """
    if t[1] == "true":
        t[1] = True
    elif t[1] == "false":
        t[1] = False
    t[0] = Primitive(t[1], t.lineno(1), 0)


def p_expresion_array(t):
    """
    expresion : CORA lista_expr CORC
    """
    t[0] = Primitive(t[2], t.lineno(1), 0)


def p_expresion_range(t):
    """
    expresion : expresion DOSPTS expresion
    """
    t[0] = TypeRange(t[1], t[3], t.lineno(1), 0)


def p_expresion_llamada(t):
    """
    expresion : sent_llamada
    """
    t[0] = t[1]


def p_expresion_id(t):
    """
    expresion : ID
    """
    t[0] = Identifier(t[1], t.lineno(1), 0)


def p_expresion_nativas(t):
    """
    expresion : LOG10 PARA expresion PARC
              | LOG PARA expresion COMA expresion PARC
              | SENO PARA expresion PARC
              | COS PARA expresion PARC
              | TAN PARA expresion PARC
              | SQRT PARA expresion PARC
              | LOWERCASE PARA expresion PARC
              | UPPERCASE PARA expresion PARC
              | TRUNC PARA expresion PARC
              | FLOAT PARA expresion PARC
              | FSTRING PARA expresion PARC
              | TYPEOF PARA expresion PARC
              | PARSE PARA tipo COMA expresion PARC
              | LENGTH PARA expresion PARC
              | POP NOT PARA expresion PARC
    """

    if t[1] == 'log10':
        t[0] = Logarithm(
            Primitive(10, t.lineno(1), 0),
            t[3],
            t.lineno(1), 0
        )
    elif t[1] == 'log':
        t[0] = Logarithm(
            t[3],
            t[5],
            t.lineno(1), 0
        )
    elif t[1] == 'sin':
        t[0] = Sin(t[3], t.lineno(1), 0)

    elif t[1] == 'cos':
        t[0] = Cos(t[3], t.lineno(1), 0)

    elif t[1] == 'tan':
        t[0] = Tan(t[3], t.lineno(1), 0)

    elif t[1] == 'sqrt':
        t[0] = Sqrt(t[3], t.lineno(1), 0)

    elif t[1] == 'lowercase':
        t[0] = Lowercase(t[3], t.lineno(1), 0)

    elif t[1] == 'uppercase':
        t[0] = Uppercase(t[3], t.lineno(1), 0)

    elif t[1] == 'parse':
        t[0] = Parse(t[5], t[3], t.lineno(1), 0)

    elif t[1] == 'trunc':
        t[0] = Trunc(t[3], t.lineno(1), 0)

    elif t[1] == 'float':
        t[0] = Float(t[3], t.lineno(1), 0)

    elif t[1] == 'string':
        t[0] = String(t[3], t.lineno(1), 0)

    elif t[1] == 'typeof':
        t[0] = Typeof(t[3], t.lineno(1), 0)

    elif t[1] == 'length':
        t[0] = Length(t[3], t.lineno(1), 0)

    elif t[1] == 'pop':
        t[0] = Pop(t[4], t.lineno(1), 0)


def p_error(t):
    print("Error sintáctico en '%s'" % t.value)


parser = yacc.yacc(debug=True)

# obtener ruta
# here = os.path.dirname(os.path.abspath(__file__))
# filename = os.path.join(here,"entrada.txt")

# f = open(filename, "r")
# input = f.read()
# print(input)
# parser.parse(input)

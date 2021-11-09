from enum import Enum


class Types(Enum):
    INT64 = 1
    FLOAT64 = 2
    BOOL = 3
    CHAR = 4
    STRING = 5
    NOTHING = 6
    ARRAY = 7
    RANGE = 8
    STRUCT = 9


def get_type(var_value):
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
    return t


def get_stype(types):
    if types == Types.INT64:
        return 'Int64'
    elif types == Types.ARRAY:
        return 'Array'
    elif types == Types.STRING:
        return 'String'
    elif types == Types.BOOL:
        return 'Bool'
    elif types == Types.FLOAT64:
        return 'Float64'
    elif types == Types.RANGE:
        return 'Range'
    elif types == Types.CHAR:
        return 'Char'
    else:
        return 'Nothing'


class Type:

    def __init__(self, stype: str) -> None:
        self.stype = stype
        self.type = self.getType(stype)

    def getType(self, s: str):
        if s == "INT64":
            return Types.INT64
        elif s == "FLOAT64":
            return Types.FLOAT64
        elif s == "BOOL":
            return Types.BOOL
        elif s == "CHAR":
            return Types.CHAR
        elif s == "STRING":
            return Types.STRING
        elif s == "NOTHING":
            return Types.NOTHING
        elif s == "RANGE":
            return Types.RANGE
        elif s == "ARRAY":
            return Types.ARRAY

    def getStype(self):
        return self.stype

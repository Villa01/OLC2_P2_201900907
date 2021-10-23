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



class Type:

    def __init__(self, stype: str) -> None:
        self.stype = stype
        self.type = getType(stype)

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

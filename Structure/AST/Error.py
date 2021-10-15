from enum import Enum

class errors(Enum):
    LEXICAL = 1
    SYNTACTIC = 2
    SEMANTIC = 3

class Err:

    def __init__(self, type, description, line, column) -> None:
        self.type = type
        self.description = description
        self.line = line
        self.column = column

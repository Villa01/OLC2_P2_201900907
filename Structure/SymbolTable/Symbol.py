from Structure.SymbolTable.Type import Type


class Symbol:

    def __init__(self, symbol: int, symbol_type: Type, identifier: str, value, param_list, method, position=0,
                 is_global=True, in_heap=False) -> None:
        'Symbol :  1-variable 2-funcion 3-metodo 4-vector 6-param'
        self.symbol = symbol
        self.symbol_type = symbol_type
        self.identifier = identifier
        self.value = value
        self.param_list = param_list
        self.method = method
        self.position = position
        self.is_global = is_global
        self.in_heap = in_heap

    def setValue(self, value):
        self.value = value

    def compilar(self, driver, symbol_table, tmp):
        return self

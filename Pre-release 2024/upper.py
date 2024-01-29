def __GetSymbolFromUser(self):
    Symbol = ""
    while not Symbol in self.__AllowedSymbols:
        Symbol = input("Enter symbol: ").upper()
    return Symbol

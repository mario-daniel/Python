def __LoadPuzzle(self, Filename):
    try:
        with open(Filename) as f:
            NoOfSymbols = int(f.readline().rstrip())
            for Count in range (1, NoOfSymbols + 1):
                self.__AllowedSymbols.append(f.readline().rstrip())
            NoOfPatterns = int(f.readline().rstrip())
            for Count in range(1, NoOfPatterns + 1):
                Items = f.readline().rstrip().split(",")
                P = Pattern(Items[0], Items[1])
                self.__AllowedPatterns.append(P)
            self.__GridSize = int(f.readline().rstrip())
            for Count in range (1, self.__GridSize * self.__GridSize + 1):
                Items = f.readline().rstrip().split(",")
                if Items[0] == "@":
                    C = BlockedCell()
                    self.__Grid.append(C)
                else:
                    C = Cell()
                    C.ChangeSymbolInCell(Items[0])
                    for CurrentSymbol in range(1, len(Items)):
                        C.AddToNotAllowedSymbols(Items[CurrentSymbol])
                    self.__Grid.append(C)
            self.__Score = int(f.readline().rstrip())
            self.__SymbolsLeft = int(f.readline().rstrip())
            print(self.__SymbolsLeft)
    except:
        print("Puzzle not loaded")
#--------------------------------------------------------------------------------------------------------------
        exit()
#--------------------------------------------------------------------------------------------------------------

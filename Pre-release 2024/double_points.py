class Puzzle():
    def __init__(self, *args):
        if len(args) == 1:
            self.__Score = 0
            self.__SymbolsLeft = 0
            self.__GridSize = 0
            self.__Grid = []
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            self.__LoadPuzzle(args[0])
        else:
            self.__Score = 0
            self.__SymbolsLeft = args[1]
            self.__GridSize = args[0]
            self.__Grid = []
            for Count in range(1, self.__GridSize * self.__GridSize + 1):
                if random.randrange(1, 101) < 90:
                    C = Cell()
                else:
                    C = BlockedCell()
                self.__Grid.append(C)
#------------------------------------------------------------------------------------------------
            for Count in range(0, 5):
                Index = random.randint(1, 63)
                C = self.__Grid[Index]
                while C.GetSymbol() != '-':
                    Index = random.randint(1, 63)
                    C = self.__Grid[Index]
                self.__Grid[Index] = DoublePointCell()
#------------------------------------------------------------------------------------------------
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            QPattern = Pattern("Q", "QQ**Q**QQ")
            self.__AllowedPatterns.append(QPattern)
            self.__AllowedSymbols.append("Q")
            XPattern = Pattern("X", "X*X*X*X*X")
            self.__AllowedPatterns.append(XPattern)
            self.__AllowedSymbols.append("X")
            TPattern = Pattern("T", "TTT**T**T")


    def CheckforMatchWithPattern(self, Row, Column):
        for StartRow in range(Row + 2, Row - 1, -1):
            for StartColumn in range(Column - 2, Column + 1):
                try:
                    PatternString = ""
#------------------------------------------------------------------------------------------------
                    Pattern = []
                    PatternString += self.__GetCell(StartRow, StartColumn).GetSymbol()
                    Pattern.append(self.__GetCell(StartRow, StartColumn))
                    PatternString += self.__GetCell(StartRow, StartColumn + 1).GetSymbol()
                    Pattern.append(self.__GetCell(StartRow, StartColumn + 1))
                    PatternString += self.__GetCell(StartRow, StartColumn + 2).GetSymbol()
                    Pattern.append(self.__GetCell(StartRow, StartColumn + 2))
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 2).GetSymbol()
                    Pattern.append(self.__GetCell(StartRow - 1, StartColumn + 2))
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 2).GetSymbol()
                    Pattern.append(self.__GetCell(StartRow - 2, StartColumn + 2))
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 1).GetSymbol()
                    Pattern.append(self.__GetCell(StartRow - 2, StartColumn + 1))
                    PatternString += self.__GetCell(StartRow - 2, StartColumn).GetSymbol()
                    Pattern.append(self.__GetCell(StartRow - 2, StartColumn))
                    PatternString += self.__GetCell(StartRow - 1, StartColumn).GetSymbol()
                    Pattern.append(self.__GetCell(StartRow - 1, StartColumn))
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 1).GetSymbol()
                    Pattern.append(self.__GetCell(StartRow - 1, StartColumn))
#------------------------------------------------------------------------------------------------
                    for P in self.__AllowedPatterns:
                        CurrentSymbol = self.__GetCell(Row, Column).GetSymbol()
                        if P.MatchesPattern(PatternString, CurrentSymbol):
                            self.__GetCell(StartRow, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
#------------------------------------------------------------------------------------------------
                            for cell in Pattern:
                                try:
                                    if cell.IsDouble():
                                        self.__Points = 20
                                        break
                                except:
                                        self.__Points = 10
                            return self.__Points
#------------------------------------------------------------------------------------------------
                except:
                    pass
        return 0
            self.__AllowedPatterns.append(TPattern)
            self.__AllowedSymbols.append("T")

#------------------------------------------------------------------------------------------------
class DoublePointCell(Cell):
    def __init__(self):
        super(DoublePointCell, self).__init__()
        self._Symbol = 'D'

    def IsDouble(self):
        return True
#------------------------------------------------------------------------------------------------

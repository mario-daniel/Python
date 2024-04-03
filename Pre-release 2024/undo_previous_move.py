class Puzzle():
    def __init__(self, *args):
        if len(args) == 1:
            self.__Score = 0
            self.__SymbolsLeft = 0
            self.__GridSize = 0
            self.__Grid = []
#-------------------------------------------------------------------------------------------------
            self.__PreviousMoves = []
#-------------------------------------------------------------------------------------------------
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            self.__LoadPuzzle(args[0])
        else:
            self.__Score = 0
            self.__SymbolsLeft = args[1]
            self.__GridSize = args[0]
            self.__Grid = []
#-------------------------------------------------------------------------------------------------
            self.__PreviousMoves = []
#-------------------------------------------------------------------------------------------------
            for Count in range(1, self.__GridSize * self.__GridSize + 1):
                if random.randrange(1, 101) < 90:
                    C = Cell()
                else:
                    C = BlockedCell()
                self.__Grid.append(C)
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            QPattern = Pattern("Q", "QQ**Q**QQ")
            self.__AllowedPatterns.append(QPattern)
            self.__AllowedSymbols.append("Q")
            XPattern = Pattern("X", "X*X*X*X*X")
            self.__AllowedPatterns.append(XPattern)
            self.__AllowedSymbols.append("X")
            TPattern = Pattern("T", "TTT**T**T")
            self.__AllowedPatterns.append(TPattern)
            self.__AllowedSymbols.append("T")

def AttemptPuzzle(self):
        Finished = False
        while not Finished:
            self.DisplayPuzzle()
            print("Current score: " + str(self.__Score))
#-------------------------------------------------------------------------------------------------
            UndoUserInput = input('Would you like to undo your previous move? (y/N): ').lower()
            if UndoUserInput == 'y':
                self.__UndoPreviousMove()
#-------------------------------------------------------------------------------------------------
            Row = -1
            Valid = False
            while not Valid:
                try:
                    Row = int(input("Enter row number: "))
                    Valid = True
                except:
                    pass
            Column = -1
            Valid = False
            while not Valid:
                try:
                    Column = int(input("Enter column number: "))
                    Valid = True
                except:
                    pass
            Symbol = self.__GetSymbolFromUser()
            self.__SymbolsLeft -= 1
            CurrentCell = self.__GetCell(Row, Column)
            if CurrentCell.CheckSymbolAllowed(Symbol):
#-------------------------------------------------------------------------------------------------
                self.__StorePreviousMove(Row, Column, CurrentCell.GetSymbol())
#-------------------------------------------------------------------------------------------------
                CurrentCell.ChangeSymbolInCell(Symbol)
                AmountToAddToScore = self.CheckforMatchWithPattern(Row, Column)
                if AmountToAddToScore > 0:
                    self.__Score += AmountToAddToScore
            if self.__SymbolsLeft == 0:
                Finished = True
        print()
        self.DisplayPuzzle()
        print()
        return self.__Score
#-------------------------------------------------------------------------------------------------
    def __StorePreviousMove(self, Row, Column, Symbol):
        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
        PreviousCell = PreviousMove(Index, Symbol)
        self.__PreviousMoves.append(PreviousCell)
    
    def __UndoPreviousMove(self):
        if self.__PreviousMoves != []:
            PreviousCell = self.__PreviousMoves[-1]
            self.__Grid[PreviousCell.Index].ChangeSymbolInCell(PreviousCell.GetSymbol())
            del self.__PreviousMoves[-1]
            self.AttemptPuzzle()
        else:
            print('No moves have been played yet.')
          
class PreviousMove(Cell):
    def __init__(self, Index, Symbol):
        super(PreviousMove, self).__init__()
        self._Symbol = Symbol
        self.Index = Index
#-------------------------------------------------------------------------------------------------

    def AttemptPuzzle(self):
        Finished = False
        while not Finished:
            self.DisplayPuzzle()
            print("Current score: " + str(self.__Score))
#------------------------------------------------------------------------------------------------------------------------
            print(f'Symbols left: {self.__SymbolsLeft}')
            RemoveSymbolInput = input('Would you like to remove a symbol? (y/N): ').lower()
            if RemoveSymbolInput == 'y':
                Row = -1
                Valid = False
                while not Valid:
                    try:
                        Row = int(input("Enter row number of symbol you would like to remove: "))
                        Valid = True
                    except:
                        pass
                Column = -1
                Valid = False
                while not Valid:
                    try:
                        Column = int(input("Enter column number of symbol you would like to remove: "))
                        Valid = True
                    except:
                        pass
                self.__RemoveSymbol(Row, Column)
            else:
#------------------------------------------------------------------------------------------------------------------------
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
#------------------------------------------------------------------------------------------------------------------------
    def __RemoveSymbol(self, Row, Column):
        C = self.__GetCell(Row, Column)
        if C.IsEmpty() or C.CheckSymbolAllowed(C.GetSymbol()) == False:
            print('\nCannot remove an empty cell, blocked cell or a cell within part of a pattern.')
        else:
            C.ChangeSymbolInCell('-')
            self.__SymbolsLeft += 1
#------------------------------------------------------------------------------------------------------------------------

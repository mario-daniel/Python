    def CheckforMatchWithPattern(self, Row, Column):
        for StartRow in range(Row + 2, Row - 1, -1):
            for StartColumn in range(Column - 2, Column + 1):
                try:
                    PatternString = ""
#---------------------------------------------------------------------------------------------------------------------------------------------
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
#---------------------------------------------------------------------------------------------------------------------------------------------
                    for P in self.__AllowedPatterns:
                        CurrentSymbol = self.__GetCell(Row, Column).GetSymbol()
#---------------------------------------------------------------------------------------------------------------------------------------------
                        for cell in Pattern:
                            if cell.CheckSymbolAllowed(CurrentSymbol) or cell.GetSymbol() == '@':
#---------------------------------------------------------------------------------------------------------------------------------------------
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
                                    return 10
#---------------------------------------------------------------------------------------------------------------------------------------------
                            else:
                                print('Overlapping pattern!')
                                return 0
#---------------------------------------------------------------------------------------------------------------------------------------------
                except:
                    pass
        return 0

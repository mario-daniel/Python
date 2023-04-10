def EditSourceCode(SourceCode): 
  LineNumber = int(input("Enter line number of code to edit: "))
  print(SourceCode[LineNumber])
  Choice = EMPTY_STRING
  while Choice != "C":
    Choice = EMPTY_STRING
    while Choice != "E" and Choice != "C":
      print("E - Edit this line")
      print("C - Cancel edit")
      Choice = input("Enter your choice: ")
      Choice = Choice.upper()
    if Choice == "E":
      SourceCode[LineNumber] = input("Enter the new line: ")
      Line = SourceCode[LineNumber].replace(" ", EMPTY_STRING)
      IsSymbol = False
      for char in Line:
        if char == ":":
          NewLabel = Line[0:Line.find(char) + 1] + " "
          while len(NewLabel) != 7:
            NewLabel = " " + NewLabel
          Line = Line.replace(Line[0:Line.find(char) + 1], NewLabel)
          if "#" not in Line:
            if len(Line) > 10:
              Line = Line[0:10] + "  " + Line[10:]
            elif len(Line) < 10:
              NewLabel = Line[0:Line.find(char) + 1] + "     "
              Line = Line.replace(Line[0:Line.find(char) + 1], NewLabel)
          IsSymbol = True
        elif char == "#":
          NewOpcode = Line[0:Line.find(char) + 1] + " "
          while len(NewOpcode) != 12:
            NewOpcode = " " + NewOpcode
          Line = Line.replace(Line[0:Line.find(char) + 1], NewOpcode)
          IsSymbol = True
          break
      if IsSymbol == False:
        Line = Line[0:3] + "  " + Line[3:]
        NewOpcode = Line[0:3]
        while len(NewOpcode)!= 10:
          NewOpcode = " " + NewOpcode
        Line = Line.replace(Line[0:3], NewOpcode)
      SourceCode[LineNumber] = Line
    DisplaySourceCode(SourceCode)
  return SourceCode

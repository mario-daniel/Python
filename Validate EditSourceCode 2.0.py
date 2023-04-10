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
      NewLabel = input("Input a new LABEL (input NOTHING if no label): ")
      NewLabel = NewLabel.replace(" ", EMPTY_STRING)
      if NewLabel != EMPTY_STRING:
        if ":" not in NewLabel:
          NewLabel = NewLabel + ":"
      NewOpcode = input("Input a new OPCODE (input NOTHING if no opcode): ")
      NewOpcode = NewOpcode.replace(" ", EMPTY_STRING)
      NewOperand = input("Input a new OPERAND (input NOTHING if no operand): ")
      NewOperand = NewOperand.replace(" ", EMPTY_STRING)
      Line = EMPTY_STRING
      while len(NewLabel) != 6:
        NewLabel = " " + NewLabel
      while len(NewOpcode) != 5:
        NewOpcode = NewOpcode + " "
      Line = NewLabel + " " + NewOpcode + NewOperand
      SourceCode[LineNumber] = Line
    DisplaySourceCode(SourceCode)
  return SourceCode

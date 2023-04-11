def LoadFile(SourceCode): 
  FileExists = False
  SourceCode = ResetSourceCode(SourceCode)
  LineNumber = 0
  FileName = input("Enter filename to load: ")
  try:
    FileIn = open(FileName + ".txt", 'r')
    FileExists = True
    Instruction = FileIn.readline()
    while Instruction != EMPTY_STRING: 
      LineNumber += 1
      SourceCode[LineNumber] = Instruction[:-1] 
      Instruction = FileIn.readline()
    FileIn.close()
    SourceCode[0] = str(LineNumber)
  except:
    if not FileExists:
      print("Error Code 1")
    else:
      print("Error Code 2")
      SourceCode[0] = str(LineNumber - 1) 
  if LineNumber > 0:
    DisplaySourceCode(SourceCode)
  return SourceCode, FileName



def AssemblerSimulator():
  SourceCode = [EMPTY_STRING for Lines in range(HI_MEM)]
  Memory = [AssemblerInstruction() for Lines in range(HI_MEM)]
  SourceCode = ResetSourceCode(SourceCode)
  Memory = ResetMemory(Memory)
  Finished = False
  while not Finished:
    DisplayMenu()
    MenuOption = GetMenuOption()
    if MenuOption == 'L':
      FileName = EMPTY_STRING
      SourceCode, FileName = LoadFile(SourceCode)
      Memory = ResetMemory(Memory)
      print(FileName, "has been assembled succesfully.")
    elif MenuOption == 'D':
      if SourceCode[0] == EMPTY_STRING:
        print("Error Code 7")
      else:
        DisplaySourceCode(SourceCode)
    elif MenuOption == 'E':
      if SourceCode[0] == EMPTY_STRING:
        print("Error Code 8")
      else:
        SourceCode = EditSourceCode(SourceCode)
        Memory = ResetMemory(Memory)
    elif MenuOption == 'A':
      if SourceCode[0] == EMPTY_STRING:
        print("Error Code 9 - The Source Code is empty due to a file not loading correctly.")
      else:
        Memory = Assemble(SourceCode, Memory)
    elif MenuOption == 'R':
      if Memory[0].OperandValue == 0:
        print("Error Code 10")
      elif Memory[0].OpCode == "ERR":  
        print("Error Code 11")
      else:
        Execute(SourceCode, Memory) 
    elif MenuOption == 'X':
      Finished = True
    else:
      print("You did not choose a valid menu option. Try again")
  print("You have chosen to exit the program")

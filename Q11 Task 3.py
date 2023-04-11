def PassTwo(Memory, SymbolTable, NumberOfLines):
  for LineNumber in range(1, NumberOfLines + 1):
    Operand = Memory[LineNumber].OperandString
    if Operand != EMPTY_STRING:
      if Operand in SymbolTable:
        OperandValue = SymbolTable[Operand]
        Memory[LineNumber].OperandValue = OperandValue
      else:
        try:
          OperandValue = int(Operand)
          Memory[LineNumber].OperandValue = OperandValue
        except:
          print("Error Code 6 - The Line" + LineNumber + "does not have an integer or a label as the operand.")
          Memory[0].OpCode = "ERR"
  return Memory

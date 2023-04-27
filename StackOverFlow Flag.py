def ExecuteJSR(Memory, Registers, Address, SourceCode):
  while True:
    StackPointer = Registers[TOS] - 1
    if StackPointer <= int(SourceCode[0]):
      ReportRunTimeError("Stack Overflow", Registers)
      break
    else:
      Memory[StackPointer].OperandValue = Registers[PC] 
      Registers[PC] = Address 
      Registers[TOS] = StackPointer
      DisplayStack(Memory, Registers)
      break
  return Memory, Registers

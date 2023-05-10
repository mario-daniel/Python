def ExecuteJSR(Memory, Registers, Address, SourceCode):
  StackPointer = Registers[TOS] - 1
  if StackPointer <= int(SourceCode[0]):
    ReportRunTimeError("Overflow", Registers)
  else:
    Memory[StackPointer].OperandValue = Registers[PC] 
    Registers[PC] = Address 
    Registers[TOS] = StackPointer
    DisplayStack(Memory, Registers)
  return Memory, Registers

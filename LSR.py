def ExecuteLSR(Memory, Registers, Address):
  Binary = ConvertToBinary(Registers[ACC])
  Binary = Binary[:-(Memory[Address].OperandValue)]
  Registers[ACC] = ConvertToDecimal(Binary)
  if Registers[STATUS] == ConvertToDecimal("001"):
    ReportRunTimeError("Overflow", Registers)
  return Registers

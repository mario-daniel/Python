def ExecuteLSL(Memory, Registers, Address):
  Binary = ConvertToBinary(Registers[ACC])
  for i in range(Memory[Address].OperandValue):
    Binary += "0"
  Registers[ACC] = ConvertToDecimal(Binary)
  if Registers[STATUS] == ConvertToDecimal("001"):
    ReportRunTimeError("Overflow", Registers)
  return Registers

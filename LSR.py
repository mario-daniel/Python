def ExecuteLSR(Memory, Registers, Address):
  Binary = ConvertToBinary(Registers[ACC])
  Binary = Binary[:-(Memory[Address].OperandValue)]
  Registers[ACC] = ConvertToDecimal(Binary)
  return Registers

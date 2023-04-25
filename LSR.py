def ExecuteLSR(Memory, Registers, Address):
  Value = ConvertToBinary(Registers[ACC])
  Value = Value[:-(Memory[Address].OperandValue)]
  Registers[ACC] = ConvertToDecimal(Value)
  return Registers

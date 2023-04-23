def ExecuteLSL(Memory, Registers, Address):
  Value = ConvertToBinary(Registers[ACC] << Memory[Address].OperandValue)
  Value = Value[(Memory[Address].OperandValue):]
  Registers[ACC] = ConvertToDecimal(Value)
  return Registers

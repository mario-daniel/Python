def ExecuteLSL(Memory, Registers, Address):
  Value = ConvertToBinary(Registers[ACC] << Memory[Address].OperandValue)
  if len(Value) > 7:
    Value = Value[(len(Value) - 7):]
  Registers[ACC] = ConvertToDecimal(Value)
  return Registers

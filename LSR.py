def ExecuteLSR(Memory, Registers, Address):
  Value = ConvertToBinary(Registers[ACC])
  Value = Value[:-(Memory[Address].OperandValue)]
  if Value == EMPTY_STRING:
    Value = "0"
  Registers[ACC] = ConvertToDecimal(Value)
  return Registers

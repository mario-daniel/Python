#Right shifts the value in the accumulator by the amount of times of the operand value. Then slicing it to 7 bits as MAX_INT is 127.

def ExecuteLSR(Memory, Registers, Address):
  Value = ConvertToBinary(Registers[ACC])
  Value = Value[:-(Memory[Address].OperandValue)]
  if Value == EMPTY_STRING:
    Value = "0"
  Registers[ACC] = ConvertToDecimal(Value)
  return Registers

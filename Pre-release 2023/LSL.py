#Left shifts the value in the accumulator by the amount of times of the operand value. Then slicing it to 7 bits as MAX_INT is 127.

def ExecuteLSL(Memory, Registers, Address):
  Value = ConvertToBinary(Registers[ACC] << Memory[Address].OperandValue)
  if len(Value) > 7:
    Value = Value[(len(Value) - 7):]
  Registers[ACC] = ConvertToDecimal(Value)
  return Registers

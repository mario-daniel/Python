def ExecuteEOR(Memory, Registers, Address):
  BinaryACC = ConvertToBinary(Registers[ACC])
  BinaryOperand = ConvertToBinary(Memory[Address].OperandValue)
  Result = EMPTY_STRING
  while len(BinaryACC) < 7:
    BinaryACC = '0' + BinaryACC
  while len(BinaryOperand) < 7:
    BinaryOperand = '0' + BinaryOperand
  for Bit in range(7):
    if (BinaryACC[Bit] == "1" and BinaryOperand[Bit] == "0") or (BinaryOperand[Bit] == "1" and BinaryACC[Bit] == "0"):
      Result = Result + "1"
    else:
      Result = Result + "0"
  Registers[ACC] = ConvertToDecimal(Result)
  return Registers

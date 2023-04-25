def ExecuteAND(Memory, Registers, Address):
  BinaryACC = ConvertToBinary(Registers[ACC])
  BinaryOperand = ConvertToBinary(Memory[Address].OperandValue)
  Final = EMPTY_STRING
  while len(BinaryACC) < 7:
    BinaryACC = '0' + BinaryACC
  while len(BinaryOperand) < 7:
    BinaryOperand = '0' + BinaryOperand
  for Bit in range(7):
    if BinaryACC[Bit] == '1' and BinaryOperand[Bit] == '1':
      Final = Final + "1"
    else:
      Final = Final + "0"
  Registers[ACC] = ConvertToDecimal(Final)
  if Registers[STATUS] == ConvertToDecimal("001"):
    ReportRunTimeError("Overflow", Registers)
  return Registers

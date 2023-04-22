def ExecuteMVN(Registers):
  BinaryACC = ConvertToBinary(Registers[ACC])
  Result = EMPTY_STRING
  while len(BinaryACC) < 7:
    BinaryACC = '0' + BinaryACC
  for Bit in range(7):
    if BinaryACC[Bit] == 1:
      Result = Result + "0"
    else:
      Result = Result + "1"
  Registers[ACC] = ConvertToDecimal(Result)
  if Registers[STATUS] == ConvertToDecimal("001"):
    ReportRunTimeError("Overflow", Registers)
  return Registers

def ExecuteMVN(Registers):
  BinaryACC = ConvertToBinary(Registers[ACC])
  Result = EMPTY_STRING
  while len(BinaryACC) < 7:
    BinaryACC = '0' + BinaryACC
  for Bit in BinaryACC:
    if Bit == "1":
      Result += "0"
    else:
      Result += "1"
  Registers[ACC] = ConvertToDecimal(Result)
  return Registers

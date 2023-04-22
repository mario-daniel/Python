def ExecuteLSL(Registers):
  Binary = ConvertToBinary(Registers[ACC])
  Binary += "0"
  Registers[ACC] = ConvertToDecimal(Binary)
  return Registers

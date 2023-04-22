def ExecuteLSR(Registers):
  Binary = ConvertToBinary(Registers[ACC])
  Shifted = Binary[:-1]
  Shifted = "0" + Binary
  Registers[ACC] = ConvertToDecimal(Shifted)
  return Registers

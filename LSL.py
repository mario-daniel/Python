def ExecuteLSL(Memory, Registers, Address):
  Binary = ConvertToBinary(Registers[ACC])
  while len(Binary) < 7:
    Binary = "0" + Binary
  for i in range(Memory[Address].OperandValue):
    Binary += "0"
  if len(Binary) > 7:
    Binary = Binary[Memory[Address].OperandValue:]
  Registers[ACC] = ConvertToDecimal(Binary)
  if Registers[STATUS] == ConvertToDecimal("001"):
    ReportRunTimeError("Overflow", Registers)
  return Registers

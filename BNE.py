def ExecuteBNE(Registers, Address):
  StatusRegister = ConvertToBinary(Registers[STATUS])
  FlagZ = StatusRegister[0]
  if FlagZ != "1":
    Registers[PC] = Address
  return Registers

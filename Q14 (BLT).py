def ExecuteBLT(Registers, Address):
    StatusRegister = ConvertToBinary(Registers[STATUS])
    FlagN = StatusRegister[1]
    if FlagN == "1":
        Registers[PC] = Address
    return Registers

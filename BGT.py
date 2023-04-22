def ExecuteBGT(Registers, Address):
    StatusRegister = ConvertToBinary(Registers[STATUS])
    FlagN = StatusRegister[1]
    FlagZ = StatusRegister[0]
    if FlagN and FlagZ == "0":
        Registers[PC] = Address
    return Registers

#Checks if the operand is greater than the value in the accumulator.

def ExecuteBGT(Registers, Address):
    StatusRegister = ConvertToBinary(Registers[STATUS])
    FlagN = StatusRegister[1]
    FlagZ = StatusRegister[0]
    if FlagN == "0" and FlagZ == "0":
        Registers[PC] = Address
    return Registers

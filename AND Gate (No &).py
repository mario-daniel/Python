def ExtractOpCode(Instruction, LineNumber, Memory):
  if len(Instruction) > 9:
    OpCodeValues = ["LDA", "STA", "AND", "LDA#", "HLT", "ADD", "JMP", "SUB", "CMP#", "BEQ", "SKP", "JSR", "RTN", "   "]
    Operation = Instruction[7:10]
    if len(Instruction) > 10:
      AddressMode = Instruction[10:11]
      if AddressMode == '#':
        Operation += AddressMode
    if Operation in OpCodeValues:
      Memory[LineNumber].OpCode = Operation
    else:
      if Operation != EMPTY_STRING:
        print("Error Code 5")
        Memory[0].OpCode = "ERR"
  return Memory   

def ExecuteAND(Memory, Registers, Address):
  BinaryACC = ConvertToBinary(Registers[ACC])
  BinaryOperand = ConvertToBinary(Memory[Address].OperandValue)
  Final = EMPTY_STRING
  while len(BinaryACC) < 8:
    BinaryACC = '0' + BinaryACC
  while len(BinaryOperand) < 8:
    BinaryOperand = '0' + BinaryOperand
  for Bit in range(len(BinaryACC)):
    if BinaryACC[Bit] == '1' and BinaryOperand[Bit] == '1':
      Final = Final + "1"
    else:
      Final = Final + "0"
  Registers[ACC] = ConvertToDecimal(Final)
  if Registers[STATUS] == ConvertToDecimal("001"):
    ReportRunTimeError("Overflow", Registers)
  return Registers

def Execute(SourceCode, Memory): 
  Registers = [0, 0, 0, 0, 0] 
  Registers = SetFlags(Registers[ACC], Registers)
  Registers[PC] = 0 
  Registers[TOS] = HI_MEM
  FrameNumber = 0
  DisplayFrameDelimiter(FrameNumber)
  DisplayCurrentState(SourceCode, Memory, Registers)
  OpCode = Memory[Registers[PC]].OpCode
  while OpCode != "HLT":
    FrameNumber += 1
    print()
    DisplayFrameDelimiter(FrameNumber)
    Operand = Memory[Registers[PC]].OperandValue
    print("*  Current Instruction Register: ", OpCode, Operand)
    Registers[PC] = Registers[PC] + 1
    if OpCode == "LDA":
      Registers = ExecuteLDA(Memory, Registers, Operand)
    elif OpCode == "STA": 
      Memory = ExecuteSTA(Memory, Registers, Operand) 
    elif OpCode == "LDA#": 
      Registers = ExecuteLDAimm(Registers, Operand)
    elif OpCode == "AND":
      Registers = ExecuteAND(Memory, Registers, Operand)
    elif OpCode == "ADD":
      Registers = ExecuteADD(Memory, Registers, Operand)
    elif OpCode == "JMP": 
      Registers = ExecuteJMP(Registers, Operand)
    elif OpCode == "JSR":
      Memory, Registers = ExecuteJSR(Memory, Registers, Operand)
    elif OpCode == "CMP#":
      Registers = ExecuteCMPimm(Registers, Operand)
    elif OpCode == "BEQ":
      Registers = ExecuteBEQ(Registers, Operand) 
    elif OpCode == "SUB":
      Registers = ExecuteSUB(Memory, Registers, Operand)
    elif OpCode == "SKP":
      ExecuteSKP()
    elif OpCode == "RTN":
      Registers = ExecuteRTN(Memory, Registers)
    if Registers[ERR] == 0:
      OpCode = Memory[Registers[PC]].OpCode    
      DisplayCurrentState(SourceCode, Memory, Registers)
    else:
      OpCode = "HLT"
  print("Execution terminated")

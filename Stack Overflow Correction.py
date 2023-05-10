def DisplayStack(Stack):
  print("Stack contents:")
  print(" ----")
  for Index in reversed(Stack):
    print("|{:>3d} |".format(Index))
  print(" ----")

def ExecuteJSR(Memory, Registers, Address, Stack):
  StackPointer = Registers[TOS] - 1
  Stack.append(Registers[PC])
  Registers[PC] = Address 
  Registers[TOS] = StackPointer
  DisplayStack(Stack)
  return Memory, Registers

def ExecuteRTN(Registers, Stack, Index): 
  Registers[TOS] += 1
  Registers[PC] = Stack[-1]
  Stack.pop(-1)
  return Registers, Index
 
def Execute(SourceCode, Memory): 
  Registers = [0, 0, 0, 0, 0]
  Stack = []
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
    elif OpCode == "ADD":
      Registers = ExecuteADD(Memory, Registers, Operand)
    elif OpCode == "JMP": 
      Registers = ExecuteJMP(Registers, Operand)
    elif OpCode == "JSR":
      Memory, Registers = ExecuteJSR(Memory, Registers, Operand, Stack)
    elif OpCode == "CMP#":
      Registers = ExecuteCMPimm(Registers, Operand)
    elif OpCode == "BEQ":
      Registers = ExecuteBEQ(Registers, Operand) 
    elif OpCode == "SUB":
      Registers = ExecuteSUB(Memory, Registers, Operand)
    elif OpCode == "SKP":
      ExecuteSKP()
    elif OpCode == "RTN":
      Registers, Index = ExecuteRTN(Registers, Stack, Index)
    if Registers[ERR] == 0:
      OpCode = Memory[Registers[PC]].OpCode    
      DisplayCurrentState(SourceCode, Memory, Registers)
    else:
      OpCode = "HLT"
  print("Execution terminated")

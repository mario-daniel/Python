#This fixes the stack overflow in prog3 to work as intended. This is done by creating a new attribute to every object.

class AssemblerInstruction:
  def __init__(self):
    self.OpCode = EMPTY_STRING
    self.OperandString = EMPTY_STRING
    self.OperandValue = 0
    self.StackPointerValue = 0

def ExecuteJSR(Memory, Registers, Address): 
  StackPointer = Registers[TOS] - 1
  Memory[StackPointer].StackPointerValue = Registers[PC] 
  Registers[PC] = Address 
  Registers[TOS] = StackPointer
  DisplayStack(Memory, Registers)
  return Memory, Registers

def ExecuteRTN(Memory, Registers): 
  StackPointer = Registers[TOS]
  Registers[TOS] += 1 
  Registers[PC] = Memory[StackPointer].StackPointerValue
  return Registers

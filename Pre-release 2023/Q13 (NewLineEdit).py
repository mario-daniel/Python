#This is a validate source code that implements the user's new line they've inputted to the write format of the program.

def EditSourceCode(SourceCode): 
  LineNumber = int(input("Enter line number of code to edit: "))
  print(SourceCode[LineNumber])
  Choice = EMPTY_STRING
  while Choice != "C":
    Choice = EMPTY_STRING
    while Choice != "E" and Choice != "C":
      print("E - Edit this line")
      print("C - Cancel edit")
      Choice = input("Enter your choice: ")
    if Choice == "E":
      SourceCode[LineNumber] = NewLineEdit(SourceCode, LineNumber)
    DisplaySourceCode(SourceCode)
  return SourceCode
  
  
  
  def NewLineEdit(SourceCode, LineNumber):
  Line = SourceCode[LineNumber]
  Label = input("Enter Label or press enter: ").replace(" ", EMPTY_STRING)
  OpCode = input("Enter OpCode or press enter: ").replace(" ", EMPTY_STRING)
  Operand = input("Enter Operand or press enter: ").replace(" ", EMPTY_STRING)
  Comment = input("Enter Comment or press enter: ").strip()
  if "*" not in Comment and Comment != EMPTY_STRING:
    Comment = "*" + Comment
  while len(Label) != 6 and Label != EMPTY_STRING:
    Label = " " + Label
  while len(OpCode) != 4 and OpCode != EMPTY_STRING:
    OpCode = " " + OpCode
  if (Label and OpCode and Operand and Comment) == EMPTY_STRING:
    print("\nThere will be no changes made to the Source Code.\n")
  else:
    Line = Label + " " + OpCode + " " + Operand + " " + Comment
  return Line

#This is a validate source code that implements the user's new line they've inputted to the write format of the program. This program also implements a save file function which saves
#the new source code to either the same prog file loaded or create a new one.

def EditSourceCode(SourceCode):
    LineNumber = int(input("Enter line number of code to edit: "))
    print(SourceCode[LineNumber])
    Choice = EMPTY_STRING
    while Choice != "C":
        Choice = EMPTY_STRING
        while Choice != "E" and Choice != "C" and Choice != "S":
            print("E - Edit this line")
            print("C - Cancel edit")
            print("S - Save file")
            Choice = input("Enter your choice: ")
        if Choice == "E":
            SourceCode[LineNumber] = NewLineEdit(SourceCode, LineNumber)
        elif Choice == "S":
            SaveFile(SourceCode)
        DisplaySourceCode(SourceCode)
    return SourceCode

def SaveFile(SourceCode):
    FileName = input("Enter new filename: ")
    FileIn = open(FileName + ".txt", "w")
    for i in range(1,int(SourceCode[0]) + 1):
        FileIn.write(str(SourceCode[i])+"\n")

def NewLineEdit(SourceCode, LineNumber):
  Line = SourceCode[LineNumber]
  Label = input("Enter Label or press enter: ").replace(" ", EMPTY_STRING)
  OpCode = input("Enter OpCode or press enter: ").replace(" ", EMPTY_STRING)
  Operand = input("Enter Operand or press enter: ").replace(" ", EMPTY_STRING)
  Comment = input("Enter Comment or press enter: ").strip()
  if Label == EMPTY_STRING and OpCode == EMPTY_STRING and Operand == EMPTY_STRING and Comment == EMPTY_STRING:
    print("\nThere will be no changes made to the Source Code.\n")
  else:
   if ":" not in Label and Label != EMPTY_STRING:
      Label += ":"
   if "*" not in Comment and Comment != EMPTY_STRING:
      Comment = "*" + Comment
   while len(Label) != 6:
      Label = " " + Label
   while len(OpCode) != 4:
      OpCode += " "
   Line = Label + " " + OpCode + " " + Operand + " " + Comment
  return Line

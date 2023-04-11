def EditSourceCode(SourceCode): 
  LineNumber = int(input("Enter line number of code to edit: "))
  while LineNumber == 0:
    LineNumber = int(input("You cannot change the total number of lines. Please try again: "))
  print(SourceCode[LineNumber])
  Choice = EMPTY_STRING
  while Choice != "C":
    Choice = EMPTY_STRING
    while Choice != "E" and Choice != "C":
      print("E - Edit this line")
      print("C - Cancel edit")
      Choice = input("Enter your choice: ")
    if Choice == "E":
      SourceCode[LineNumber] = input("Enter the new line: ")
    DisplaySourceCode(SourceCode)
  return SourceCode

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
            SourceCode[LineNumber] = input("Enter the new line: ")
        elif Choice == "S":
            FileName = input("Enter new filename: ")
            FileIn = open(FileName + ".txt", "a")
            for i in range(1,int(SourceCode[0]) + 1):                                        
                FileIn.write(str(SourceCode[i])+"\n")
        DisplaySourceCode(SourceCode)
    return SourceCode

import random

def DisplayHelp():
    print()
    print('The aim of this game is to collect more than half of the seeds.')
    print('In the game you will identify a pit to pick up the seeds from.')
    print('These seeds are then dropped one by one into the following pits.')
    print('If the pit into which the last seed is dropped now contains 2 or 3 seeds the player collects them.')
    print('If the previous pit also has 2 or 3 seeds the player also collects these.')
    print('The player continues collecting seeds whilst any previous pit has 2 or 3 seeds.')
    
def CreateBoard(Seeds, PitCount):
    global Board
    for Count in range(PitCount):
        Board.append(Seeds // PitCount)

def SetupBoard(TypeOfBoard, Seeds=0, PitCount=0):
    global Board, State
    if TypeOfBoard == 'T':
        Board = [1, 0, 3, 1, 2, 2, 0, 0, 0, 0, 2, 1]
        State = [48, 16, 20]
    elif TypeOfBoard == 'S':
        CreateBoard(Seeds, PitCount)
        State = [Seeds, 0, 0]
    print("Your board is set up with", PitCount, "pits and", Seeds // PitCount, "seeds in each pit")

def DisplayBoard():
    global Board, State
    print(' ', end='')
    PitCount = len(Board)
    for Count in range(PitCount, PitCount // 2, -1):
        print('%2d' % (Count - 1), end='')
        print('  ', end='')
    print()
    print('-' * PitCount * 2)
    for Count in range(PitCount - 1, PitCount // 2 - 1, -1):
        print('|', end='')
        if Board[Count] < 10:
            print(' ', end='')
        print(Board[Count], end='')
        print('|', end='')
    print(' Player 1 holds:', State[1])
    print('-' * PitCount * 2)
    for Count in range(0, PitCount // 2):
        print('|', end='')
        if Board[Count] < 10:
            print(' ', end='')
        print(str(Board[Count]), end='')
        print('|', end='')
    print(' Player 2 holds:', State[2])
    print('-' * PitCount * 2)
    print(' ', end='')
    for Count in range(1, PitCount // 2 + 1):
        print('%2d' % (Count - 1), end='')
        print('  ', end='')
    print()
    print()

def GetMove(Player):
    global Board
    Pit = int(input('Player ' + str(Player) + ', which pit do you want to take seeds from? '))
    while Pit >= len(Board):
        print("Invalid")
        Pit = int(input('Player ' + str(Player) + ', which pit do you want to take seeds from? '))
    while Board[Pit] == 0:
        print ("Therer are 0 seeds in the selected pit. Choose another pit.")
        Pit = int(input('Player ' + str(Player) + ', which pit do you want to take seeds from? '))
    return Pit

def DropSeeds(Pit):
    global Board
    Seeds = Board[Pit]
    DropPit = Pit
    PitCount = len(Board)
    Board[Pit] = 0
    while Seeds > 0:
        DropPit = (DropPit + 1) % PitCount        
        if DropPit == Pit:
            DropPit = (DropPit + 1) % PitCount
        Board[DropPit] = Board[DropPit] + 1
        Seeds = Seeds - 1
    return DropPit

def BonusPoints(Pit, LastPit, PlayerOneSeeds, PlayerTwoSeeds):
    global Board
    Values = Board.count(Pit)
    while Board[LastPit] in [2, 3]:
        PlayerOneSeeds += 2

def MakeMove(Pit, Player):
    global Board, State
    LastPit = DropSeeds(Pit)
    while Board[LastPit] in [2, 3, 4]:
        print('Collected seeds from pit: ' + str(LastPit))
        State[Player] = State[Player] + Board[LastPit]
        Board[LastPit] = 0
        LastPit = LastPit - 1
        if LastPit == -1:
            LastPit = len(Board) - 1
    
def GetGameState(Player):
    global State
    TotalSeeds = State[0]
    PlayerOneSeeds = State[1]
    PlayerTwoSeeds = State[2]
    if  PlayerOneSeeds >= TotalSeeds // 2 + 1 or PlayerTwoSeeds >= TotalSeeds // 2 + 1:
        return 'Won'
    else:
        return 'Play'

def PlayGame(Player):
    global Board, State
    while GetGameState(Player) == 'Play':
        DisplayBoard()
        Pit = GetMove(Player)
        MakeMove(Pit, Player)
        if Player == 1:
            Player = 2
        else:
            Player = 1
    print(GetGameState(Player))
    Board = []
    State = []
    
def DisplayMenu():
    print()
    print('H - Help')
    print('S - Setup a basic board')
    print('B - Play a basic game')
    print('T - Play the test board')
    print('Q - Quit')
    print()

def GetInitialValues():
    print()
    PitCount = int(input('How many pits on the board? '))
    while PitCount > 100 or PitCount % 2 > 0:
        print("The Number of pits you have entered is invalid.")
        PitCount = int(input('How many pits on the board? '))
    Seeds = int(input('How many seeds for the game? '))
    while Seeds % PitCount != 0:
        print("The Number of seeds you have entered is invalid.")
        Seeds = int(input('How many seeds for the game? '))
    return Seeds, PitCount

def Main():
    global Board
    Playing = True
    while Playing:
        DisplayMenu()
        Choice = input('Choice: ')
        if Choice == 'H'or Choice == "h":
            DisplayHelp()
        elif Choice == 'S' or Choice == "s":
            Seeds, PitCount = GetInitialValues()
            SetupBoard('S', Seeds, PitCount)
        elif Choice == 'B' or Choice == "b":
            if len(Board) != 0:
                Player = random.randint(1, 2)
                PlayGame(Player)
            else:
                print('You need to setup a board first')
        elif Choice == 'T' or Choice == "t":
            SetupBoard('T')
            Player = 1
            PlayGame(Player)
        elif Choice == 'Q' or Choice == "q":
            Playing = False
        else:
          print("Invalid Choice! ")
          print("Enter a choice provided from the main menu")
          continue

if __name__ == '__main__':
    Board = []
    State = []
    Main()
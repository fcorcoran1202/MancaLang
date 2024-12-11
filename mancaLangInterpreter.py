import random

#Vars

Board = {}
P1Pits = []
P2Pits = []
NextPit = {}
OppositePit = {}
ReversePit = {}
CaptureRules = {}
TurnRules = {}
MultiplierRules = {}
Reverse = False
Random = False
Turn = '1'
Pits = 12
Seeds = 4

def interpret(filename):
    global Pits, Seeds, Random, Reverse, P1Pits, P2Pits, NextPit, OppositePit, ReversePit, CaptureRules, TurnRules, MultiplierRules
    
    for i in range(1, Pits + 1):
        CaptureRules[str(i)] = False
        TurnRules[str(i)] = False
        MultiplierRules[str(i)] = 1

    file = open(filename)
    lines = file.readlines()

    hasBoard = False
    hasRules = False
    hasPlay = False
    BoardLine = 0
    RulesLine = 0
    PlayLine = 0
    for count, l in enumerate(lines):
        if l.startswith('Board'):
            hasBoard = True
            BoardLine = count
        elif l.startswith('Rules'):
            hasRules = True
            RulesLine = count
        elif l.startswith('Play'):
            hasPlay = True
            PlayLine = count

    if not (hasBoard and hasRules and hasPlay):
        raise Exception('Missing or incorrect label(s)')

    for i in range(BoardLine + 1, RulesLine):
        if lines[i].strip().startswith('Pits'):
            Pits = int(lines[i].split()[1])
            if not (Pits % 2 == 0):
                raise Exception('Amount of pits must be even.')
            if (Pits < 2):
                raise Exception('Must have at least 2 pits.')
        elif lines[i].strip().startswith('Seeds'):
            Seeds = int(lines[i].split()[1])
            if (Seeds < 1):
                raise Exception('Amount of seeds must be greater than 0.')
        elif lines[i].strip().startswith('#'):
            continue
        else:
            raise Exception('Language not supported: \'' + lines[i] + '\'')

    for i in range(RulesLine + 1, PlayLine):
        if lines[i].strip().startswith('Capture'):
            CaptureRules[lines[i].split()[4]] = True
            if (int(lines[i].split()[4]) > Pits or int(lines[i].split()[4]) < 2):
                raise Exception('Must be within amount of pits.')
        elif lines[i].strip().startswith('ExtraTurn'):
            if (int(lines[i].split()[4]) > Pits or int(lines[i].split()[4]) < 2):
                raise Exception('Must be within amount of pits.')
            TurnRules[lines[i].split()[4]] = True
        elif lines[i].strip().startswith('Multiply'):
            MultiplierRules[lines[i].split()[1]] = int(lines[i].split()[3])
            if (int(lines[i].split()[1]) > Pits or int(lines[i].split()[1]) < 2):
                raise Exception('Must be within amount of pits.')
        elif lines[i].strip() == 'Reverse':
            Reverse = True
        elif lines[i].strip() == 'Randomize':
            Random = True
        elif lines[i].strip().startswith('#'):
            continue
        else:
            raise Exception('Language not supported: \'' + lines[i] + '\'')
        
    play(Pits, Seeds, Random)
        
def newBoard(p,s,r):
    
    b = {'Store1' : 0 , 'Store2' : 0}
    
    if r:
        for i in range (1, p + 1):
            b[str(i)] = random.randint(1,s)
    else:
        for i in range (1, p + 1):
            b[str(i)] = s

    for i in range (1, int(p / 2)):
        NextPit[str(i)] = str(i + 1)
        NextPit[str(p - i + 1)] = str(p - i)
    NextPit['Store1'] = str(p)
    NextPit['Store2'] = '1'
    NextPit[str(int(p / 2))] = 'Store1'
    NextPit[str(int(p / 2) + 1)] = 'Store2'

    for i in range (1, int(p / 2)):
        ReversePit[str(i + 1)] = str(i)
        ReversePit[str(p - i)] = str(p - i + 1)
    ReversePit[str(p)] = 'Store1'
    ReversePit['1'] = 'Store2'
    ReversePit['Store1'] = str(int(p / 2))
    ReversePit['Store2'] = str(int(p / 2) + 1)

    for i in range (1, int(p / 2) + 1):
        OppositePit[str(i)] = str(i + int(p / 2))
        OppositePit[str(i + int(p / 2))] = str(i)

    for i in range (1, (int)(p / 2) + 1):
        P1Pits.append(str(i))
        P2Pits.append(str(i + int(p / 2)))

    return b

def displayBoard(b, p, r):
    
    print('\n' * 10)
    
    pit_width = max(len(str(k)) for k in b.keys()) + 5
    
    print(' ', end='')
    print('*' * (pit_width * int(p / 2) + 10))
    
    if r:
        print(' ' * (pit_width * int(p / 2) - 6) + '>> Player 2')
    else:
        print(' ' * (pit_width * int(p / 2) - 6) + '<< Player 2')
    
    print('     |', end=' ')
    for i in range(int(p / 2) + 1, p + 1):
        if i < 10:
            print(f"{i} : {b[str(i)]:<4}", end=' | ')
        else:
            print(f"{i} : {b[str(i)]:<4}", end='| ')
    print()
    
    print('     |', end=' ')
    for i in range(1, int(p / 2) + 1):
        if i < 10:
            print(f"{i} : {b[str(i)]:<4}", end=' | ')
        else:
            print(f"{i} : {b[str(i)]:<4}", end='| ')
    print()
    
    if r:
        print(' ' * (pit_width * int(p / 2) - 6) + '<< Player 1')
    else:
        print(' ' * (pit_width * int(p / 2) - 6) + '>> Player 1')
    
    print(' ', end='')
    print('*' * (pit_width * int(p / 2) + 10))
    
    print(' ' * (pit_width * int(p / 6) - 6) + f" PIT : SEED    Store 2: {b['Store2']}    |    Store 1: {b['Store1']}")
    print('\n' * 2)

def getMove(turn, b, p):

    while True:  
        if turn == '1':
            print('P1, choose move: 1-' + str((int)(p/2)))
        elif turn == '2':
            print('P2, choose move: ' + str(int((p/2)+1)) + '-' + str(p))
        move = input().strip().upper()

        if move in {'QUIT', 'END', 'EXIT', 'STOP', 'LEAVE'}:
            quit()

        if (turn == '1' and move not in P1Pits) or (turn == '2' and move not in P2Pits):
            print('Pit must be on your side of the board.')
            continue
        if b[move] == 0:
            print('Pit must be non-empty.')
            continue
        return move
    
def makeMove(turn, b, p, r):

    sow = b[p]
    sow = int(sow)
    m = MultiplierRules[p]
    b[p] = 0

    if r:
        while sow > 0:
            p = ReversePit[p]
            if (turn == '1' and p == 'Store2') or (
                turn == '2' and p == 'Store1'
            ):
                continue
            b[p] += (1 * m)
            sow -= 1
    else:
        while sow > 0:
            p = NextPit[p]
            if (turn == '1' and p == 'Store2') or (
                turn == '2' and p == 'Store1'
            ):
                continue
            b[p] += (1 * m)
            sow -= 1

    if (turn == '1' and p == 'Store1') or (turn == '2' and p == 'Store2'):
        return turn

    if turn == '1' and p in P1Pits and b[p] == 1 and CaptureRules[p]:
        o = OppositePit[p]
        b['Store1'] += b[o]
        b[o] = 0
    elif turn == '2' and p in P2Pits and b[p] == 1 and CaptureRules[p]:
        o = OppositePit[p]
        b['Store2'] += b[0]
        b[o] = 0

    if (TurnRules[p] and b[p] == 1):
        return turn

    if turn == '1':
        return '2'
    elif turn == '2':
        return '1'
    
def checkWinner(b, p):

    player1Total = 0
    player2Total = 0

    for i in range(1, int(p / 2) + 1):
        player1Total += b[str(i)]
        player2Total += b[str(i + int(p / 2))]

    if player1Total == 0:
        b['Store2'] += player2Total
        for p in P2Pits:
            b[p] = 0
    elif player2Total == 0:
        b['Store1'] += player1Total
        for p in P1Pits:
            b[p] = 0
    else:
        return 'undecided'
 
    if b['Store1'] > b['Store2']:
        return '1'
    elif b['Store2'] > b['Store1']:
        return '2'
    else:
        return 'tie'
    
def play(p, s, r):
    Board = newBoard(p, s, r)
    turn = '1'

    while True:
        
        displayBoard(Board, p, Reverse)
        move = getMove(turn, Board, p)
        turn = makeMove(turn, Board, move, Reverse)
        winner = checkWinner(Board, p)

        if winner == '1' or winner == '2':
            displayBoard(Board, p, Reverse)
            print('Player ' + winner + ' wins')
            quit()
        elif winner == 'tie':
            displayBoard(Board, p, Reverse)
            print(winner)
            quit()

interpret('testprog1.manca')





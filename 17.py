
from utils import readInput, Pt
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('--part2', action='store_true')
args = ap.parse_args()

text = readInput()

W = 7
if args.part2:
    TARGET_ROCKS = 1000000000000
else:
    TARGET_ROCKS = 2022

rocks = [[c for c in x.split('\n')] for x in [
    '####',

    '.#.\n'
    '###\n'
    '.#.',
    
    '..#\n'
    '..#\n'
    '###',
    
    '#\n'
    '#\n'
    '#\n'
    '#',
    
    '##\n'
    '##'
]]

#H = 2023 * 4
H = 1000 # Estimated to be large enough
board = [['.' for _ in range(W)] for _ in range(H)]

def engrave(board, rock, pos: Pt):
    for ry in range(len(rock)):
        for rx in range(len(rock[0])):
            if rock[ry][rx] == '#':
                board[len(board) - 1 - pos.y - len(rock) + 1 + ry][pos.x + rx] = '#'

def checkCollision(board, rock, pos: Pt):
    if pos.y < 0:
        return True # Floor collision
    if pos.x < 0:
        return True # Left wall collision
    if pos.x + len(rock[0]) > len(board[0]):
        return True # Right wall collision
    for ry in range(len(rock)):
        for rx in range(len(rock[0])):
            if rock[ry][rx] == '#':
                if board[len(board) - 1 - pos.y - len(rock) + 1 + ry][pos.x + rx] == '#':
                    return True
    return False

def board2str(board):
    return '\n'.join(''.join(line) for line in board)

def printBoard(board, h = None):
    if h == None:
        h = len(board)
    print(board2str(board[-h:]))
    print('-' * len(board[0]))

def cleanBoard(board, topY):
    sl0 = ['@' for _ in range(len(board[0]))]
    h = 0
    while any(c == '@' for c in sl0):
        targetY = len(board) - 1 - topY + h
        if targetY >= len(board):
            sl1 = ['#' for _ in range(len(board[0]))] # Floor
        else:
            sl1 = board[targetY][:]
        # Spread down
        for i in range(len(sl0)):
            if sl0[i] == '@' and sl1[i] == '.':
                sl1[i] = '@'
        # Spread sideways
        for i in range(len(sl1)):
            if sl1[i] == '@':
                if i < len(sl1)-1 and sl1[i+1] == '.':
                    sl1[i+1] = '@'
        for i in reversed(range(len(sl1))):
            if sl1[i] == '@':
                if i > 0 and sl1[i-1] == '.':
                    sl1[i-1] = '@'
        sl0 = sl1
        h += 1
    return h - 2

topY = 0
windList = text.strip()
curRock = -1
curWind = 0

totCleaned = 0

states = {}

newRock = True
nRocks = 0
while True:
    if newRock:
        droppingRock = Pt(2, 3 + topY)
        curRock += 1
        curRock %= len(rocks)
        nRocks += 1
        newRock = False
    # Wind
    wind = windList[curWind]
    curWind += 1
    curWind %= len(windList)
    newPos = droppingRock + (Pt(1, 0) if wind == '>' else Pt(-1, 0))
    if not checkCollision(board, rocks[curRock], newPos):
        droppingRock = newPos
    # Gravity
    newPos = droppingRock + Pt(0, -1)
    if not checkCollision(board, rocks[curRock], newPos):
        droppingRock = newPos
    else:
        engrave(board, rocks[curRock], droppingRock)
        #printBoard(board, 20)
        topY = max(topY, droppingRock.y + len(rocks[curRock]))
        # Cleanup board
        keepSize = cleanBoard(board, topY)
        if keepSize < topY:
            if keepSize > 0:
                board[-keepSize:] = board[-topY:-topY+keepSize]
                board[-topY:-keepSize] = [['.' for _ in range(W)] for _ in range(topY - keepSize)]
            else:
                board[-topY:] = [['.' for _ in range(W)] for _ in range(topY)]
            totCleaned += topY - keepSize
            topY = keepSize
        # SAVE CLEAN STATE
        state = (board2str(board[-topY:]), curRock, curWind)
        myScore = topY + totCleaned
        if state in states:
            prevScore, prevRocks = states[state]
            rockInc = nRocks - prevRocks
            scoreInc = myScore - prevScore
            steps = (TARGET_ROCKS - nRocks) // rockInc
            if steps > 0:
                print(f'Recursion at {nRocks} rocks')
                print(f'Fast forwarding by increment of {rockInc} rocks doing {steps} steps')
                nRocks += rockInc * steps
                totCleaned += scoreInc * steps
        states[state] = (myScore, nRocks)

        if nRocks % 500 == 0:
            print(f'...{nRocks}')
        if nRocks == TARGET_ROCKS:
            break
        newRock = True

printBoard(board, 20)
print(f'Height: {topY + totCleaned}')

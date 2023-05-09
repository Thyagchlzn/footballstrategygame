import random
# Generates a Random number from 0 to 2^64-1
def randomInt():
    min = 0
    max = pow(2, 64)
    return random.randint(min, max)


# This function associates each piece with
# a number
def indexOf(piece):
    if (piece == 1):
        return 0
    elif (piece == 2):
        return 1
    elif (piece == 3):
        return 2
    elif (piece == 6):
        return 3
    elif (piece == 7):
        return 4
    elif (piece == 8):
        return 5
    elif (piece == 9):
        return 6
    elif (piece == 10):
        return 7
    elif (piece == -1):
        return 8
    elif (piece == -2):
        return 9
    elif (piece == -3):
        return 10
    elif (piece == -6):
        return 11
    elif (piece == -7):
        return 12
    elif (piece == -8):
        return 13
    elif (piece ==-9):
        return 14
    elif (piece ==-10):
        return 15
    else:
        return -1


# Initializes the table
def initTable():
    # 14x7x14 array
    ZobristTable = [[[randomInt() for k in range(16)] for j in range(7)] for i in range(14)]
    return ZobristTable


# Computes the hash value of a given board
def computeHash(board, ZobristTable):
    h = 0
    for i in range(14):
        for j in range(7):
            if (board[i][j] != 0):
                piece = indexOf(board[i][j])
                h ^= ZobristTable[i][j][piece]
    return h
def updateHash(hashvalue,ZobristTable,move):
    hashvalue ^= ZobristTable[move.srow][move.scol][indexOf(move.piecemoved)]
    hashvalue ^= ZobristTable[move.erow][move.ecol][indexOf(move.piecemoved)]

    return hashvalue
def updateHashundo(hashvalue,ZobristTable,move):
    hashvalue ^= ZobristTable[move.erow][move.ecol][indexOf(move.piecemoved)]
    hashvalue ^= ZobristTable[move.srow][move.scol][indexOf(move.piecemoved)]


    return hashvalue
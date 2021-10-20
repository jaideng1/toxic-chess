import chess
import chess.engine
import re #regex
import math
import utils

board = None
engine = chess.engine.SimpleEngine.popen_uci("stockfish")
limit = chess.engine.Limit(time=0.1)

symbols = {
    "pawn": "",
    "knight": "N",
    "king": "K",
    "queen": "Q",
    "rook": "R",
    "bishop": "B"
}

nameCoords = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h"
]

#Reset the board.
def resetBoard():
    global board
    board = chess.Board()

#Returns the board.
def getBoard():
    return board

#Turns grid coords to a UCI move.
def gridToUCI(gridFrom, gridTo):
    return chess.Move.from_uci(gridNToChessCoord(gridFrom) + gridNToChessCoord(gridTo))

#Makes a move using two grid numbers
def makeMove(gridFrom, gridTo):
    move = gridToUCI(gridFrom, gridTo)
    board.push(move)
    return move

def makeUCIMove(p1, p2):
    board.push(chess.Move.from_uci(p1 + p2))

def getLetterDistance(p1, p2):
    return abs(nameCoords.index(utils.split(p1)[0]) - nameCoords.index(utils.split(p2)[0]))

def getUnchangedLetterDistance(p1, p2):
    return nameCoords.index(utils.split(p1)[0]) - nameCoords.index(utils.split(p2)[0])

#Unmakes the last move.
def unmakeLastMove():
    unmadeMove = board.pop()
    return unmadeMove

#Returns if that's a possible move.
def isPossibleMove(gridFrom, gridTo):
    legalMoves = board.legal_moves
    move = gridToUCI(gridFrom, gridTo)
    return move in legalMoves

def makeEngineMove():
    move = engine.play(board, limit)
    board.push(move.move)
    return move

#Returns if the board is in check.
def inCheck():
    return board.is_check()

#Returns if the game has finished or not.
#Is not tracking time though.
def gameHasFinished():
    return board.is_game_over()

#Returns the outcome of the game.
def getGameOutcome():
    return board.outcome()

#Converts a grid number to a chess coordinate.
def gridNToChessCoord(gridN):
    y = 7 - math.floor(gridN / 8)
    x = gridN % 8 + 1

    return nameCoords[y] + str(x)

def chessCoordToGridN(chessCoord):
    splt = utils.split(chessCoord)
    letter_n = nameCoords.index(splt[0])
    num = int(splt[1]) - 1
    return ((7 - letter_n) * 8) + num

def uciToSplit(move):
    return re.findall('.{1,2}', str(move.move))

def uciSplitStr(st):
    return re.findall('.{1,2}', str(st))

def getTeam(t):
    if t == "white": return chess.WHITE
    else: return chess.BLACK

#Just play them against eachother.
if __name__ == "__main__":
    print(chessCoordToGridN("a1"))
    #print(gridNToChessCoord(57))

    # resetBoard()
    # print(board)
    # while not gameHasFinished():
    #     mv = makeEngineMove()
    #     print(str(uciToSplit(mv)))
    #     print("#################")
    #     print(board)
    # engine.quit()
    # print("#### FINAL RESULT ####")
    # print("Winner: ")
    # winner = getGameOutcome().winner
    # print(getGameOutcome())
    # if winner == chess.WHITE:
    #     print("White!")
    # elif winner == chess.BLACK:
    #     print("Black!")
    # else:
    #     print("Draw!")
    # print("Final Board:")
    # print(board)
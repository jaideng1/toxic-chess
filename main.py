#imports
from re import sub
import cv2
import numpy as np
import contours as ct
import threading
#import menu 
# Using display instead of menu.
import display
import chess_manager as chess
import insults
import time
from dataclasses import dataclass

#Colors
lower_blue = np.array([100,128,0])
upper_blue = np.array([215,255,255])

lower_white = np.array([0,0,128], dtype=np.uint8)
upper_white = np.array([255,255,255], dtype=np.uint8)

lower_black = np.array([0,0,0], dtype=np.uint8)
upper_black = np.array([170,150,50], dtype=np.uint8)

upper_orange = np.array([237, 179, 147])
lower_orange = np.array([232, 83, 2])

lower_red = np.array([170,50,50])
upper_red = np.array([180,255,255])

lower_green = np.array([40, 40,40])
upper_green = np.array([70, 255,255])

lower_yellow = np.array([22, 93, 0])
upper_yellow = np.array([45, 255, 255])

#Cords
letter_cords = [
    "h",
    "g",
    "f",
    "e",
    "d",
    "c",
    "b",
    "a",
]

names = [
    "pawns",
    "rooks",
    "knights",
    "queen",
    "king",
    "bishops"
]

#Pieces
piece_tracker = {
    "white": {
        'pawns': [1, 9, 17, 25, 33, 41, 49, 57],
        'rooks': [0, 56],
        'knights': [8, 48],
        'bishops': [16, 40],
        'queen': [32],
        'king': [24]
    },
    "black": {
        'pawns': [6, 14, 22, 30, 38, 46, 54, 62],
        'rooks': [7, 63],
        'knights': [15, 55],
        'bishops': [23, 47],
        'queen': [39],
        'king': [31]
    }
}

#Fonts
font = cv2.FONT_HERSHEY_PLAIN

#Cam
cap = None

cam = 2 #3

width = 0
height = 0

#start camera
cap = cv2.VideoCapture(cam)

if cap.isOpened():
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#adjusts the box to the middle
gridXAdj = round(width / 2 - (height / 2))

#Check if two numbers are similar
def similar(n1, n2):
    return n1 > n2 - (n2 / 100) and n1 < n2 + (n2 / 100)

boxWAdj = 10
boxHAdj = 10

#Get which section a piece is in.
def getContourSection(contour):
    (x, y, w, h) = cv2.boundingRect(contour) 

    if w < 50 and h < 50:
        return -1

    boxW = round(width / 8)
    boxH = round(height / 8)

    if boxW > boxH:
        boxW = boxH
    else:
        boxH = boxW

    boxW -= boxWAdj
    boxH -= boxHAdj
    
    for y_ in range(8):
        for x_ in range(8):
            adjX = int(x_ * boxW) + gridXAdj
            adjY = int(y_ * boxH)

            midX = x + (w / 2)
            midY = y + (h / 2)

            if midX > adjX and midX < adjX + boxW and midY > adjY and midY < adjY + boxH:
                return x_ + (y_ * 8)

    return -1

#Sort the contours
def sortContours(contours): 
    contours = sorted(contours, key=getContourSection)
    return contours

#Finds the moved pieces.
def getMissingPieces(contours):
    boxW = round(width / 8)
    boxH = round(height / 8)

    if boxW > boxH:
        boxW = boxH
    else:
        boxH = boxW

    boxW -= boxWAdj
    boxH -= boxHAdj

    recordedPieces = []

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour) 
        if w < 30 and h < 30: continue
        section = getContourSection(contour)
        if section == -1: continue
        recordedPieces.append(section)

    missingPieces = []

    for y_ in range(8):
        for x_ in range(8):
            gn = x_ + (y_ * 8)
            if supposedToBeAPieceHere(gn) and gn not in recordedPieces:
                missingPieces.append(gn)

    return missingPieces

#Finds a piece in a new slot.
def getPieceInNewSlot(contours):
    boxW = round(width / 8)
    boxH = round(height / 8)

    if boxW > boxH:
        boxW = boxH
    else:
        boxH = boxW

    boxW -= boxWAdj
    boxH -= boxHAdj

    recordedPieces = []

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour) 
        if w < 30 and h < 30: continue
        section = getContourSection(contour)
        if section == -1: continue
        recordedPieces.append(section)

    missing = []

    for y_ in range(8):
        for x_ in range(8):
            gn = (y_ * 8) + x_
            if not supposedToBeAPieceHere(gn) and gn in recordedPieces:
                print("found " + str(gn))
                missing.append(gn)
                #break
    
    return missing

#Gets the piece
def getPieceByCoord(gridN):
    global piece_tracker, names
    for piece in names:
        subLen = len(piece_tracker['white'][piece])
        for i in range(subLen):
            if piece_tracker['white'][piece][i] == int(gridN):
                return {
                    'side': 'white',
                    'type': piece,
                    'n': i
                }
            if piece_tracker['black'][piece][i] == int(gridN):
                return {
                    'side': 'black',
                    'type': piece,
                    'n': i
                }
            
    return {
        'side': None,
        'type': None,
        'n': -1
    }

#Checks to see if there's supposed to be a piece in a grid.
def supposedToBeAPieceHere(gridN):
    global piece_tracker
    for piece in names:
        subLen = len(piece_tracker['white'][piece])
        for i in range(subLen):
            if piece_tracker['white'][piece][i] == gridN:
                return True
            if piece_tracker['black'][piece][i] == gridN:
                return True
    return False

def main():
    #get the camera
    ret, frame = cap.read()

    #mirror the camera
    frame = cv2.flip(frame, 1)

    #get the blue
    blue_frame = ct.getColor(frame, lower_blue, upper_blue)
    #get the green
    green_frame = ct.getColor(frame, lower_green, upper_green)
    #get yellow frame
    yellow_frame = ct.getColor(frame, lower_yellow, upper_yellow)

    #get the blue frame contours
    contours = ct.getContours(frame, blue_frame)

    #draw the yellow contours
    frame = ct.drawContours(frame, yellow_frame, 50, (width * height) * 0.75)

    #get the yellow contours
    yellow_contours = sortContours(ct.getContours(frame, yellow_frame))

    i = 0
    for contour in yellow_contours:
        (x, y, w, h) = cv2.boundingRect(contour) 

        if (w * h) > (width * height) * 0.75:
            continue

        contourSection = getContourSection(contour)

        if contourSection == -1: continue

        textX = x + (w / 2)
        textY = y + (h / 2)

        cv2.putText(frame, str(contourSection), (int(textX), int(textY)), font, 4, (255, 82, 212), 4, cv2.LINE_4)
        i += 1

    boxW = round(width / 8)
    boxH = round(height / 8)

    if boxW > boxH:
        boxW = boxH
    else:
        boxH = boxW

    boxW -= boxWAdj
    boxH -= boxHAdj

    #draw a "board" graphic over
    for y in range(8):
        for x in range(8):
            adjX = int(x * boxW) + gridXAdj
            adjY = int(y * boxH)
            cv2.rectangle(frame, (adjX, adjY), (adjX + boxW, adjY + boxH), (20, 20, 20), 2)
            cv2.putText(frame, str(x + (y * 8)), (int(adjX + (boxW / 2)), int(adjY + (boxH / 2))), font, 1, (0,255,0), 2, cv2.LINE_4)

    #show the frame
    cv2.imshow('camera', frame)

    #Update the menu.
    # menu.update()

    if display.justStarted():
        print("Started.")

    if display.isPlaying():
        if display.justChangedTurns():
            if display.getTurn() == "black":
                print("#### CALC WHITE'S PIECES ####")
                print("Turn just changed to black.")

                #Choose a move, and then change the turn.
                missing = getMissingPieces(yellow_contours)

                if len(missing) > 2:
                    #Insult -> illegal moves.
                    print("More than 2 pieces moved, illegal. missing: " + str(missing))
                    insults.illegalPlayInsult()
                    display.forceChangeTurn("white")
                
                #TODO: Check if castle.
                if len(missing) == 2:
                    print("Maybe castle? ", str(missing))

                    piece_1 = getPieceByCoord(missing[0])
                    piece_2 = getPieceByCoord(missing[1])

                    if (piece_1['type'] == "rooks" and piece_2['type'] == 'king') or (piece_1['type'] == "king" and piece_2['type'] == 'rooks'):
                        print("Castled.")

                        if not chess.getBoard().has_castling_rights(chess.getTeam('white')):
                            insults.illegalPlayInsult()
                            insults.play(insults.createNewRecording('you don\'t have castling rights poopyhead'))
                            display.forceChangeTurn('white')
                            return False

                        print("possible castling pieces: " + str(piece_tracker[piece_1['side']][piece_1['type']][piece_1['n']]), str(piece_tracker[piece_2['side']][piece_2['type']][piece_2['n']]))

                        if piece_tracker[piece_1['side']][piece_1['type']][piece_1['n']] == 0 or piece_tracker[piece_2['side']][piece_2['type']][piece_2['n']] == 0:
                            if piece_1['type'] == "rooks":
                                piece_tracker[piece_1['side']][piece_1['type']][piece_1['n']] = 16
                                piece_tracker[piece_2['side']][piece_2['type']][piece_2['n']] = 8
                            if piece_1['type'] == "king":
                                piece_tracker[piece_1['side']][piece_1['type']][piece_1['n']] = 8
                                piece_tracker[piece_2['side']][piece_2['type']][piece_2['n']] = 16
                            chess.makeUCIMove("e1", "g1")
                        else:
                            print("(Queen Side)")
                            if not chess.getBoard().has_queenside_castling_rights(chess.getTeam('white')):
                                insults.illegalPlayInsult()
                                insults.play(insults.createNewRecording('you don\'t have queenside castling rights poop'))
                                display.forceChangeTurn('white')
                                return False

                            if piece_1['type'] == "rooks":
                                piece_tracker[piece_1['side']][piece_1['type']][piece_1['n']] = 32
                                piece_tracker[piece_2['side']][piece_2['type']][piece_2['n']] = 40
                            if piece_1['type'] == "king":
                                piece_tracker[piece_1['side']][piece_1['type']][piece_1['n']] = 40
                                piece_tracker[piece_2['side']][piece_2['type']][piece_2['n']] = 32
                            
                            chess.makeUCIMove("e1", "c1")
                        
                        print("### CALC BLACK'S MOVE ###")

                        engine_mv = chess.makeEngineMove()
                        
                        if chess.getBoard().is_castling(engine_mv.move):
                            print("Engine castled")
                            kingside_rook = getPieceByCoord(7)
                            queenside_rook = getPieceByCoord(63)
                            if chess.getBoard().is_kingside_castling(engine_mv.move):
                                piece_tracker['black']['rooks'][kingside_rook['n']] = 23
                                piece_tracker['black']['king'][0] = 15
                            else:
                                piece_tracker['black']['rooks'][queenside_rook['n']] = 39
                                piece_tracker['black']['king'][0] = 47
                        else:
                            move = chess.uciToSplit(engine_mv)

                            print("Generated move from engine: " + str(move))
                            
                            frm = chess.chessCoordToGridN(move[0])
                            to = chess.chessCoordToGridN(move[1])

                            print("From " + str(frm) + " to " + str(to) + " (Grid Numbers)")

                            frm_piece = getPieceByCoord(frm)

                            print(str(frm_piece), str(frm), str(to))

                            #Check if there is a piece already at that spot, if so, 'remove' it.
                            if getPieceByCoord(to)['n'] > -1:
                                piece = getPieceByCoord(to)
                                piece_tracker[piece['side']][piece['type']][int(piece['n'])] = -15331462
                            
                            #Update the piece tracker to black's move
                            piece_tracker[frm_piece['side']][frm_piece['type']][int(frm_piece['n'])] = to

                        insults.moveInsult(frm_piece['type'], move[0], move[1])
                        display.changeTurn()

                        print("### BLACK TURN FINISH ###")

                    else:
                        insults.illegalPlayInsult()
                        display.forceChangeTurn("white")
                    return False

                if len(missing) == 1:
                    grid_from = missing[0]
                    grid_to = getPieceInNewSlot(yellow_contours)

                    print("Missing: " + str(missing))
                    print("To: " + str(grid_to))

                    mightBeTaken = False

                    if len(grid_to) == 1:
                        grid_to = grid_to[0]

                        if grid_to == 36:
                            print("grid_to is acting weird again.")
                            grid_to = [grid_to]
                            mightBeTaken = True
                    elif len(grid_to) > 1:
                        #For some reason 36 keeps getting picked up?? idk why
                        for gt in grid_to:
                            if gt != 36:
                                grid_to = gt

                    missing_piece = getPieceByCoord(grid_from)

                    try:
                        if grid_to == None or len(grid_to) == 0 or mightBeTaken:
                            print("Took a piece.")

                            coord = chess.gridNToChessCoord(piece_tracker[missing_piece['side']][missing_piece['type']][int(missing_piece['n'])])

                            if grid_to == None or len(grid_to) == 0:
                                grid_to = []
                            else:
                                grid_to[0] = chess.gridNToChessCoord(grid_to[0])

                            for move in list(chess.board.legal_moves):
                                splt = chess.uciSplitStr(move)
                                if splt[0] == coord:
                                    grid_to.append(splt[1])

                            display.choices = grid_to

                            insults.choosePieceInsult()

                            return False
                    except:
                        print("not a take")
                    
                    if chess.isPossibleMove(grid_from, grid_to):
                        piece_tracker[missing_piece['side']][missing_piece['type']][int(missing_piece['n'])] = grid_to

                        print("Moved " + missing_piece['side'] + " on the " + missing_piece['type'] + " side to " + str(grid_to) + " from " + str(grid_from))

                        chess.makeMove(grid_from, grid_to)

                        print("Made move on board.")
                        
                        engine_mv = chess.makeEngineMove()
                        
                        if chess.getBoard().is_castling(engine_mv.move):
                            print("Engine castled")
                            kingside_rook = getPieceByCoord(7)
                            queenside_rook = getPieceByCoord(63)
                            if chess.getBoard().is_kingside_castling(engine_mv.move):
                                piece_tracker['black']['rooks'][kingside_rook['n']] = 23
                                piece_tracker['black']['king'][0] = 15
                            else:
                                piece_tracker['black']['rooks'][queenside_rook['n']] = 39
                                piece_tracker['black']['king'][0] = 47
                        else:
                            move = chess.uciToSplit(engine_mv)

                            print("Generated move from engine: " + str(move))
                            
                            frm = chess.chessCoordToGridN(move[0])
                            to = chess.chessCoordToGridN(move[1])

                            print("From " + str(frm) + " to " + str(to) + " (Grid Numbers)")

                            frm_piece = getPieceByCoord(frm)

                            print(str(frm_piece), str(frm), str(to))

                            #Check if there is a piece already at that spot, if so, 'remove' it.
                            if getPieceByCoord(to)['n'] > -1:
                                piece = getPieceByCoord(to)
                                piece_tracker[piece['side']][piece['type']][int(piece['n'])] = -15331462
                            
                            #Update the piece tracker to black's move
                            piece_tracker[frm_piece['side']][frm_piece['type']][int(frm_piece['n'])] = to

                        insults.moveInsult(frm_piece['type'], move[0], move[1])
                        display.changeTurn()

                        print("### FINISHED BLACK'S TURN ###")
                    
                    else:
                        insults.illegalPlayInsult()
                        display.forceChangeTurn('white')
        if display.justChose():
            choice = display.getChoice()

            missing = getMissingPieces(yellow_contours)
            grid_to = chess.chessCoordToGridN(choice)

            if len(missing) > 1:
                #Insult -> illegal moves.
                print("More than 1 piece moved, illegal.")
                insults.illegalPlayInsult()
                display.forceChangeTurn("white")

            if len(missing) == 1:
                grid_from = missing[0]

                print("Missing: " + str(missing))
                print("To: " + str(grid_to))

                missing_piece = getPieceByCoord(grid_from)
                
                if chess.isPossibleMove(grid_from, grid_to):
                    piece_at_place = getPieceByCoord(grid_to)

                    piece_tracker[piece_at_place['side']][piece_at_place['type']][int(piece_at_place['n'])] = -595013859 #idk random number
                    
                    piece_tracker[missing_piece['side']][missing_piece['type']][int(missing_piece['n'])] = grid_to

                    print("Moved " + missing_piece['side'] + " on the " + missing_piece['type'] + " side to " + str(grid_to) + " from " + str(grid_from))

                    chess.makeMove(grid_from, grid_to)

                    print("Made move on board.")

                    print("### CALC BLACK'S MOVE ###")
                    
                    engine_mv = chess.makeEngineMove()
                    
                    #Check if the board is castling
                    if chess.getBoard().is_castling(engine_mv.move):
                            print("Engine castled")

                            kingside_rook = getPieceByCoord(7)
                            queenside_rook = getPieceByCoord(63)
                            if chess.getBoard().is_kingside_castling(engine_mv.move):
                                piece_tracker['black']['rooks'][kingside_rook['n']] = 23
                                piece_tracker['black']['king'][0] = 15
                            else:
                                piece_tracker['black']['rooks'][queenside_rook['n']] = 39
                                piece_tracker['black']['king'][0] = 47
                    else: #if not, just do the turn.
                        move = chess.uciToSplit(engine_mv)

                        print("Generated move from engine: " + str(move))
                        
                        frm = chess.chessCoordToGridN(move[0])
                        to = chess.chessCoordToGridN(move[1])

                        print("From " + str(frm) + " to " + str(to) + " (Grid Numbers)")

                        frm_piece = getPieceByCoord(frm)

                        if getPieceByCoord(to)['n'] > -1:
                                piece = getPieceByCoord(to)
                                piece_tracker[piece['side']][piece['type']][int(piece['n'])] = -15331462

                        #print(str(frm_piece), str(frm), str(to))

                        piece_tracker[frm_piece['side']][frm_piece['type']][int(frm_piece['n'])] = to

                    insults.moveInsult(frm_piece['type'], move[0], move[1])
                    display.changeTurn()

                    print("### FINISH BLACK'S MOVE ###")
                else:
                    insults.illegalPlayInsult()
                    display.forceChangeTurn('white')


    #if q is pressed, stop the program.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return True
    
    display.setBoard(piece_tracker)

    return False

def subMain():
    #pretty much the most important line of code in this program
    time.sleep(1)

    res = True
    while res:
        res = not main()
    finish()

#Release the camera and close the windows.
def finish():
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    #Setup board
    chess.resetBoard()

    print("Reset the board.")

    #Do threading stuff
    thread = threading.Thread(target=display.launchApp)
    thread.start()
    subMain()

    print("Started tasks. Launching the app soon.")
import logging
from logging import error
from flask import Flask, request, jsonify
from flask.globals import request
from flask.helpers import send_from_directory
from flask.templating import render_template
import json

app = Flask(__name__, static_url_path='/static')

app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True

success = '{"success": true}'

started = playing = waitingForChoice = justChosenChoice = False
turn = lastTurnCheck = "white"

choice = None

choices = []

boardCopy = None

@app.route("/")
def index():
    return render_template('display.html', error=error)

@app.route("/api/started")
def start():
    global started, playing
    started = True
    playing = True
    print("Got started.")
    return success

@app.route("/api/board")
def board():
    return json.dumps(boardCopy)

@app.route("/api/turn")
def gtTurn():
    t = {
        'turn': turn
    }
    return json.dumps(t)

@app.route('/api/finishturn')
def changeTurn():
    global turn, lastTurnCheck
    if turn == "white":
        turn = 'black'
        lastTurnCheck = 'white'
    else: 
        turn = 'white'
        lastTurnCheck = 'black'

    print("Switched turn to " + turn)

    return json.dumps({
        'success': True,
        'turn': turn
    })

@app.route('/api/choose', methods=['POST', 'GET'])
def choose():
    global choice, waitingForChoice, justChosenChoice, choices
    #In post body, it'll contain a choice field -> the index of the choice chosen.
    if request.method == 'POST':
        choice_number = int(request.json['choice'])

        if choice_number == -1:
            choice = str(request.json['move']) #Idk, there's some weird glitches and stuff, made this to try to fix things.
        else:
            choice = choices[choice_number] 

        waitingForChoice = False
        justChosenChoice = True
        choices = []
    else:
        return jsonify(choices)

def forceChangeTurn(to):
    global turn, lastTurnCheck
    turn = lastTurnCheck = to

def getApp():
    return app

def setBoard(board):
    global boardCopy
    boardCopy = board

def justStarted():
    global started
    st = not not started
    started = False
    return st

def justChangedTurns():
    global turn, lastTurnCheck
    if turn == lastTurnCheck:
        return False
    else:
        lastTurnCheck = turn
        return True

def justChose():
    global justChosenChoice
    if justChosenChoice:
        justChosenChoice = False
        return True
    return False

def getChoice():
    global choice
    choiceCopy = choice
    choice = None
    return choiceCopy

def waitForUser():
    return waitingForChoice

def isPlaying():
    return playing

def getTurn():
    return turn

def launchApp():
    app.run()

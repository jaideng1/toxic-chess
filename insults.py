from gtts import gTTS
import os
import csv
import glob
import json
import time
from random import randint

language = "en"

id = 0

doInsults = False

shakespear = [
    [],
    [],
    []
]

#Notes: Why is 'Sam Rea' an insult???? like what
#Also:
#Shandy - that's a drink?
#arfarfan'arf - wwhaat??
names = [

]

starters = [
    "wow you",
    "",
    "i can't believe you,",
    "you are a dumbo,",
]

#Loading
def loadShakespearInsults():
    with open('insults/shakespear.csv') as shakespeareanInsults:
        rdr = csv.reader(shakespeareanInsults, delimiter=',')
        line_count = 0
        for row in rdr:
            if line_count == 0:
                line_count += 1
                continue

            for i in range(3):
                shakespear[i].append(row[i])

            line_count += 1

def loadNameInsults():
    #Btw you'll need to create your own file for this, that file is so vile
    f = open('insults/insults.json')

    data = json.load(f)

    for insult in data:
        names.append(insult)
    
    f.close()

#Recordings stuff
def clearRecordings():
    files = glob.glob("./recordings/*")
    print(files)
    for f in files:
        os.remove(f)
    print("Cleared recordings.")

def createNewRecording(text, slow=False):
    global id
    obj = gTTS(text=text, lang=language, slow=slow)
    name = "recordings/rc_" + str(id) + ".mp3"
    obj.save(name)
    id += 1
    return name

def play(name):
    os.system("afplay " + name)

#Insult generators
def generateShakespeareanInsult():
    if not doInsults: return ""

    wrds = []
    for i in range(3):
        wrds.append(shakespear[i][randint(0, len(shakespear[i]) - 1)])

    return wrds[0] + " " + wrds[1] + " " + wrds[2]

def randNameInsult():
    return names[randint(0, len(names) - 1)]


def getStarter():
    return starters[randint(0, len(starters) - 1)]

#Saying insults
def missedEnPassantInsult():
    insult = "can't believe you missed that enpassant!!"
    play(createNewRecording(insult))

def illegalPlayInsult():
    print("instult of somethign")
    insult = "that was illegal"
    play(createNewRecording(insult))

def choosePieceInsult():
    ps_l = [
        generateShakespeareanInsult(),
        randNameInsult() + randNameInsult()
    ]
    insult = "choose the piece you took you " + ps_l[randint(0, 1)]
    play(createNewRecording(insult))

def moveInsult(piece, from_, to):
    inserts = [
        "you hear me, you " + randNameInsult() + randNameInsult(),
        "you got it, you " + generateShakespeareanInsult(),
        ". " + getStarter() + " you " + randNameInsult() + ", guess you're gonna lose soon"
    ]
    insult = "i moved my " + piece + " from " + from_ + " to " + to + ", " + inserts[randint(0, len(inserts) - 1)]
    if doInsults:
        play(createNewRecording(insult, True))
    else:
        play(createNewRecording('i moved my ' + piece + " from " + from_ + " to " + to))

def init():
    #Clear the recordings
    clearRecordings()
    #Load different insults
    loadNameInsults()
    loadShakespearInsults()

#Run the init if this is the main file or this is imported.
init()

if __name__ == "__main__":
    #missedEnPassantInsult()
    play(createNewRecording(getStarter() + " you " + randNameInsult() + randNameInsult()))
    # #moveInsult("pawn", "e7", "e5")
    print("done")


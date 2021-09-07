from gtts import gTTS
import os
import csv
import glob
import json
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

#Saying insults
def missedEnPassantInsult():
    insult = "Are you kidding ??? What the fuck are you talking about man ? You are a biggest looser i ever seen in my life ! You was doing PIPI in your pampers when i was beating players much more stronger then you! You are not proffesional, because proffesionals knew how to lose and congratulate opponents, you are like a girl crying after i beat you! Be brave, be honest to yourself and stop this trush talkings!!! Everybody know that i am very good blitz player, i can win anyone in the world in single game! And wesley so is nobody for me, just a player who are crying every single time when loosing, ( remember what you say about Firouzja ) !!! Stop playing with my name, i deserve to have a good name during whole my chess carrier, I am Officially inviting you to OTB blitz match with the Prize fund! Both of us will invest 5000$ and winner takes it all! I suggest all other people who's intrested in this situation, just take a look at my results in 2016 and 2017 Blitz World championships, and that should be enough... No need to listen for every crying babe, Tigran Petrosyan is always play Fair ! And if someone will continue Officially talk about me like that, we will meet in Court! God bless with true! True will never die ! Liers will kicked off..."
    play(createNewRecording(insult))

def illegalPlayInsult():
    print("instult of somethign")
    insult = "poopyhead that was illegal"
    play(createNewRecording(insult))

def choosePieceInsult():
    insult = "choose the piece you took you " + generateShakespeareanInsult()
    play(createNewRecording(insult))

def moveInsult(piece, from_, to):
    inserts = [
        "you hear me, you " + names[randint(0, len(names) - 1)],
        "you got it, you " + generateShakespeareanInsult(),
        ". guess you're gonna lose soon"
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
    #play(createNewRecording(" you, you " + generateShakespeareanInsult()))
    moveInsult("pawn", "e7", "e5")
    print("done")
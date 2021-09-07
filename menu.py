#### NOT USED ANYMORE, WAS PHASED OUT FOR `./display.py` ####


import tkinter as tk
from tkinter.constants import N

started = False
selected = None
readyToChangeMove = False

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        self.choiceButtons = []

    def create_widgets(self):
        self.readyButton = tk.Button(self, fg='green')
        self.readyButton["text"] = "Ready to start?"
        self.readyButton["command"] = self.start_prg
        self.readyButton.pack(side="top")

        self.turnText = tk.Text(self, width=20, height=2)
        self.turnText.insert(tk.END, "Not playing yet.")
        self.turnText.pack()

        self.quit = tk.Button(self, text="Quit the program.", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def removeChoiceButtons(self):
        for button in self.choiceButtons:
            button.pack_forget()

        self.choiceButtons = []

    def createChoiceButtons(self, pieces):
        self.removeChoiceButtons()

        #Pieces will have the piece type, and the chess board location.
        i = 0
        for piece in pieces:
            b = tk.Button(self)
            b["text"] = piece["type"] + " at " + piece["location"]
            b["command"] = (lambda: self.selectMove(n=i))
            b.pack()
            self.choiceButtons.append(b)

            i += 1
    
    def setTurnText(self, text):
        self.turnText.pack_forget()
        self.turnText = tk.Text(self, height=2, width=20)
        self.turnText.insert(tk.END, text)
        self.turnText.pack()

    def selectMove(self, n):
        global selected

        self.removeChoiceButtons()

        selected = n
    
    def onFinishedWithTurn(self):
        global readyToChangeMove
        readyToChangeMove = True

    def start_prg(self):
        global started
        print("Set started to True, will start program soon.")
        started = True

        self.readyButton.pack_forget()

        self.readyButton = tk.Button(self, 
            text="Press this when you're finished with your turn.",
            command=self.onFinishedWithTurn,
            height = 5, width = 30,
            fg='green'
        )

        self.readyButton.pack(side="top")

        self.setTurnText("Current Turn: Black (Computer)")


root = tk.Tk()
root.geometry("600x400")
app = Application(master=root)

def haveStarted():
    return started

def setChoices(choices):
    app.createChoiceButtons(choices=choices)

def getSelectedChoice():
    global selected
    toReturn = selected + 1
    selected = None
    return toReturn - 1

def readyToChangeMove():
    global readyToChangeMove
    copy = not not readyToChangeMove
    readyToChangeMove = False
    return copy

def update():
    app.update_idletasks()
    app.update()
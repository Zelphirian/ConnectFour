# -*- coding: utf-8 -*-
"""
File: ConnectFour.py
Casaundra Holley
Description: Runs a GUI that allows the user to play connect four with another person.
Python 3.13
Requires: Numpy, Pillow

"""

import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

RADIUS = 39

def main():
    app = None;
    if app == None:
        app = App()
        app.resizable(False, False)
        app.mainloop()
    
    
''' Player object for storing wins/loses/draws
'''
class Player():
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.loses = 0
        self.draws = 0
    def rename(self, name):
        self.name = name
    
''' Model class for storing all necessary arrays and values.
'''     
class Model():
    def __init__(self):
        self.players = []
        self.playerNames = []
        self.addPlayer("Player One")
        self.addPlayer("Player Two")
        
        self.xcord = [230, 355, 478, 604, 725, 855, 985]
        self.ycord = [753, 628, 509, 386, 264, 142]
        
        self.turn = 0
        self.gameOver = False
        self.board = np.zeros((6,7))
    '''Function for adding Player objects to players array
    '''    
    def addPlayer(self, name):
        if(self.findPlayer(name)) == 0:
            newPlayer = Player(name)
            self.players.append(newPlayer)
            self.playerNames.append(name)
    '''Finds a Player object inside the players array from given name
    '''     
    def findPlayer(self, name):
        for person in self.players:
            if person.name == name:
                return person
        return 0
    
'''Controller for all active actions and game implementation
'''    
class Controller():
    def __init__(self, model, view):
        self.view = view
        self.model = model
        
    '''Calls functions for each turn for Board event. Runs playerTurn() and checks for wins or draw
        via win() and catsGame(). Sets game over notification and incraments Player statss.
    '''    
    def runGame(self, event):
        if(self.model.gameOver == False):
            #Runs player turn event
            self.playerTurn(event)
        #check for win and draw
            if (self.catsGame() == True):
                #display draw text
                self.model.gameOver = True
                self.view.playerTurnL.configure(text = "Game Over")
                self.view.display.itemconfig(['banner'], state = tk.NORMAL)
                self.view.wLabel.config(text = "Draw", background = "#9B98D2")
            winChk = self.win()
            if (winChk != 0):
                self.model.gameOver = True
                if(winChk == 1):
                    winner = self.view.varOne.get()
                    loser = self.view.varTwo.get()
                    self.view.display.itemconfig(['banner'], state = tk.NORMAL)
                    self.view.wLabel.config(text = winner+" Wins", background = "#fdb2a5")
                else:
                    winner = self.view.varTwo.get()
                    loser = self.view.varOne.get()
                    self.view.display.itemconfig(['banner'], state = tk.NORMAL)
                    self.view.wLabel.config(text = winner+" Wins", background = "#9de6cc")
                #display player won text
                objWin= self.model.findPlayer(winner)
                objWin.wins+=1
                objLos= self.model.findPlayer(loser)
                objLos.loses+=1
                self.updateInfo(self.view.varOne.get())
                self.updateInfoTwo(self.view.varTwo.get())
                self.view.playerTurnL.configure(text = "Game Over")
        else:
             self.newGame()
             
    '''Runs player's turn dropping piece and ending turn if applicable
    '''           
    def playerTurn(self, event):
        x,y = self.view.master.winfo_pointerxy()
        track = self.view.master.winfo_containing(x, y)
        canvas = self.view.display
        turnTaken = 0
        x = self.view.display.canvasx(event.x)
        
        if(track == canvas):
            #If valid piece location drops piece depending on player one/player two
            col = self.convert(x)
            if (self.model.turn == 0):
                turnTaken = self.dropDot(col, 1)
            elif (self.model.turn == 1):
                turnTaken = self.dropDot(col, 2)
        #Incraments to next turn, sets player's turn text, and changes color of floater.
        if (turnTaken == True):
            self.model.turn += 1
            self.model.turn = self.model.turn%2
            if(self.model.turn == 0):
                playerN = self.view.varOne.get()
                self.view.display.itemconfig(["floater"], fill = "#fdb2a5", outline = "#fdb2a5")
            else:
                playerN = self.view.varTwo.get()
                self.view.display.itemconfig(["floater"], fill = "#9de6cc", outline = "#9de6cc")
            self.view.playerTurnL.configure(text = playerN+"'s Turn")
        #print(self.model.board)  ##test print
            
    '''Resets game board; clearing markers, turn, and rehides win notifictation.
    '''            
    def newGame(self):
        self.model.board.fill(0)
        self.model.turn = 0
        self.model.gameOver = False
        self.view.clearMarkers()
        playerN = self.view.varOne.get()
        self.view.display.itemconfig(["floater"], fill = "#fdb2a5", outline = "#fdb2a5")
        self.view.display.itemconfig(['banner'], state = tk.HIDDEN)
        self.view.playerTurnL.configure(text = playerN+"'s Turn")
        
    '''Returns the column number from player click event. Tracks the mouse and applies each section
        of board to a specific column for player to place their marker.
    '''    
    def convert(self, x):
        if (x >= 180 and x <= 280):
            col = 0
        elif (x >= 300 and x <= 400):
            col = 1
        elif (x >= 430 and x <= 530):
            col = 2
        elif (x >= 550 and x <= 650):
            col = 3
        elif (x >= 680 and x <= 780):
            col = 4
        elif (x >= 810 and x <= 910):
            col = 5
        elif (x >= 940 and x <= 1040):
            col = 6
        else:
            col = -1
        return col

    '''Updates Player one info box in View
    '''        
    def updateInfo(self,name):
        playerObj = self.model.findPlayer(name)
        self.view.winLbl.configure(text = "Wins: "+ str(playerObj.wins))
        self.view.losLbl.configure(text = "Loses: "+ str(playerObj.loses))
        self.view.draLbl.configure(text = "Draws: "+ str(playerObj.draws))
    '''Updates Player two info box
    '''    
    def updateInfoTwo(self, name):
        playerObj = self.model.findPlayer(name)
        self.view.winLblT.configure(text = "Wins: "+ str(playerObj.wins))
        self.view.losLblT.configure(text = "Loses: "+ str(playerObj.loses))
        self.view.draLblT.configure(text = "Draws: "+ str(playerObj.draws))
    
    
    '''Checks if selected column is valid location and has available spot for marker.
    '''
    def validLocation(self, col):
        if (col == -1):
            return -1
        return self.model.board[5][col]
    '''Returns the current open row for the selected column
    '''
    def getOpenRow(self, col):
        for row in range(6):
            if (self.model.board[row][col] == 0):
                return row
    '''Updates board array with the player piece for the given column and row.
    '''        
    def dropDot(self, col, piece):
        if (self.validLocation(col) == 0):
            row = self.getOpenRow(col)
            self.model.board[row][col] = piece
            self.placeMarker(col, row, piece)
            return True
        return False
    
    '''Places grpahic marker on View.board canvas for each player at the specified coordinates.
    '''
    def placeMarker(self, col, row, piece):
        for cord in self.model.xcord:
            cord = self.view.display.canvasx(cord)
        for cord in self.model.ycord:
            cord = self.view.display.canvasy(cord)
        xcord = self.model.xcord
        ycord = self.model.ycord
        if (piece == 1):
            self.view.display.create_oval(xcord[col]-RADIUS, ycord[row]-RADIUS, xcord[col]+RADIUS, ycord[row]+RADIUS, 
                                                 tag=["marker"], outline = '#fdb2a5', fill = '#fdb2a5') ############################
        elif (piece == 2):
            self.view.display.create_oval(xcord[col]-RADIUS, ycord[row]-RADIUS, xcord[col]+RADIUS, ycord[row]+RADIUS, 
                                                 tag=["marker"], outline = '#9de6cc', fill = '#9de6cc') ############################
    '''Checks if the entire board is filled. Returns True if so, False otherwise.
    '''    
    def allFull(self):
        for col in range(7):
            if (self.model.board[5][col] == 0):
                return False
        return True
            
    '''Runs winChk() for each player to determine a win 
    '''
    def win(self):
        if (self.winChk(1) == True):
            return 1
        elif (self.winChk(2)== True):
            return 2
        else:
            return False
    '''Takes player piece and checks board array for subsequent 'pieces' for four in a row
    '''
    def winChk(self, piece):
        board = self.model.board
        for c in range(7-3):
            for r in range(6):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True
        for c in range(7):
            for r in range(6-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True
 
        # Check positively sloped diaganols
        for c in range(7-3):
            for r in range(6-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True
 
        # Check negatively sloped diaganols
        for c in range(7-3):
            for r in range(3, 6):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True
 
    '''Checks if game board is full and if so sets a draw and updates player info. 
        Else returns false.
    '''
    def catsGame(self):
        if(self.allFull() == True):
            name = self.view.varOne.get()
            nameT = self.view.varTwo.get()
            playerOne = self.model.findPlayer(name)
            playerOne.draws+=1
            playerTwo = self.model.findPlayer(nameT)
            playerTwo.draws+=1
            self.updateInfo(name)
            self.updateInfoTwo(nameT)
            return True
        else:
            return False
        
        
'''Genertates all frames and widgets for GUI
'''    
class View(tk.Frame):
    def __init__(self, master, model):
        super().__init__(master)
        self.master = master
        self.model = model
        
        self.configure(background = "#E9FBFF")
        
        self.master.bind("<Motion>", self.motion)
        #Activate header
        self.header()
        #Set PLayer frames
        midFrame = tk.Frame(self, background = "#E9FBFF")
        midFrame.pack(side = tk.TOP, fill = tk.X)
        spacer = tk.Label(midFrame, width = 10, background = "#E9FBFF")
        spacer2 = tk.Label(midFrame, width = 10, background = "#E9FBFF")
    
        spacer.pack(side = tk.LEFT)
        #Set up Option menu for player one
        self.varOne = tk.StringVar()
        self.varOne.set("Player One")
        self.oneFrame = tk.Frame(midFrame)
        self.oneFrame.pack(side = tk.LEFT, fill = tk.X)
        self.plOneMenu = tk.OptionMenu(self.oneFrame, self.varOne, *self.model.playerNames)
        self.plOneMenu.pack(side = tk.LEFT)
        self.plOneMenu.config(width = 10, borderwidth = 2, relief = "groove", font = ("Berlin Sans FB",13)) 
        self.oneInfo(self.varOne.get())
        
        #End game text
        playerOne = self.varOne.get()
        self.playerTurnL = tk.Label(midFrame, text = playerOne+"'s Turn", font = ("Berlin Sans FB",18), background = "#E9FBFF") 
        self.playerTurnL.pack(side = tk.LEFT,anchor = tk.N, fill = tk.X, expand = 1)
        
        spacer2.pack(side = tk.RIGHT)
        #Set up Option menu for player two
        self.varTwo = tk.StringVar()
        self.varTwo.set("Player Two")
        self.twoFrame = tk.Frame(midFrame)
        self.twoFrame.pack(side = tk.RIGHT, fill = tk.X)
        self.plTwoMenu = tk.OptionMenu(self.twoFrame, self.varTwo, *self.model.playerNames)
        self.plTwoMenu.pack(side = tk.RIGHT)
        self.plTwoMenu.config(width = 10, borderwidth = 2, relief = "groove", font = ("Berlin Sans FB",13)) 
        self.twoInfo(self.varTwo.get())
        
        #Set board graphic
        self.boardGraphic()
        #Sets player info colors
        self.theme("#fdb2a5", "#9de6cc") ##B6D7A8"
        
    '''Configures all player info boxes to given hex color, hexOne for player one
        and hexTwo for player two
    '''
    def theme(self, hexOne, hexTwo):
        self.oneFrame.config(background = hexOne)
        self.plOneMenu.config(background = hexOne)
        self.winLbl.config(background = hexOne)
        self.losLbl.config(background = hexOne)
        self.draLbl.config(background = hexOne)
        
        self.twoFrame.config(background = hexTwo)
        self.plTwoMenu.config(background = hexTwo)
        self.winLblT.config(background = hexTwo)
        self.losLblT.config(background = hexTwo)
        self.draLblT.config(background = hexTwo)
        
    '''Generates the header box consisting of window title, new player button, and new game button
    '''   
    def header(self):
        topFrame = tk.Frame(self, background = "#E9FBFF")
        topFrame.pack(side=tk.TOP, fill=tk.X, pady = 10)
        addButton = tk.Button(topFrame, text = "Add Player", font= ("Berlin Sans FB", 13), command = self.newPlayer, background = "#fff2cc",
                              borderwidth = 2, relief = "groove", height = 1, width = 10)
        addButton.pack(side = tk.LEFT, padx = 80)
        titleLabel = tk.Label(topFrame, text = "   Connect Four", font = ("Berlin Sans FB",32), justify = tk.CENTER, 
                              background = "#E9FBFF", foreground = "#674EA7")
        titleLabel.pack(side = tk.LEFT, expand = 1)
        newButton = tk.Button(topFrame, text = "New Game", font= ("Berlin Sans FB", 13), command = self.newGame, background = "#fff2cc",
                              borderwidth = 2, relief = "groove", height = 1, width = 12)
        newButton.pack(side = tk.RIGHT, padx = 80)
        
    '''Generates player info boxes for player one
    '''
    def oneInfo(self, name):
        obj = self.model.findPlayer(name)
        #Player labels
        self.winLbl = tk.Label(self.oneFrame, text = "Wins: "+ str(obj.wins), font = ("Berlin Sans FB",13))
        self.winLbl.pack(side = tk.LEFT)
        self.losLbl = tk.Label(self.oneFrame, text = "Loses: "+ str(obj.loses), font = ("Berlin Sans FB",13))
        self.losLbl.pack(side= tk.LEFT, padx = 8)
        self.draLbl = tk.Label(self.oneFrame, text = "Draws: "+ str(obj.draws), font = ("Berlin Sans FB",13))
        self.draLbl.pack(side= tk.LEFT, padx = 5)
    '''Generates player info boxes for player two
    '''    
    def twoInfo(self, name):
        obj = self.model.findPlayer(name)
        #Player labels
        self.winLblT = tk.Label(self.twoFrame, text = "Wins: "+ str(obj.wins), font = ("Berlin Sans FB",13))
        self.winLblT.pack(side = tk.LEFT)
        self.losLblT = tk.Label(self.twoFrame, text = "Loses: "+ str(obj.loses), font = ("Berlin Sans FB",13))
        self.losLblT.pack(side= tk.LEFT, padx = 8)
        self.draLblT = tk.Label(self.twoFrame, text = "Draws: "+ str(obj.draws), font = ("Berlin Sans FB",13))
        self.draLblT.pack(side= tk.LEFT, padx = 5)
       
    '''Create the board graphic as tk.Canvas and win banner as a canvas.window
    '''
    def boardGraphic(self):
        image = Image.open("./img/Board.png")
        maxsize = (1200, 730)
        image.thumbnail(maxsize)
        self.graphic = ImageTk.PhotoImage(image)
        self.display = tk.Canvas(self, bd = 0, highlightthickness = 0, background = "#E9FBFF")
        self.display.create_image(600, 82, image = self.graphic, tags = ["graphic"], anchor = tk.N)
        self.display.create_oval(170-RADIUS, 2, 170+RADIUS, RADIUS*2+2, tag = ['floater'],
                                              outline = '#fdb2a5', fill = '#fdb2a5')
        #self.display.create_polygon(170,10,170+34,68,170+68,10, tag = ['floater'], fill = "#fdb2a5", outline= "#fdb2a5")
        self.display.image = self.graphic
        self.display.pack(fill = tk.BOTH, expand = 1)
        
        #Win banner and button
        frame = tk.Frame(self.display, background = "#9B98D2")
        self.wLabel = tk.Label(frame, height = 3, width = 100, font = ("Berlin Sans FB",17))
        self.wLabel.pack()
        button = tk.Button(frame, text = "New Game", font = ("Berlin Sans FB",13), command = self.newGame, background = "#fff2cc",
                              borderwidth = 2, relief = "groove", height = 1, width = 12)
        button.pack(side = tk.BOTTOM)
        self.display.create_window(0, 250, window = frame, anchor = tk.NW, tags = ['banner'], state = tk.HIDDEN)
        
        #self.bind("<Configure>", self.resize)
        self.display.bind("<Motion>", self.motion)
        self.display.bind("<Button-1>", self.runGame)
            
    '''Makes the new player window for adding additional players
    '''    
    def newPlayer(self):
        self.newWind = tk.Toplevel(self)
        self.newWind.title("New Player")
        self.newWind.geometry('%dx%d+%d+%d' % (230,140,300,200))
        self.newWind.resizable(0,0)
        self.newWind.configure(background = "#E9FBFF")
        #Name entry
        label = tk.Label(self.newWind, text="Name:", anchor=tk.E, background = "#E9FBFF", font = ("Berlin Sans FB",13))
        label.pack(pady = 10)
        self.nameIn = tk.Entry(self.newWind)
        self.nameIn.pack()
        
        frame = tk.Frame(self.newWind, background = "#E9FBFF")
        frame.pack(pady = 15)
        conButton = tk.Button(frame, text="Confirm", command = self.addPlayer, background = "#d9ead3",
                              borderwidth = 2, relief = "groove", font = ("Berlin Sans FB",13))
        conButton.pack(side = tk.LEFT, padx = 10)
        cancButton = tk.Button(frame, text = "Cancel", command = self.cancel, background = "#f4cccc",
                              borderwidth = 2, relief = "groove", font = ("Berlin Sans FB",13))
        cancButton.pack(side = tk.RIGHT, padx = 10)
    
    '''Tracks the motion of the mouse
    '''            
    def motion(self,event):
        x,y = self.master.winfo_pointerxy() # counts the entire screen
        track = self.master.winfo_containing(x, y)
        canvas = self.display
        x = self.display.canvasx(event.x)
        #print(event.x, event.y, x, self.display.canvasy(event.y)) #test prints
        if((track == canvas or track == self.wLabel) and x >= 170 and x <= 1050):
            self.display.coords("floater",x-RADIUS, 2, x+RADIUS, RADIUS*2+2)
        self.controller.updateInfo(self.varOne.get())
        self.controller.updateInfoTwo(self.varTwo.get())
        
    ''' Relocates the "graphic" image to center when window is resized.
    '''
    def resize(self, event):
        self.master.update()
        width = self.master.winfo_width()
        self.display.delete("graphic")
        self.display.create_image(width/2, 80, image = self.graphic, tags = ["graphic"], anchor = tk.N)
        self.display.update()
        
    
    '''Clears all player makers from the board display
    '''    
    def clearMarkers(self):
       self.display.delete("marker")
       self.display.update() ##need?
    '''Destroys the new player window when cancel button is clicked
    '''
    def cancel(self):
        self.newWind.destroy()
    '''Performs addplayer() function and updates option menu for player one and two, when
        confirm button is clicked.
    '''
    def addPlayer(self):
        name = self.nameIn.get()
        self.model.addPlayer(name)
        self.updateOptions(self.plOneMenu, self.varOne)
        self.updateOptions(self.plTwoMenu, self.varTwo)
        self.newWind.destroy()

    '''Updates the options menu with new variable
    '''    
    def updateOptions(self, menu, var):
        menu = menu["menu"]
        menu.delete(0, "end")
        for string in self.model.playerNames:
            menu.add_command(label=string, 
                             command=lambda value=string: var.set(value))
    '''runGame() function from controller
    '''        
    def runGame(self, event):
        self.controller.runGame(event)
    '''newGame() function from controller
    '''    
    def newGame(self):
        self.controller.newGame()
    
    '''Sets controller'''
    def setController(self, controller):
        self.controller = controller
'''Sets model, view, and controller.
'''
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Connect Four")
        self.geometry("1200x960")
        
        model = Model()                   
       
        view = View(self, model)
        view.pack(fill= tk.BOTH, expand = 1)

        controller = Controller(model, view)
        view.setController(controller)
        
main()
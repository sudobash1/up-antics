##
#Game
#Description: Keeps track of game logic and manages the play loop.
##
import os, re, sys, HumanPlayer
from UserInterface import *
from Construction import *
from GameState import *
from Inventory import *
from Building import *
from Location import *
from Ant import *

#Game Modes
TOURNAMENT_MODE = 0
HUMAN_MODE = 1
AI_MODE = 2

class Game(object):
    def __init__(self):
        self.players = []
        #BOARDS ARE SQUARE
        board = [[Location((col, row)) for row in xrange(0,BOARD_LENGTH)] for col in xrange(0,BOARD_LENGTH)]
        p1Inventory = Inventory(PLAYER_ONE, [], [], 0)
        p2Inventory = Inventory(PLAYER_TWO, [], [], 0)
        self.state = GameState(board, [p1Inventory, p2Inventory], MENU_PHASE, PLAYER_ONE)
        self.scores = [0,0]
        self.mode = None
        self.ui = UserInterface((960,750))
        self.ui.initAssets()
        #UI Callback functions
        self.ui.buttons['start'][3] = self.startGame
        self.ui.buttons['tournament'][3] = self.tournamentPath
        self.ui.buttons['human'][3] = self.humanPath
        self.ui.buttons['ai'][3] = self.aiPath
        self.ui.locationClicked = self.locationClickedCallback
          
    def runGame(self):
        # initialize board be ready for player input for game parameter
        while True:
            self.ui.drawBoard(self.state)
            #Determine current chosen game mode. Enter different execution paths based on the mode, which must be chosen by clicking a button.
            
            #player has clicked start game so enter game loop
            if self.state.phase != MENU_PHASE:
                print "Game Started!"
                #init game stuffs
                #build a list of things to place
                #things to place: 2 anthill/queen, 9 obstacles, 2 food sources (for opponent)
                constrsToPlace = []
                constrsToPlace += [Building(None, ANTHILL, i) for i in xrange(0,2)]
                constrsToPlace += [Construction(None, GRASS) for i in xrange(0,18)]
                constrsToPlace += [Construction(None, FOOD) for i in xrange(0,4)]
                
                while not self.isGameOver(PLAYER_ONE) and not self.isGameOver(PLAYER_TWO):
                    #Draw the board again (to recognize user input in game loop)
                    self.ui.drawBoard(self.state)
                
                    if self.state.phase == SETUP_PHASE:
                        currentPlayer = self.players[self.state.whoseTurn]
                        
                        #if the player is player two, flip the board
                        theState = self.state.clone()
                        if theState.whoseTurn == PLAYER_TWO:
                            theState.flipBoard()
                            
                        #get the placement from the player
                        target = currentPlayer.getPlacement(constrsToPlace[0], theState)
                        validPlace = self.isValidPlacement(constrsToPlace[0], target)
                        if validPlace:
                            #translate coords to match player
                            target = self.state.coordLookup(target, theState.whoseTurn)
                            #get construction to place
                            constr = constrsToPlace.pop(0)
                            #give constr its coords
                            constr.coords = target
                            #put constr on board
                            self.state.board[target[0]][target[1]].constr = constr
                            #change player turn in actual state
                            self.state.whoseTurn = (self.state.whoseTurn + 1) % 2
                        else:
                            if not type(currentPlayer) is HumanPlayer.HumanPlayer:
                                #exit gracefully
                                exit(0)
                            elif validPlace != None:
                                self.ui.notify("Invalid placement: " + str(target[0]) + ", " + str(target[1]))
                        
                        if not constrsToPlace:
                            self.state.phase = PLAY_PHASE
                        
                    elif self.state.phase == PLAY_PHASE:
                        pass
                    else:
                        #something went wrong, exit gracefully
                        pass
                    
                    #check what type first player is
                        #get move(list of locs) from first player until end turn is submitted
                        #If computer player, check validMove 
                        #check if player wants to attack
                        #check isGameOver. If so, break
                    #Don't check what type second player is, because player 1 can't be human
                        #get move(list of locs) from second until end turn is submitted 
                        #If computer player, check ValidMove
                        #check if player wants to attack 
                        #check isGameOver If so, break 
                
    def startGame(self):
        if self.mode != None:
            self.state.phase = SETUP_PHASE
                
    def tournamentPath(self):
        #If already in tournament mode, do nothing. WILL BE CHANGED IN THE FUTURE
        if self.mode == TOURNAMENT_MODE:
            return
        #Attempt to load the AI files
        self.loadAIs()
        #Check right number of players, if successful set the mode.
        if len(self.players) >= 2:
            self.mode = TOURNAMENT_MODE
        self.mode = None # DELETE THIS LINE LATER!!
        
    def humanPath(self):
        #If already in human mode, do nothing.
        if self.mode == HUMAN_MODE:
            return
        #Attempt to load the AI files
        self.loadAIs() 
        #Add the human player to the player list
        self.players.insert(PLAYER_ONE, HumanPlayer.HumanPlayer(len(self.players)))                
        #Check right number of players, if successful set the mode.
        if len(self.players) == 2:
            self.mode = HUMAN_MODE
            self.ui.notify("Mode changed to human")
    
    def aiPath(self):
        #If already in ai mode, do nothing.
        if self.mode == AI_MODE:
            return
        #Attempt to load the AI files
        self.loadAIs()
        #Check right number of players, if successful set the mode.
        if len(self.players) == 2:
            self.mode = AI_MODE
        self.mode = None # DELETE THIS LINE LATER!!
    
    def loadAIs(self):
        #Reset the player list in case some have been loaded already
        self.players = []
        #Attempt to load AIs. Exit gracefully if user trying to load weird stuff.
        filesInAIFolder = os.listdir("AI")
        #Change directory to AI subfolder so modules can be loaded (they won't load as filenames).
        os.chdir('AI')
        #IF WE FOUND A BUG IN PYTHON!!!!
        #Details: changing directory, then importing in python terminal will first check subdirectories for modules.
        #   However, modules will not be foud if this function is used. Does it have to do with it being in a function?
        #Add current directory in python's import search order.
        sys.path.insert(0, os.getcwd())
        #Make player instances from all AIs in folder.
        for file in filesInAIFolder:
            if re.match(".*\.py$", file):
                moduleName = file.rstrip('.py')
                #Check to see if the file is already loaded.
                temp = __import__(moduleName, globals(), locals(), [], -1)
                #If the module has already been imported into this python instance, reload it.
                if temp == None:
                    temp = reload(globals()[moduleName])
                #Create an instance of Player from temp
                self.players.append(temp.AIPlayer(len(self.players)))
        #Remove current directory from python's import search order.
        sys.path.pop(0)
        #Revert working directory to parent.
        os.chdir('..')
    
    def locationClickedCallback(self, coords):
        #Check if its human player's turn
        if self.state.phase != MENU_PHASE and type(self.players[self.state.whoseTurn]) is HumanPlayer.HumanPlayer:
            currentPlayer = self.players[self.state.whoseTurn]
           
            #add location to human player's movelist, context-free since Game will check appropriatocity...??
            if len(currentPlayer.moveList) != 0 and coords == currentPlayer.moveList[-1]:
                currentPlayer.moveList.pop()
            else:
                currentPlayer.moveList.append(coords)
            
    
    # once end game has been reached, display screen "player x wins!" OK/Play Again button
    def isGameOver(self, playerId):
        opponentId = (playerId + 1) % 2
        
        #temp, remove later
        return False
        
        #if ((self.state.phase == PLAY_PHASE) and 
        #((self.state.inventories[playerId].queen.isAlive == False) or
        #(self.state.inventories[opponentId].antHill.captureHealth <= 0) or
        # (self.state.inventories[playerId].foodCount >= 11))):
           # return True
        # else:
          # return False
        
    def isValidMove(self, inputMove, inputPlayer):
        pass
        #if (inputMove.fromLoc.coords[0] < 10) and 
        #    (inputMove.fromLoc.coords[0] >= 0) and 
        #    (inputMove.fromLoc.coords[1] < 10) and 
        #    (inputMove.fromLoc.coords[1] >= 0) and 
        #    (inputMove.toLoc.coords[0] < 10) and 
        #    (inputMove.toLoc.coords[0] >= 0) and 
        #    (inputMove.toLoc.coords[1] < 10) and 
        #    (inputMove.toLoc.coords[1] >= 0) and 
        #    (inputMove.fromLoc.ant.player == inputPlayer) and
        #    (inputMove.toLoc.ant == None) 
    
    def isValidAttack(self):
        pass
        
    def isValidPlacement(self, item, target):
        #If no target, return None (human vs ai caught by caller)
        if target == None:
            return None
                
        #check item type
        if item.type == ANTHILL or item.type == GRASS:
            #check target is on the board
            if target[0] >= 0 and target[0] < BOARD_LENGTH:
                #Nobody can place in the center two rows of the board or on their opponents side
                if target[1] >= 0 and target[1] < BOARD_LENGTH / 2 - 1:
                    #change target to access appropriate players locations
                    target = self.state.coordLookup(target, self.state.whoseTurn)
                    #make sure nothing is there yet
                    if self.state.board[target[0]][target[1]].constr == None:
                        #valid placement
                        return True
                    
        #check item type
        if item.type == FOOD:
            #check target is on the board
            if target[0] >= 0 and target[0] < BOARD_LENGTH:
                #Must place food on your opponents side
                if target[1] < BOARD_LENGTH and target[1] >= BOARD_LENGTH / 2 + 1:
                #change target to access appropriate players locations
                #
                    target = self.state.coordLookup(target, self.state.whoseTurn)
                    #make sure nothing is there yet
                    if self.state.board[target[0]][target[1]].constr == None:
                        #valid placement
                        return True
        #invalid move
        return False
    

a = Game()
a.runGame()

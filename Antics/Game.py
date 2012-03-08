##
#Game
#Description: Keeps track of game logic and manages the play loop.
##
import os
from UserInterface import *
from GameState import *
from Inventory import *
from Location import *
from Ant import *


PLAYER_ONE = 0
PLAYER_TWO = 1

BOARD_LENGTH = 10

#Game Modes
TOURNAMENT_MODE = 0
HUMAN_MODE = 1
AI_MODE = 2

#Game Phases
MENU_PHASE = 0
SETUP_PHASE = 1
PLAY_PHASE = 2

class Game:
    def __init__(self):
        self.players = []
        #BOARDS ARE SQUARE
        board = [[Location(True, 1, (row, col)) for col in xrange(0,BOARD_LENGTH)] for row in xrange(0,BOARD_LENGTH)]
        p1Inventory = Inventory(PLAYER_ONE, None, 0, None)
        p2Inventory = Inventory(PLAYER_TWO, None, 0, None)
        self.state = GameState(board, [p1Inventory, p2Inventory], MENU_PHASE, PLAYER_ONE)
        self.ui = UserInterface((860,700))
        self.ui.initAssets()
        self.ui.buttons['tournament'][3] = self.tournamentPath()
        self.ui.buttons['human'][3] = self.humanPath()
        self.ui.buttons['ai'][3] = self.aiPath()
        self.runGame()
        #self.scores
        #self.mode
        
    def runGame(self):
        # initialize board be ready for player input for game parameter
        while True:
            self.ui.drawBoard(self.state)
            #Determine current chosen game mode. Enter different execution paths based on the mode, which must be chosen by clicking a button.
            #If game mode is tournament
            
            #If game mode is human vs AI
            
            #If game mode is AI vs AI
            
            
            # *player clicks start game* enter game loop
            while not self.isGameOver(PLAYER_ONE) and not self.isGameOver(PLAYER_TWO):
                break
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
                
                
                
    def tournamentPath(self):
        #If already in tournament mode, do nothing.
        if self.mode == TOURNAMENT_MODE:
            return
        #Attempt to load AIs. Exit gracefully if user trying to load .doc files.
        filesInAIFolder = os.listdir("AI")
        for file in filesInAIFolder:
            if re.match(".*\.py", file):
                #First, load the file to make sure it is in globals.
                temp = __import__(os.path.join("AI", file), globals(), locals(), [], -1)
                #Next, reload the file in case it was already in globals, which would mean the above import did nothing.
                globals()[file] = reload(globals()[file])
        #If successful, set the mode.
        
    def humanPath(self):
        #If already in human mode, do nothing.
        if self.mode == HUMAN_MODE:
            return
        #Attempt to load AIs. Exit gracefully if user trying to load .doc files.
        #If successful, set the mode.
    
    def aiPath(self):
        #If already in ai mode, do nothing.
        if self.mode == AI_MODE:
            return
        #Attempt to load AIs. Exit gracefully if user trying to load .doc files.
        #If successful, set the mode.
    
    # once end game has been reached, display screen "player x wins!" OK/Play Again button
    def isGameOver(self, playerId):
        opponentId = (playerId + 1) % 2
        
        #if ((self.state.inventories[playerId].queen.isAlive == False) or
        #(self.state.inventories[opponentId].antHill.captureHealth <= 0) or
        # (self.state.inventories[playerId].foodCount >= 11)):
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


a = Game()
a.runGame()
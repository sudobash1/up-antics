##
#Game
#Description: Keeps track of game logic and manages the play loop.
##
from UserInterface import *
from GameState import *
from Inventory import *
from Location import *
from Ant import *


PLAYER_ONE = 0
PLAYER_TWO = 1

BOARD_LENGTH = 10

#Game Phases
MENU_PHASE = 0
SETUP_PHASE = 1
PLAY_PHASE = 2

class Game:
    def __init__(self):
        #self.players
        #BOARDS ARE SQUARE
        board = [[1 for col in xrange(0,BOARD_LENGTH)] for row in xrange(0,BOARD_LENGTH)]
        p1Inventory = Inventory(PLAYER_ONE, None, 0, None)
        p2Inventory = Inventory(PLAYER_TWO, None, 0, None)
        self.state = GameState(board, [p1Inventory, p2Inventory], MENU_PHASE)
        self.ui = UserInterface((860,700))
        self.ui.initAssets()
        #self.scores
        #self.mode
        
    def runGame(self):
        # initialize board be ready for player input for game parameter
        while True:
            self.ui.drawBoard(self.state)
            #assign first player
            
            # *player clicks start game* enter game loop
            while not isGameOver(PLAYER_ONE) and not isGameOver(PLAYER_TWO):
                pass
                #check what type first player is
                    #get move(list of locs) from first player until end turn is submitted
                    #If computer player, check validMove 
                    #check if player wants to attack
                    #check isGameOver. If so, break
                #check what type second player is 
                    #get move(list of locs) from second until end turn is submitted 
                    #If computer player, check ValidMove
                    #check if player wants to attack 
                    #check isGameOver If so, break 
                
                
                
                
    # once end game has been reached, display screen "player x wins!" OK/Play Again button
    def isGameOver(self, playerId):
        opponentId = (playerId + 1) % 2
        
        if ((self.state.inventories[playerId].queen.isAlive == False) or
        (self.state.inventories[opponentId].antHill.captureHealth <= 0) or
        (self.state.inventories[playerId].foodCount >= 11)):
            return True
        else:
            return False
        
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

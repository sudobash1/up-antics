#Player IDs
PLAYER_ONE = 0
PLAYER_TWO = 1

#Length of the board (it's square)
BOARD_LENGTH = 10

#Game Phases
MENU_PHASE = 0
SETUP_PHASE = 1
PLAY_PHASE = 2

##
#GameState
#Description: The current state of the game.
#
#Variables:
#   board - The game Board being used.
#   inventories - A tuple containing the Inventory for each player.
#   phase - The current phase of the game.
#    whoseTurn - The ID of the Player who's turn it currently is.
##
class GameState(object):

    ##
    #__init__
    #Description: Creates a new GameState
    #
    #Parameters:
    #   inputBoard - The Board to be used by the GameState (Board)
    #   inputInventories - A tuple containing the Inventory for each player ((Inventory, Inventory))
    #   inputPhase - The phase of the game (int)
    #   inputTurn - The ID of the Player who's turn it is (int)
    ##
    def __init__(self, inputBoard, inputInventories, inputPhase, inputTurn):
        self.board = inputBoard
        self.inventories = inputInventories
        self.phase = inputPhase
        self.whoseTurn = inputTurn

    ##
    #applyMove
    #Description: Makes the required changes to the GameState based off of the given move
    #
    #Parameters:
    #   inputMove - The move to make (Move)
    ##
    def applyMove(self, inputMove):
        fromX = fromLoc.getCoords()[0]
        fromY = fromLoc.getCoords()[1]

        toX = toLoc.getCoords()[0]
        toY = toLoc.getCoords()[1]
        
        tempAnt = self.board[fromX][fromY].getAnt()

        tempAnt.coords = ToLoc.getCoords()
        self.board[fromX][fromY].ant = None
        self.board[toX][toY].ant = tempAnt

    ##
    #coordLookup
    #Description: Returns the appropriate coordinates for the given
    #   player to allow both players to play from top of the board.
    #
    #Return: Correct coordinate location for player
    ##
    def coordLookup(self, coords, player):
        if player == PLAYER_ONE:
            return coords
        else:
            return (BOARD_LENGTH - 1 - coords[0], BOARD_LENGTH - 1 - coords[1])
    
    ##
    #flipBoard
    #Description: Flips the board (so Player Two sees self on top side)
    #
    ##
    def flipBoard(self):
        for col in self.board:
            col.reverse()
            
        self.board.reverse()
    
    ##
    #clone
    #Description: Returns a deep copy of itself
    #
    #Return: The GameState identical to the original
    ##
    def clone(self):
        newBoard = [[self.board[row][col].clone() for col in xrange(0,len(self.board))] for row in xrange(0,len(self.board))]
        return GameState(newBoard, [self.inventories[0].clone(), self.inventories[1].clone()], self.phase, self.whoseTurn)
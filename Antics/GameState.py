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
    #    inputTurn - The ID of the Player who's turn it is (int)
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
    #clone
    #Description: Returns a deep copy of itself
    #
    #Return: The GameState identical to the original
    ##
    def clone(self):
        return GameState(self.board.clone(), self.inventories.clone(), self.phase, self.whoseTurn)
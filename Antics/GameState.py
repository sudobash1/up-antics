##
#GameState
#Description: The current state of the game.
#
#Variables:
#   board - The game Board being used.
#   inventories - A tuple containing the Inventory for each player.
#   phase - The current phase of the game.
##
class GameState:
    def __init__(self, inputBoard, inputInventories, inputPhase):
        self.board = inputBoard
        self.inventories = inputInventories
        self.phase = inputPhase

    def applyMove(self, inputMove):
        fromX = fromLoc.getCoords()[0]
        fromY = fromLoc.getCoords()[1]

        toX = toLoc.getCoords()[0]
        toY = toLoc.getCoords()[1]
        
        tempAnt = self.board[fromX][fromY].getAnt()

        tempAnt.coords = ToLoc.getCoords()
        self.board[fromX][fromY].ant = None
        self.board[toX][toY].ant = tempAnt

    def clone(self):
        return GameState(self.board.clone(), self.inventories.clone(), self.phase.clone())
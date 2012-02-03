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
        

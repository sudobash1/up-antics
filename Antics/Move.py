class Move:
    def __init__(self, inputMoveType, inputToLoc, inputFromLoc, inputUnitType):
        self.moveType = inputMoveType
        self.toLoc = inputToLoc
        self.fromLoc = inputFromLoc
        self.unitType = inputUnitType

    def getMoveType(self):
        return self.moveType

    def getToLoc(self):
        return self.toLoc

    def getFromLoc(self):
        return self.fromLoc

    def getUnitType(self):
        return self.unitType

    

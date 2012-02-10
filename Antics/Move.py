##
#Move
#Description: This class represents any valid move that can be made during Antics gameplay
#
#Variables:
#   moveType - This represents the type of move the player has made(moveAnt,build and endTurn)
#   toLoc - This represents the location of where an Ant is moving to
#   fromLoc - This represents the location of where Ant is moving from or being built from(this
#       depends on the moveType)
#   unitType - This identifies the type of a unit(only relevant to Moves of type build)
##
class Move:
    def __init__(self, inputMoveType, inputToLoc, inputFromLoc, inputUnitType):
        self.moveType = inputMoveType
        self.toLoc = inputToLoc
        self.fromLoc = inputFromLoc
        self.unitType = inputUnitType
    

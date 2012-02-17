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

    ##
    #__init__
    #Description: Creates a new Move
    #
    #Parameters:
    #   inputMoveType - The type of move the Player is making (int)
    #   inputToLoc - The Location the Ant is moving to (Location)
    #   inputFromLoc - The Location the Ant is moving from (Location)
    #   inputUnitType - The type of unit being moved (int)
    ##
    def __init__(self, inputMoveType, inputToLoc, inputFromLoc, inputUnitType):
        self.moveType = inputMoveType
        self.toLoc = inputToLoc
        self.fromLoc = inputFromLoc
        self.unitType = inputUnitType
    

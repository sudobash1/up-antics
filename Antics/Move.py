##
#Move
#Description: This class represents any valid move that can be made during Antics gameplay
#
#Variables:
#   moveType - This represents the type of move the player has made(moveAnt,build and endTurn)
#   fromLoc - This represents the location of where Ant is moving from or being built from(this
#       depends on the moveType)
#    locList - The list of Locations representing the path to take
#   unitType - This identifies the type of a unit(only relevant to Moves of type build)
##
class Move(object):

    ##
    #__init__
    #Description: Creates a new Move
    #
    #Parameters:
    #   inputMoveType - The type of move the Player is making (int)
    #   inputFromLoc - The Location the Ant is moving from (Location)
    #    inputLocList - A list of Locations representing the path to take (List<Location>)
    #   inputUnitType - The type of unit being built (int)
    ##
    def __init__(self, inputMoveType, inputFromLoc, inputLocList,inputUnitType):
        self.moveType = inputMoveType
        self.fromLoc = inputFromLoc
        self.locList = inputLocList
        self.unitType = inputUnitType
    

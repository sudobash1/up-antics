##
#Location
#Description: This class represents all valid locations on the board
#
#Variables 
#   isPassable - A boolean to indicate whether an Ant can move through this location
#   movementCost - The cost of moving through this location 
#   ant - The ant found at this location
#   constr - The construction found at this location 
#   coords - The coordinates of this location
##
class Location:

    ##
    #__init__
    #Description: Creates a new Location
    #
    #Parameters:
    #   inputPassable - A boolean describing if the Location can be passed through by an Ant (boolean)
    #   inputMoveCost - The cost of moving through the Location (int)
    #   inputCoordinates - Where on the Board the Location is ((int, int))
    ##
    def __init__(self, inputPassable, inputMoveCost, inputCoordinates):
        self.isPassable = inputPassable
        self.movementCost = inputMoveCost
        self.ant = None
        self.constr = None
        self.coords = inputCoordinates

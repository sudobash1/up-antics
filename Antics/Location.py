##
#Location
#Description: This class represents all valid locations on the board
#
#Variables 
#   ant - The ant found at this location
#   constr - The construction found at this location 
#   coords - The coordinates of this location
##
class Location(object):

    ##
    #__init__
    #Description: Creates a new Location
    #
    #Parameters:
    #   inputCoordinates - Where on the Board the Location is ((int, int))
    ##
    def __init__(self, inputCoordinates):
        self.ant = None
        self.constr = None
        self.coords = inputCoordinates
    
    def getMoveCost(self):
        if self.constr == None:
            return 1
        else:
            return self.constr.movementCost
    
    def clone(self):
        newLoc = Location(self.coords)
        newLoc.ant = self.ant
        newLoc.constr = self.constr
        return newLoc

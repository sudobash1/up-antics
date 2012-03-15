from Constants import *

#Contruction stats array
#(movement cost, capture health)[type]
CONSTR_STATS = []
CONSTR_STATS.append((1,3)) #Anthill
CONSTR_STATS.append((1,2)) #Tunnel
CONSTR_STATS.append((2,None)) #Grass
CONSTR_STATS.append((1,None)) #Food

##
#Construction
#Description: Parent class for static (non-Ant) objects on the board.
#
#Variables:
#   type - int identifying the type of Building, which allows the game to
#       decide what to do with it.
#   movementCost - The cost of moving through this location 
#   coords - An int[] of length 2, representing the Construction's position on
#       the board.  Positions start at (0, 0) in the upper left and increase
#       down and to the right.
##
class Construction(object):

    ##
    #__init__
    #Description: Creates a new Construction. Only ever called by subclasses.
    #
    #Parameters:
    #   inputCoords - The position to put the Construction (int[])
    #   inputType - The type of the Construction
    ##
    def __init__(self, inputCoords, inputType):
        self.coords = inputCoords
        self.type = inputType
        self.movementCost = CONSTR_STATS[inputType][0]
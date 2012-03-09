#Types
ANTHILL = 0
TUNNEL = 1
GRASS = 2
FOOD = 3

##
#Construction
#Description: Parent class for static (non-Ant) objects on the board.
#
#Variables:
#	type - int identifying the type of Building, which allows the game to
#       decide what to do with it.
#   coords - An int[] of length 2, representing the Construction's position on
#       the board.  Positions start at (0, 0) in the upper left and increase
#       down and to the right.
##
class Construction:

    ##
    #__init__
    #Description: Creates a new Construction. Only ever called by subclasses.
    #
    #Parameters:
    #   inputCoords - The position to put the Construction (int[])
	#	inputType - The type of the Construction
    ##
    def __init__(self, inputCoords, inputType):
        self.coords = inputCoords
		self.type = inputType
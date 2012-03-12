##
#Construction
#Description: Parent class for static (non-Ant) objects on the board.
#
#Variables:
#   id - A reference to a Construction that can be manually tracked, so that
#       the programmer can define Construction equality.
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
    #   inputId - The id used to reference the Construction (int)
    #   inputCoords - The position to put the Construction (int[])
    ##
    def __init__(self, inputId, inputCoords):
        self.id = inputId
        self.coords = inputCoords
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
    def __init__(self, inputId, inputCoords):
        self.id = inputId
        self.coords = inputCoords
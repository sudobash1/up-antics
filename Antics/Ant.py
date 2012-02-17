##
#Ant
#Description: This class represents an ant on the board. All information
#   pertaining to Ants that may be required by the game is stored in this
#   class.
#
#Variables:
#   id - A reference to an Ant that can be manually tracked, so that the
#       programmer can define Ant equality.
#   coords - An int[] of length 2, representing the Ant's position on the
#       board.  Positions start at (0, 0) in the upper left and increase down
#       and to the right.
#   type - Ants come in all shapes and sizes. Type is an int that indexes into
#       an array of stats for various ant types.
#   alive - A boolean representing if the Ant's alive or not.
#   carrying - A boolean representing if the Ant's carrying food or not.
##
class Ant:

    ##
    #__init__
    #Description: Creates a new Ant
    #
    #Parameters:
    #   inputId - The id to use for refrencing the ant (int)
    #   inputCoords - The position on the board to place the Ant at (int[])
    #   inputType - The type of ant to create (int)
    ##
    def __init__(self, inputId, inputCoords, inputType):
        self.id = inputId
        self.coords = inputCoords
        self.type = inputType
        self.alive = True
        self.carrying = False

    ##
    #die
    #Description: Does all maintenance necessary for removing an Ant from the
    #   game.
    ##
    def die(self):
        self.alive = False
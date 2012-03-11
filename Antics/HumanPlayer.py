##
#HumanPlayer
#Description: The responsbility of this class is to interact with the game by
#deciding a valid move based on a given game state.
#
#Variables:
#   playerId - The id of the player.
##
class HumanPlayer(Player):

    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    ##
    def __init__(self, inputPlayerId):
        super(HumanPlayer,self).__init__(inputPlayerId)
        self.moveList = []
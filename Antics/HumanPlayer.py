from Player import *

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
        
    ##
    #getPlacement
    #Description: called during setup phase for each Construction that must be placed by the player.
    #   These items are: 1 Anthill on the player's side; 9 grass on the player's side; and 2 food on the enemy's side.
    #
    #Parameters:
    #   construction - the Construction to be placed.
    #   currentState - the state of the game at this point in time.
    #
    #Return: The coordinates of where the construction is to be placed
    ##
    def getPlacement(self, construction, currentState):
        if len(self.moveList) == 0:
            return None
        target = self.moveList[0]
        self.moveList = []
        return target
        
    ##
    #getMove
    #Description: Gets the next move from the Player.
    #
    #Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    #Return: The Move to be made
    ##
    def getMove(self, currentState):
        #method template, not implemented
        pass
    
    ##
    #getAttack
    #Description: Gets the attack to be made from the Player
    #
    #Parameters:
    #   enemyLocation - The Locations of the Enemies that can be attacked (Location[])
    ##
    def getAttack(self, enemyLocations):
        #method template, not implemented
        pass
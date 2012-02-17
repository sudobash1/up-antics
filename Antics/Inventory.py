##
#Inventory
#Description: This class keeps track of the resources at a player's disposal
#
#Variables
#   player - The id of the player that this inventory belongs to
#   ants - The ants belonging to the player
#   foodCount - The amount of food that the player has to use
##
class Inventory:

    ##
    #__init__
    #Description: Creates a new Inventory
    #Parameters:
    #   playerId - The id of the player that owns the Inventory (int)
    #   antArray - An array containing the Player's Ants (Ant[])
    #   food - The amount of food in the Inventory (int)
    ##
	def __init__(self, playerId, antArray, food):
		self.player = playerId
		self.ants = antArray
		self.foodCount = food

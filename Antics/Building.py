##
#Building
#Description: Represents any static object that can be placed on the board
#   aside from food.
#
#Variables:
#   type - int identifying the type of Building, which allows the game to
#       decide what to do with it.
#   player - int equal to the playerId of the player that owns this Building.
#   captureHealth - int representing the amount of damage this Building can
#       take before being captured.
##
class Building(Construction):
	def __init__(self,inputId,inputCoords, inputType, inputPlayer, inputHealth):
        super(Building,self).__init__(inputId,inputCoords)
		self.type = inputType
		self.player = inputPlayer
		self.captureHealth = inputHealth		
	
	
	
